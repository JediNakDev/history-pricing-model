# HISTORY PRICING MODEL

This repository will domonstrate how to price option with history pricing model.

## What is History Pricing Model?

Instead of using Heston model with Monte Carlo Simulation to determine the probability of an assets to move to some price using 'historical collected/calculated volatility', this model will used historical data directly to determine that probability.

## Assumptions

- The assets price follows Geometric Brownian Motion (GBM)
- The assets price is log-normally distributed

## Model Iteration 1

- use the full historical data to calculate the probability of an assets to move to some price and price option
- price option still a bit off from the actual price

## TODO

- [x] Fetch price history data from yahoo finance API
- [x] Calculate probability of an assets to move to some price using historical data
- [x] Price option using history pricing model
- [ ] Compare the result with Heston model
