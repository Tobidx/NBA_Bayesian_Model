import pandas as pd
import numpy as np
from typing import Tuple, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Process NBA shooting data for model input
    """
    def __init__(self):
        self.processed_shots = None
        self.processed_players = None

    def process_shot_data(self, shots_df: pd.DataFrame) -> pd.DataFrame:
        """
        Process raw shot data

        Args:
            shots_df: Raw shot DataFrame loaded from local path
        """
        logger.info("Processing shot data...")
        try:
            # Make copy to avoid modifying original
            df = shots_df.copy()

            # Calculate shot distance from coordinates
            df['shot_distance'] = np.sqrt(
                df['x_location']**2 + df['y_location']**2
            )

            # Convert shot outcome to binary
            df['shot_made'] = df['shot_outcome'].map({'made': 1, 'missed': 0})

            # Calculate fatigue metrics
            df = self._calculate_fatigue(df)

            # Normalize numerical features
            features_to_normalize = ['shot_distance', 'defender_dist']
            for feature in features_to_normalize:
                df[feature] = (df[feature] - df[feature].mean()) / df[feature].std()

            self.processed_shots = df
            logger.info("Shot data processing completed")
            return df

        except Exception as e:
            logger.error(f"Error processing shot data: {str(e)}")
            raise

    def process_player_data(self, players_df: pd.DataFrame) -> pd.DataFrame:
        """
        Process player data

        Args:
            players_df: Raw player DataFrame loaded from local path
        """
        logger.info("Processing player data...")
        try:
            df = players_df.copy()

            # Calculate career shooting percentage
            df['career_fg_pct'] = df['career_fg_made'] / df['career_fg_attempts']

            # Handle any missing values
            df['career_fg_pct'] = df['career_fg_pct'].fillna(df['career_fg_pct'].mean())

            self.processed_players = df
            logger.info("Player data processing completed")
            return df

        except Exception as e:
            logger.error(f"Error processing player data: {str(e)}")
            raise

    def _calculate_fatigue(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate fatigue metrics"""
        try:
            # Sort by player and game time
            df = df.sort_values(['player_id', 'game_id', 'game_clock'])

            # Calculate minutes played in game
            df['minutes_played'] = df.groupby(['player_id', 'game_id'])['game_clock'].transform(
                lambda x: (2880 - x) / 60  # Convert seconds to minutes
            )

            # Calculate fatigue score
            df['fatigue_score'] = df['minutes_played']
            df['fatigue_score'] = (df['fatigue_score'] - df['fatigue_score'].mean()) / df['fatigue_score'].std()

            return df

        except Exception as e:
            logger.error(f"Error calculating fatigue: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    # Use your actual file paths
    SHOTS_PATH = "C:/Users/Ajibola/Documents/NBA_Data/shots.csv"
    PLAYERS_PATH = "C:/Users/Ajibola/Documents/NBA_Data/players.csv"

    # First load the data
    from data_loader import NBADataLoader
    loader = NBADataLoader()
    shots_df = loader.load_shots_data(SHOTS_PATH)
    players_df = loader.load_players_data(PLAYERS_PATH)

    # Then process it
    processor = DataProcessor()
    processed_shots = processor.process_shot_data(shots_df)
    processed_players = processor.process_player_data(players_df)

    # Show some info about processed data
    print("\nProcessed Data Info:")
    print(f"Number of shots: {len(processed_shots)}")
    print(f"Number of players: {len(processed_players)}")
    print("\nFeatures available:")
    print(processed_shots.columns.tolist())