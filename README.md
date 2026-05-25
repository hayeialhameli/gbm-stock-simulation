# Monte Carlo Stock Price Simulation — Geometric Brownian Motion

A Python implementation of Geometric Brownian Motion (GBM) for simulating stock price dynamics, built as part of coursework in stochastic processes at the University of Minnesota.

A full write-up of the mathematical derivation, results, and model limitations is included in [`report.pdf`](./report.pdf).

## Overview

Stock prices are modeled using the stochastic differential equation:

$$dS_t = \mu S_t \, dt + \sigma S_t \, dW_t$$

where $\mu$ is the drift (expected annual return), $\sigma$ is the volatility, and $W_t$ is a standard Brownian motion. The exact solution via Itô's Lemma gives:

$$S_t = S_0 \exp\left[\left(\mu - \frac{\sigma^2}{2}\right)t + \sigma W_t\right]$$

This is discretized over 252 trading days and simulated using Monte Carlo methods.

## Figures

**Figure 1 — Simulated Price Paths**  
200 simulated paths under medium volatility (σ = 0.20), with the simulated mean and theoretical mean overlaid.

**Figure 2 — Volatility Comparison**  
Side-by-side comparison of low (σ = 0.10) and high (σ = 0.40) volatility regimes across 150 simulations.

**Figure 3 — Terminal Distributions**  
Distribution of final prices and log-returns after 1 year across 1000 simulations, with fitted log-normal and normal PDFs.

**Figure 4 — Uncertainty Bands**  
Percentile-based confidence bands (5th–95th, 25th–75th) over time across 1000 simulations.

## Key Results

| Statistic | Value |
|---|---|
| Initial price | $100.00 |
| Mean final price | $108.36 |
| Median final price | $106.79 |
| Standard deviation | $22.20 |
| 5th percentile | $76.13 |
| 95th percentile | $149.59 |
| Theoretical mean $S_0 e^{\mu T}$ | $108.33 |

The simulated mean ($108.36) closely matches the theoretical mean ($108.33), confirming correct implementation.

## Requirements

```
numpy
matplotlib
scipy
```

Install with:
```bash
pip install numpy matplotlib scipy
```

## Usage

```bash
python gbm_simulation.py
```

Charts are saved to a `charts/` folder in the working directory.

## Parameters

| Parameter | Value | Description |
|---|---|---|
| `startPrice` | 100.0 | Initial stock price |
| `annualReturn` | 0.08 | Expected annual drift (μ) |
| `medVolatility` | 0.20 | Medium volatility (σ) |
| `tradingDays` | 252 | Trading days per year |

## Author

Hayei Alhameli — Mathematics, University of Minnesota Twin Cities  
[LinkedIn](https://linkedin.com/in/hayeialhameli) · [GitHub](https://github.com/hayeialhameli)
