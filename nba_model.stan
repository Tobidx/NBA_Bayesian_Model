data {
  int<lower=0> N_shots;         // number of shots
  int<lower=0> N_players;       // number of players
  int<lower=0> N_games;         // number of games
  
  // Shot data
  int<lower=0,upper=1> made[N_shots];        // 1 if shot made, 0 if missed
  vector[N_shots] distance;                   // shot distance
  int<lower=1,upper=N_players> player[N_shots];  // player ID for each shot
  vector[N_shots] defender_distance;          // distance to nearest defender
  int<lower=1,upper=N_games> game[N_shots];   // game ID for each shot
  vector[N_shots] fatigue_score;              // fatigue metric
  
  // Player data
  vector[N_players] career_fg_pct;           // career shooting percentages
}

parameters {
  // Player parameters
  vector[N_players] ability_raw;
  real<lower=0> sigma_player;
  
  // Shot factors
  real beta_distance;
  real beta_defender;
  real beta_fatigue;
  
  // Game effects
  vector[N_games] game_effect_raw;
  real<lower=0> sigma_game;
  
  // Hierarchical parameters
  real mu_ability;
  real<lower=0> tau_ability;
}

transformed parameters {
  vector[N_players] ability = mu_ability + tau_ability * ability_raw;
  vector[N_games] game_effect = sigma_game * game_effect_raw;
}

model {
  // Priors
  mu_ability ~ normal(0, 1);
  tau_ability ~ cauchy(0, 2);
  sigma_player ~ cauchy(0, 2);
  sigma_game ~ cauchy(0, 1);
  
  beta_distance ~ normal(0, 1);
  beta_defender ~ normal(0, 1);
  beta_fatigue ~ normal(-0.1, 0.5);
  
  ability_raw ~ normal(0, 1);
  game_effect_raw ~ normal(0, 1);
  
  // Likelihood
  for (i in 1:N_shots) {
    real shot_prob = inv_logit(
      ability[player[i]] +
      beta_distance * distance[i] +
      beta_defender * defender_distance[i] +
      beta_fatigue * fatigue_score[i] +
      game_effect[game[i]]
    );
    made[i] ~ bernoulli(shot_prob);
  }
}