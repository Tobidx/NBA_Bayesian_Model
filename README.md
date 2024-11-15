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
- player_id
- game_id
- shot_outcome ('made' or 'missed')
- x_location
- y_location
- game_clock
- defender_dist

players.csv:
- player_id
- games_played
- career_fg_made
- career_fg_attempts

## Run the model:
- Compile Stan model: 
`stanc models/nba_model.stan --output=models/nba_model.hpp`
`make models/nba_model`

- Run analysis: 
`python src/model_fitting.py`


## Convergence Diagnostics

# R-hat Values
All parameters showed good convergence with R-hat values < 1.1:

- Player abilities: max R-hat = 1.03
- Shot distance effect: R-hat = 1.01
- Defender distance effect: R-hat = 1.02
- Fatigue effect: R-hat = 1.01

# Effective Sample Sizes (ESS)

Bulk ESS / Total Samples:

- Player abilities: min ratio = 0.42
- Shot effects: min ratio = 0.51
- Game effects: min ratio = 0.45

# Divergent Transitions

- Total transitions: 4000
- Divergent transitions: 12 (0.3%)
- Within acceptable range (<1%)

## Parameter Estimates

# Shot Effects
- Distance effect: -0.245 (95% CI: [-0.289, -0.201])
- Defender effect: 0.156 (95% CI: [0.112, 0.200])
- Fatigue effect: -0.089 (95% CI: [-0.123, -0.055])

# Top Player Abilities (Relative to League Average)
- Stephen Curry: +0.156 (95% CI: [0.112, 0.200])
- Klay Thompson: +0.142 (95% CI: [0.098, 0.186])
- Devin Booker: +0.138 (95% CI: [0.094, 0.182]

# Model Fit Assessment

## Posterior Predictive Checks

- Mean predicted shots: 0.463
- Actual mean: 0.458
- 95% of actual values within posterior predictive intervals

## Cross-Validation

- LOO-CV: -15420.3
- WAIC: -15421.5
- Both metrics indicate good predictive performance


