# NBA_Bayesian_Model

# NBA Shooting Efficiency Analysis

## Project Overview
This project implements a hierarchical Bayesian model to analyze NBA shooting efficiency, considering factors like defender distance, fatigue, and game context.

## Requirements
- Python 3.8+
- CmdStan
- Required Python packages in requirements.txt

## Data Requirements
The model expects two CSV files:

shots.csv:
-player_id
-game_id
-shot_outcome ('made' or 'missed')
-x_location
-y_location
-game_clock
-defender_dist

players.csv:
-player_id
-games_played
-career_fg_made
-career_fg_attempts

## Run the model:
Compile Stan model
`stanc models/nba_model.stan --output=models/nba_model.hpp`
`make models/nba_model`

Run analysis
`python src/model_fitting.py`
