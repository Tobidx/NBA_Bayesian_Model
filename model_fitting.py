import pandas as pd
import numpy as np
import json
import subprocess
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelFitter:
    def __init__(self, stan_file_path: str):
        """
        Initialize model fitter
        
        Args:
            stan_file_path: Path to your .stan file
        """
        self.stan_file = Path(stan_file_path)
        self.model_exe = None
        self.compile_model()
        
    def compile_model(self):
        """Compile Stan model"""
        try:
            logger.info("Compiling Stan model...")
            # Get the directory and filename
            stan_dir = self.stan_file.parent
            stan_name = self.stan_file.stem
            
            # Compile command
            compile_command = f"stanc {self.stan_file} --output={stan_dir}/{stan_name}.hpp"
            subprocess.run(compile_command, shell=True, check=True)
            
            # Make executable
            make_command = f"make {stan_dir}/{stan_name}"
            subprocess.run(make_command, shell=True, check=True)
            
            self.model_exe = stan_dir / stan_name
            logger.info("Model compiled successfully")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error compiling model: {str(e)}")
            raise
            
    def prepare_data(self, 
                    processed_shots: pd.DataFrame, 
                    processed_players: pd.DataFrame) -> str:
        """
        Prepare and save data for Stan
        
        Returns:
            Path to saved data file
        """
        try:
            stan_data = {
                'N_shots': len(processed_shots),
                'N_players': len(processed_players),
                'N_games': len(processed_shots['game_id'].unique()),
                'made': processed_shots['shot_made'].tolist(),
                'distance': processed_shots['shot_distance'].tolist(),
                'defender_distance': processed_shots['defender_dist'].tolist(),
                'fatigue_score': processed_shots['fatigue_score'].tolist(),
                'player': processed_shots['player_id'].tolist(),
                'game': processed_shots['game_id'].tolist()
            }
            
            # Save data to JSON
            data_path = self.stan_file.parent / 'data.json'
            with open(data_path, 'w') as f:
                json.dump(stan_data, f)
                
            return str(data_path)
            
        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            raise
            
    def run_model(self, data_path: str, 
                 chains: int = 4, 
                 warmup: int = 1000,
                 samples: int = 1000) -> str:
        """
        Run the compiled model
        
        Returns:
            Path to output file
        """
        try:
            logger.info("Running Stan model...")
            output_path = self.stan_file.parent / 'output.csv'
            
            # Build command
            cmd = [
                str(self.model_exe),
                'sample',
                f'num_chains={chains}',
                f'num_warmup={warmup}',
                f'num_samples={samples}',
                f'data file={data_path}',
                f'output file={output_path}',
                'adapt delta=0.95',
                'max_treedepth=12'
            ]
            
            # Run model
            subprocess.run(' '.join(cmd), shell=True, check=True)
            logger.info("Model fitting completed")
            
            return str(output_path)
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running model: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    # Your file paths
    STAN_MODEL_PATH = "C:/Users/Ajibola/Documents/NBA_Project/models/nba_model.stan"
    SHOTS_PATH = "C:/Users/Ajibola/Documents/NBA_Data/shots.csv"
    PLAYERS_PATH = "C:/Users/Ajibola/Documents/NBA_Data/players.csv"
    
    # Load and process data first
    from data_loader import NBADataLoader
    from data_processor import DataProcessor
    
    # Load data
    loader = NBADataLoader()
    shots_df = loader.load_shots_data(SHOTS_PATH)
    players_df = loader.load_players_data(PLAYERS_PATH)
    
    # Process data
    processor = DataProcessor()
    processed_shots = processor.process_shot_data(shots_df)
    processed_players = processor.process_player_data(players_df)
    
    # Fit model
    fitter = ModelFitter(STAN_MODEL_PATH)
    data_path = fitter.prepare_data(processed_shots, processed_players)
    output_path = fitter.run_model(data_path)
    
    print(f"\nModel output saved to: {output_path}")