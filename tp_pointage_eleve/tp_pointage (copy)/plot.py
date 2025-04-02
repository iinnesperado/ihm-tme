import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc
from scipy.stats import norm
from scipy.optimize import minimize

# Task 3 #
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
    gvalues = []
    for i in range(1, 100):
        gvalues.append(g(i, c, r))
    plt.plot(range(1,100), gvalues, label="c=%.1f, r=%.1f" % (c,r))

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
sigma_values = [0.5, 1.0, 2.0, 3.0]
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

data = np.loadtxt("pointing_data_sample.txt")
# print(data)
 
def gaussian_llh(params, data): 
    mu, sigma = params
    return - np.sum(norm.logpdf(data, loc=mu, scale=sigma))

def emg_llh(params, data):
    mu, sigma, beta = params
    pdf_values = emg_pdf(np.array(data), mu, sigma=sigma, beta=beta)
    return - np.sum(np.log(np.maximum(pdf_values, 1e-10)))

def fit_models(data):
    """
    Fit both Gaussian and EMG models to data
    Returns:
        gauss_params: (mu, sigma)
        emg_params: (mu, sigma, beta)
        gauss_ll: Gaussian log-likelihood
        emg_ll: EMG log-likelihood
    """
    # Initial guesses (mean, std of data)
    mu_init = np.mean(data)
    sigma_init = np.std(data)
    
    # Gaussian fit
    gauss_result = minimize(
        gaussian_llh,
        x0=[mu_init, sigma_init],
        args=(data,),
        bounds=[(None, None), (1e-10, None)]  # sigma > 0
    )
    gauss_params = gauss_result.x
    gauss_ll = gauss_result.fun
    
    # EMG fit
    emg_result = minimize(
        emg_llh,
        x0=[mu_init, sigma_init, 1.0],  # initial beta guess = 1
        args=(data,),
        bounds=[(None, None), (1e-10, None), (1e-10, None)]  # sigma, beta > 0
    )
    emg_params = emg_result.x
    emg_ll = emg_result.fun

    print("Gaussian fit:")
    print(f"μ = {gauss_params[0]:.3f}, σ = {gauss_params[1]:.3f}")
    print(f"Log-likelihood = {gauss_ll:.3f}\n")

    print("EMG fit:")
    print(f"μ = {emg_params[0]:.3f}, σ = {emg_params[1]:.3f}, β = {emg_params[2]:.3f}")
    print(f"Log-likelihood = {emg_ll:.3f}")
    
    return gauss_params, emg_params#, gauss_ll, emg_ll

gauss_params, emg_params = fit_models(data)

plt.figure(figsize=(10, 6))
plt.hist(data, bins=40, color="xkcd:barbie pink", alpha=0.4, label="Data")

xvals = np.linspace(min(data), max(data), 500)
plt.plot(xvals, norm.pdf(x, *gauss_params), label= f"Gaussian (μ={gauss_params[0]:.2f}, σ={gauss_params[1]:.2f})")
mu, sigma, beta = emg_params
plt.plot(xvals, emg_pdf(xvals, mu, sigma, beta), label=f"EMG (μ={mu:.2f}, σ={sigma:.2f}, β={beta:.2f})")


plt.title("Modeling of data sample")
plt.xlabel("Pointing Time")
plt.ylabel("Density")
plt.legend()
plt.grid(True, alpha=0.3)





plt.show()