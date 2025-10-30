# HISTORY PRICING MODEL

This repository prices options directly from empirical market data instead of simulated paths (e.g., Heston/Monte Carlo). It estimates the payoff using historical return distributions, lower compute cost, and reduced model misspecification risk.

## Assumptions

- The assets price follows Geometric Brownian Motion (GBM)
- The assets price is log-normally distributed

## Model Iteration 1

- use the full historical data to calculate the probability of an assets to move to some price and price option
- The predicted option price is still a bit off from the actual price

## Model Iteration 2

- Refine the drift estimation using historical data
- Enforce the martingale condition to ensure the model is consistent with the market data

## TODO

- [x] Fetch price history data from yahoo finance API
- [x] Calculate probability of an assets to move to some price using historical data
- [ ] Iteration 1
  - [x] Price option using history pricing model
- [ ] Iteration 2
  - [ ] Refine the drift estimation using historical data
  - [ ] Enforce the martingale condition to ensure the model is consistent with the market data
- [ ] Compare the result with Heston model
