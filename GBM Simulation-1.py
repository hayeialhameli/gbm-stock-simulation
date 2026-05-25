import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
import os

print("Saving files to:", os.getcwd()
      )
np.random.seed(1)
os.makedirs("charts", exist_ok=True)

# Variables

startPrice = 100.0 # Starting at $100, could be any price
annualReturn = 0.08 # Assuming the annual return to be at 8%
time = 1.0 # The length of the simulation will only be one year
tradingDays = 252 # Actual Trading Days in a Year
dt = time / tradingDays 
tGrid = np.linspace(0, time, tradingDays + 1) 

# Figure 1: Simulated Price Paths (Medium Volatility, 200 Simulations)

medVolatility = 0.20 # Assumed Medium Volatility (20%)
nSims = 200 # Number of Simulations

paths = np.zeros((nSims, tradingDays + 1)) 
paths[:, 0] = startPrice
Z = np.random.standard_normal((nSims, tradingDays))

for i in range(tradingDays):
    drift = (annualReturn - 0.5 * medVolatility**2) * dt
    shock = medVolatility * np.sqrt(dt) * Z[:, i]
    paths[:, i+1] = paths[:, i] * np.exp(drift + shock)

fig, ax = plt.subplots(figsize=(10, 5.5))

for j in range(nSims):
    ax.plot(tGrid, paths[j], lw = 0.6, alpha = 0.35, color = "#4472C4")

averagePaths = paths.mean(axis=0)

ax.plot(tGrid, averagePaths, lw = 2.2, color = "#C00000", label = "Average Path", zorder = 5)
ax.plot(tGrid, startPrice * np.exp(annualReturn * tGrid), lw = 2.2, ls = "--", color = "#375623", label = r"$S_0 e^{\mu t}$ (Theoretical Mean)", zorder = 5)

ax.set_xlabel("Time (Years)", fontsize = 12)
ax.set_ylabel("Stock Price ($)", fontsize  = 12)
ax.set_title(f"GBM Simulated Stock Price Paths\n"
              rf"($S_0 = {startPrice}$, $\mu = {annualReturn}$, $\sigma = {medVolatility}$, {nSims} simulations)", fontsize = 13)
ax.legend(fontsize = 11)
ax.grid(True, alpha = 0.3)
ax.set_xlim(0, time)
fig.tight_layout()
fig.savefig("charts/figure1_paths.png", dpi = 150, bbox_inches = "tight")
plt.close()
print("Figure 1 saved")

# Figure 2: Low vs. High Volatility Comparison

lowVolatility = 0.1 # Low Volatility (10%)
highVolatility = 0.4 # High Volatility (40%)

nSims2 = 150

fig, axes = plt.subplots(1, 2, figsize = (13, 5.5), sharey = False)


# Low Volatility

ax = axes[0]

pathsLow = np.zeros((nSims2, tradingDays + 1))
pathsLow[:, 0] = startPrice
Zv = np.random.standard_normal((nSims2, tradingDays))

for i in range(tradingDays):
    drift = (annualReturn - 0.5 * lowVolatility**2) * dt
    shock = lowVolatility * np.sqrt(dt) * Zv[:, i]
    pathsLow[:, i + 1] = pathsLow[:, i] * np.exp(drift + shock)

for j in range(nSims2):
    ax.plot(tGrid, pathsLow[j], lw = 0.5, alpha = 0.3, color = "#4472C4")

finals = pathsLow[:, -1]

ax.plot(tGrid, pathsLow.mean(axis = 0), lw = 2, color = "black", label = "Mean")
ax.plot(tGrid, startPrice * np.exp(annualReturn * tGrid), lw = 2, ls = "--", color = "#375623", label = r"$S_0 e^{\mu t}$")
ax.set_xlabel("Time (Years)", fontsize = 11)
ax.set_ylabel("Stock Price ($)", fontsize = 11)
ax.set_title(f"Low Volatility\nFinal Price: mean = ${finals.mean():.1f}, std = ${finals.std():.1f}", fontsize = 11)
ax.legend(fontsize = 10)
ax.grid(True, alpha = 0.3)
ax.set_xlim(0, time)

# High Volatility

ax = axes[1]

pathsHigh = np.zeros((nSims2, tradingDays + 1))
pathsHigh[:, 0] = startPrice
ZHigh = np.random.standard_normal((nSims2, tradingDays))

for i in range(tradingDays):
    drift = (annualReturn - 0.5*highVolatility**2) * dt
    shock = highVolatility * np.sqrt(dt) * ZHigh[:, i]
    pathsHigh[:, i + 1] = pathsHigh[:, i] * np.exp(drift + shock)

for j in range(nSims2):
    ax.plot(tGrid, pathsHigh[j], lw = 0.5, alpha = 0.3, color = "#C00000")

finals = pathsHigh[:, -1]

ax.plot(tGrid, pathsHigh.mean(axis = 0), lw = 2, color = "black", label = "Mean")
ax.plot(tGrid, startPrice * np.exp(annualReturn * tGrid), lw = 2, ls = "--", color = "#375623", label = r"$S_0 e^{\mu t}$")
ax.set_xlabel("Time (Years)", fontsize = 11)
ax.set_ylabel("Stock Price ($)", fontsize = 11)
ax.set_title(f"High Volatility\nFinal Price: mean = ${finals.mean():.1f}, std = ${finals.std():.1f}", fontsize = 11)
ax.legend(fontsize = 10)
ax.grid(True, alpha = 0.3)
ax.set_xlim(0, time)

fig.suptitle(r"Volatility Effect on GBM Stock Price Paths ($\mu = 0.08$, 150 simulations)", fontsize = 13, y = 1.01)
fig.tight_layout()
fig.savefig("charts/figure2_volatility.png", dpi = 150, bbox_inches = "tight")
plt.close()
print("Figure 2 saved")

