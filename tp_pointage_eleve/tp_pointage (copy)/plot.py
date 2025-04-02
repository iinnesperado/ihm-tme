import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc
from scipy.stats import norm

def g(u, c, r):
    return c*u**r

params = [(0,0),
           (1,1), (3,1), 
           (2,1), 
           (0,1), 
           (0.5, 1), 
           (0.5, -1),
           (-1, 1),
           (-1,-1) ]

plt.figure(figsize=(10, 6))

for r,c in params:
    data = []
    for i in range(1, 100):
        data.append(g(i, c, r))
    plt.plot(range(1,100), data, label="c=%.1f, r=%.1f" % (c,r))

plt.legend()
plt.grid(True, alpha=0.2)
# plt.show()

# Task 15 #

def emg_pdf(x, mu, sigma, beta):
    term1 = (1 / (2 * beta)) * np.exp((1 / (2 * beta)) * (2 * mu + (sigma**2 / beta) - 2 * x))
    term2 = erfc((mu + (sigma**2 / beta) - x) / (np.sqrt(2) * sigma))
    return term1 * term2

# Parameters (fixed μ=0, β=1)
mu = 0
beta = 1
sigma_values = [0.5, 1.0, 2.0, 3.0]  # Test these σ values

# Generate x values
x = np.linspace(-5, 10, 500)

# Plot EMG vs. Gaussian
plt.figure(figsize=(10, 6))
for sigma in sigma_values:
    y_emg = emg_pdf(x, mu, sigma, beta)
    y_gaussian = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)
    
    plt.plot(x, y_emg, label=f'EMG (σ={sigma})')
    plt.plot(x, y_gaussian, '--', label=f'Gaussian (σ={sigma})', alpha=0.7)

plt.title("EMG vs. Gaussian (μ=0, β=1)")
plt.xlabel("x")
plt.ylabel("PDF")
plt.legend()
plt.grid(True, alpha=0.2)

# Task 16 #
file = open("pointing_data_sample.txt", "r")
data = file.read()
data = data.split("\n")
data = data[:-1]
data = [float(i) for i in data]
# print(data)

plt.figure(figsize=(10, 6))
plt.hist(data, bins=40, color="xkcd:barbie pink", alpha=0.4)


#TODO check functions 
def gaussian_llh(params, data): 
    mu, sigma = params
    return np.sum(norm.logpdf(data, loc=mu, scale=0.5))

def emg_llh(params, data):
    mu, sigma, beta = params
    pdf_values = emg_pdf(np.array(data), mu, sigma=0.5, beta=beta)
    return  np.sum(np.log(np.maximum(pdf_values, 1e-10)))

print(f"{gaussian_llh=}\n{emg_llh=}")




plt.title("Modeling of data sample")
plt.xlabel("Vitesses")
plt.ylabel("Fréquence")





plt.show()