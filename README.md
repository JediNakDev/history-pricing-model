# HISTORY PRICING MODEL

This repository prices options directly from empirical market data instead of simulated paths (e.g., Heston/Monte Carlo). It estimates the payoff using historical return distributions, lower compute cost, and reduced model misspecification risk.

## Assumptions

- The assets price follows Geometric Brownian Motion (GBM)
- The assets price is log-normally distributed

## Model Iteration 1

- use the full historical data to calculate the probability of an assets to move to some price and price option
- The predicted option price is still a bit off from the actual price

## Model Iteration 1.1

- Account for risk-free rate in the option pricing formula
- Change the data time frame.

## TODO

- [x] Fetch price history data from yahoo finance API
- [x] Calculate probability of an assets to move to some price using historical data
- [x] Iteration 1
  - [x] Price option using history pricing model
- [ ] Iteration 1.1
  - [ ] Test multiple time frames
  - [ ] Change the data time frame to see if it affects the result
  - [x] Account for risk-free rate in the option pricing formula
- [ ] Compare the result with Heston model