# Figure 3: Final Price Distribution 

nSims3 = 1000
paths3 = np.zeros((nSims3, tradingDays + 1))
paths3[:, 0] = startPrice

Z3 = np.random.standard_normal((nSims3, tradingDays))

for i in range(tradingDays):
    drift = (annualReturn - 0.5 * medVolatility**2) * dt
    shock = medVolatility * np.sqrt(dt) * Z3[:, i]
    paths3[:, i+1] = paths3[:, i] * np.exp(drift + shock)

finals3 = paths3[:, -1]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left Histogram (Histogram of Final Prices)

ax = axes[0]
nBins = 45

ax.hist(finals3, bins = nBins, density = True, color = "#4472C4", alpha = 0.7, edgecolor = "white", lw = 0.4)

muLn = (annualReturn - 0.5 * medVolatility**2) * time
sigLn = medVolatility * np.sqrt(time)
xRange = np.linspace(finals3.min(), finals3.max(), 400)
pdfLn = stats.lognorm.pdf(xRange, s = sigLn, scale = startPrice * np.exp(muLn))

ax.plot(xRange, pdfLn, lw = 2.5, color = "#C00000", label = "Log-normal PDF")
ax.axvline(finals3.mean(), color = "#375623", lw = 2, ls = "--", label = f"Mean=${finals3.mean():.1f}")
ax.axvline(np.median(finals3), color = "orange", lw = 2, ls = ":", label = f"Median=${np.median(finals3):.1f}")
ax.set_xlabel("Final Stock Price ($)", fontsize=11)
ax.set_ylabel("Density", fontsize = 11)
ax.set_title(f"Distribution of Final Prices After 1 Year\n(σ={medVolatility}, n={nSims3})", fontsize = 11)
ax.legend(fontsize = 10)
ax.grid(True, alpha = 0.3)


# Right histogram (Histogram of log-returns)

ax = axes[1]
logReturns = np.log(finals3 / startPrice)

ax.hist(logReturns, bins = 45, density = True, color = "#ED7D31", alpha = 0.75, edgecolor = "white", lw = 0.4)

muRet = (annualReturn - 0.5 * medVolatility**2) * time
sigRet = medVolatility * np.sqrt(time)
xR = np.linspace(logReturns.min(), logReturns.max(), 400)

ax.plot(xR, stats.norm.pdf(xR, muRet, sigRet), lw = 2.5, color = "#C00000", label = "Normal PDF")
ax.axvline(logReturns.mean(), color = "#375623", lw = 2, ls = "--", label = f"Mean = {logReturns.mean():.3f}")
ax.set_xlabel(r"Log-Return $\ln(S_T / S_0)$", fontsize = 11)
ax.set_ylabel("Density", fontsize = 11)
ax.set_title("Distribution of Log-Returns After 1 Year", fontsize = 11)
ax.legend(fontsize = 10)
ax.grid(True, alpha = 0.3)

fig.suptitle("GBM Final Price & Log-Return Distributions", fontsize=13, y=1.01)
fig.tight_layout()
fig.savefig("charts/figure3_distributions.png", dpi = 150, bbox_inches = "tight")
plt.close()
print("Figure 3 saved")

# Figure 4: Confidence bands

nSims4 = 1000
paths4 = np.zeros((nSims4, tradingDays + 1))
paths4[:, 0] = startPrice

Z4 = np.random.standard_normal((nSims4, tradingDays))

for i in range(tradingDays):
    drift = (annualReturn - 0.5 * medVolatility**2) * dt
    shock = medVolatility * np.sqrt(dt) * Z4[:, i]
    paths4[:, i+1] = paths4[:, i] * np.exp(drift + shock)

fig, ax = plt.subplots(figsize = (10, 5.5))

p5 = np.percentile(paths4, 5, axis = 0)
p25 = np.percentile(paths4, 25, axis = 0)
p50 = np.percentile(paths4, 50, axis = 0)
p75 = np.percentile(paths4, 75, axis = 0)
p95 = np.percentile(paths4, 95, axis = 0)

ax.fill_between(tGrid, p5, p95, alpha = 0.20, color = "#4472C4", label = "5th-95th percentile")
ax.fill_between(tGrid, p25, p75, alpha = 0.40, color = "#4472C4", label = "25th-75th percentile")
ax.plot(tGrid, p50, lw = 2.2, color = "#4472C4", label = "Median (50th percentile)")
ax.plot(tGrid, startPrice * np.exp(annualReturn * tGrid), lw = 2, ls = "--", color = "#C00000", label = r"Theoretical mean $S_0 e^{\mu t}$")

ax.set_xlabel("Time (Years)", fontsize = 12)
ax.set_ylabel("Stock Price ($)", fontsize = 12)
ax.set_title(f"GBM Uncertainty Bands Over Time\n($\sigma$ = {medVolatility}, $\mu$ = {annualReturn}, n = {nSims4})", fontsize = 13)
ax.legend(fontsize = 11)
ax.grid(True, alpha = 0.3)
ax.set_xlim(0, time)
fig.tight_layout()
fig.savefig("charts/figure4_bands.png", dpi = 150, bbox_inches = "tight")
plt.close()
print("Figure 4 saved")

print("\nAll charts generated successfully.")
print("Final price stats (Fig 3, n = 1000):")
print(f" Mean: ${finals3.mean():.2f}")
print(f" Median: ${np.median(finals3):.2f}")
print(f" Standard Deviation: ${finals3.std():.2f}")
print(f" 5th percentile: ${np.percentile(finals3, 5):.2f}")
print(f" 95th percentile: ${np.percentile(finals3, 95):.2f}")