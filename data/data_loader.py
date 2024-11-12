import pandas as pd
import numpy as np
from typing import Tuple, Dict
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NBADataLoader:
    def __init__(self):
        """
        Initialize data loader
        """
        self.shots_data = None
        self.players_data = None
        
    def load_shots_data(self, file_path: str) -> pd.DataFrame:
        """
        Load shots data from specific path
        
        Args:
            file_path: Full path to shots data file
        """
        try:
            logger.info(f"Loading shots data from {file_path}")
            shots_df = pd.read_csv(file_path)
            
            # Validate required columns
            required_columns = [
                'player_id', 'game_id', 'shot_outcome',
                'x_location', 'y_location', 'game_clock',
                'defender_dist'
            ]
            
            missing_cols = [col for col in required_columns if col not in shots_df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
                
            self.shots_data = shots_df
            logger.info(f"Successfully loaded {len(shots_df)} shots")
            return shots_df
            
        except Exception as e:
            logger.error(f"Error loading shots data: {str(e)}")
            raise
            
    def load_players_data(self, file_path: str) -> pd.DataFrame:
        """
        Load players data from specific path
        
        Args:
            file_path: Full path to players data file
        """
        try:
            logger.info(f"Loading players data from {file_path}")
            players_df = pd.read_csv(file_path)
            
            # Validate required columns
            required_columns = [
                'player_id', 'games_played',
                'career_fg_made', 'career_fg_attempts'
            ]
            
            missing_cols = [col for col in required_columns if col not in players_df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
                
            self.players_data = players_df
            logger.info(f"Successfully loaded {len(players_df)} players")
            return players_df
            
        except Exception as e:
            logger.error(f"Error loading players data: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    # Use actual paths from your system
    SHOTS_PATH = "C:/Users/Ajibola/Documents/NBA_Data/shots.csv"
    PLAYERS_PATH = "C:/Users/Ajibola/Documents/NBA_Data/players.csv"
    
    loader = NBADataLoader()
    shots_df = loader.load_shots_data(SHOTS_PATH)
    players_df = loader.load_players_data(PLAYERS_PATH)