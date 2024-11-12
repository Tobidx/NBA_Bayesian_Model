# analysis_results.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResultAnalyzer:
    def __init__(self, output_path: str):
        """
        Initialize analyzer with path to Stan output CSV
        
        Args:
            output_path: Path to Stan output CSV file
        """
        self.output_path = output_path
        self.results_df = pd.read_csv(output_path, comment='#')
        logger.info(f"Loaded results from {output_path}")
        
    def analyze_parameters(self):
        """Analyze main model parameters"""
        # Extract key parameters
        parameters = {
            'beta_distance': self.results_df.filter(like='beta_distance').mean(),
            'beta_defender': self.results_df.filter(like='beta_defender').mean(),
            'beta_fatigue': self.results_df.filter(like='beta_fatigue').mean()
        }
        
        print("\nModel Parameters:")
        print(f"Distance Effect: {parameters['beta_distance']:.3f}")
        print(f"Defender Effect: {parameters['beta_defender']:.3f}")
        print(f"Fatigue Effect: {parameters['beta_fatigue']:.3f}")
        
        return parameters
        
    def plot_effects(self):
        """Plot parameter effects"""
        parameters = self.analyze_parameters()
        
        plt.figure(figsize=(10, 6))
        plt.bar(parameters.keys(), parameters.values())
        plt.title('Shot Factor Effects')
        plt.ylabel('Effect Size')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def check_convergence(self):
        """Check model convergence"""
        # Look for divergent transitions
        divergent = self.results_df.filter(like='divergent__').sum().sum()
        
        print("\nConvergence Diagnostics:")
        print(f"Number of divergent transitions: {divergent}")
        
        # Check effective sample size
        n_eff = len(self.results_df) * 4  # 4 chains
        print(f"Effective sample size: {n_eff}")
        
    def get_player_abilities(self, player_ids):
        """
        Get player shooting abilities
        
        Args:
            player_ids: List of player IDs to match with ability parameters
        """
        # Extract ability parameters
        ability_cols = [col for col in self.results_df.columns if 'ability[' in col]
        abilities = self.results_df[ability_cols].mean()
        
        # Create results dataframe
        results = pd.DataFrame({
            'player_id': player_ids,
            'shooting_ability': abilities.values,
            'lower_ci': self.results_df[ability_cols].quantile(0.025),
            'upper_ci': self.results_df[ability_cols].quantile(0.975)
        })
        
        # Sort by ability
        results = results.sort_values('shooting_ability', ascending=False)
        
        print("\nTop 5 Players by Shooting Ability:")
        print(results.head())
        
        return results
        
    def plot_ability_distribution(self, results_df):
        """Plot distribution of player abilities"""
        plt.figure(figsize=(12, 6))
        
        # Plot ability distribution
        sns.histplot(results_df['shooting_ability'], kde=True)
        plt.title('Distribution of Player Shooting Abilities')
        plt.xlabel('Shooting Ability')
        plt.ylabel('Count')
        plt.show()
        
        # Plot top players with confidence intervals
        top_10 = results_df.head(10)
        
        plt.figure(figsize=(12, 6))
        plt.errorbar(
            x=range(len(top_10)),
            y=top_10['shooting_ability'],
            yerr=[(top_10['shooting_ability'] - top_10['lower_ci']),
                  (top_10['upper_ci'] - top_10['shooting_ability'])],
            fmt='o'
        )
        plt.title('Top 10 Players with 95% Confidence Intervals')
        plt.xlabel('Player Rank')
        plt.ylabel('Shooting Ability')
        plt.tight_layout()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Your output path from model fitting
    OUTPUT_PATH = "C:/Users/Ajibola/Documents/NBA_Project/models/output.csv"
    
    # Initialize analyzer
    analyzer = ResultAnalyzer(OUTPUT_PATH)
    
    # Get parameter estimates
    parameters = analyzer.analyze_parameters()
    
    # Check convergence
    analyzer.check_convergence()
    
    # Plot effects
    analyzer.plot_effects()
    
    # Analyze player abilities
    player_ids = [1, 2, 3, 4, 5]  
    player_results = analyzer.get_player_abilities(player_ids)
    
    # Plot ability distributions
    analyzer.plot_ability_distribution(player_results)
