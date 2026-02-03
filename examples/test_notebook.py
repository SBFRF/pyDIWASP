#!/usr/bin/env python
# coding: utf-8

# # pyDIWASP Example: Directional Wave Spectrum Analysis
# 
# This notebook demonstrates how to use pyDIWASP to analyze directional wave spectra from instrument array data.
# 
# ## Overview
# 
# pyDIWASP is a Python implementation of the DIWASP (DIrectional WAve SPectrum) toolbox. It estimates the directional distribution of wave energy from measurements by an array of wave instruments.
# 
# ### What is a Directional Wave Spectrum?
# 
# A directional wave spectrum describes how wave energy is distributed across:
# - **Frequencies** (or wave periods)
# - **Directions** (where waves are coming from)
# 
# This is more informative than a 1D frequency spectrum because it tells us not just how much energy is at each frequency, but also which direction that energy is traveling.

# ## Setup
# 
# First, import the necessary libraries:

# In[ ]:


import sys
import numpy as np
import matplotlib.pyplot as plt

# Add parent directory to path to import pyDIWASP modules
sys.path.insert(0, '..')

from dirspec import dirspec
from infospec import infospec
from plotspec import plotspec

# Set random seed for reproducibility
np.random.seed(42)

print("Libraries imported successfully!")


# ## Example 1: Basic Directional Spectrum Analysis
# 
# In this example, we'll create synthetic wave data representing a wave field with:
# - A dominant wave direction from the east (90 degrees)
# - Peak period around 10 seconds (0.1 Hz)
# - Wave height around 2 meters
# 
# We'll use a simple 3-sensor array to measure pressure at different locations.

# ### Step 1: Generate Synthetic Wave Data
# 
# We'll create a simple wave field using superposition of sinusoidal components:

# In[ ]:


# Simulation parameters
duration = 1024  # seconds
fs = 2.0  # sampling frequency (Hz)
depth = 10.0  # water depth (m)

# Time array
t = np.arange(0, duration, 1/fs)
nsamples = len(t)

# Wave parameters
peak_freq = 0.1  # Hz (10 second period)
peak_dir = np.pi/2  # radians (from East)
wave_amplitude = 1.0  # meters

# Instrument array layout (3 pressure sensors in an L-shape)
# Layout is 3xN array: [x positions; y positions; z positions]
layout = np.array([
    [0, 10, 0],      # x positions (meters)
    [0, 0, 10],      # y positions (meters)
    [-depth, -depth, -depth]  # z positions (meters, negative = below surface)
])

ninst = layout.shape[1]

print(f"Simulation setup:")
print(f"  Duration: {duration} seconds")
print(f"  Sampling rate: {fs} Hz")
print(f"  Number of samples: {nsamples}")
print(f"  Number of instruments: {ninst}")
print(f"  Water depth: {depth} m")
print(f"\nInstrument positions (x, y, z):")
for i in range(ninst):
    print(f"  Sensor {i+1}: ({layout[0,i]:.1f}, {layout[1,i]:.1f}, {layout[2,i]:.1f}) m")


# In[ ]:


# Generate synthetic wave data
# Simple model: superposition of wave components

# Create several wave components with different frequencies and directions
frequencies = np.array([0.08, 0.10, 0.12, 0.15])  # Hz
directions = np.array([np.pi/2, np.pi/2, np.pi/2 + np.pi/6, np.pi/3])  # radians
amplitudes = np.array([0.5, 1.0, 0.3, 0.2])  # meters

# Calculate wavenumbers using dispersion relation: omega^2 = g*k*tanh(k*h)
g = 9.81  # gravity (m/s^2)
wavenumbers = []
for f in frequencies:
    omega = 2 * np.pi * f
    # Solve iteratively for k
    k = omega**2 / g  # deep water approximation as initial guess
    for _ in range(10):
        k = omega**2 / (g * np.tanh(k * depth))
    wavenumbers.append(k)
wavenumbers = np.array(wavenumbers)

# Initialize data array
data = np.zeros((nsamples, ninst))

# Generate pressure signal at each instrument location
for i in range(len(frequencies)):
    f = frequencies[i]
    theta = directions[i]
    A = amplitudes[i]
    k = wavenumbers[i]
    omega = 2 * np.pi * f

    # Phase at each instrument location
    for j in range(ninst):
        x = layout[0, j]
        y = layout[1, j]
        z = layout[2, j]

        # Spatial phase
        phase_xy = k * (x * np.cos(theta) + y * np.sin(theta))

        # Pressure response (includes depth attenuation)
        pressure_response = np.cosh(k * (z + depth)) / np.cosh(k * depth)

        # Add wave component
        random_phase = np.random.uniform(0, 2*np.pi)
        data[:, j] += A * pressure_response * np.cos(omega * t - phase_xy + random_phase)

# Add some noise
noise_level = 0.05  # 5% noise
data += noise_level * np.random.randn(nsamples, ninst)

print(f"\nGenerated wave data shape: {data.shape}")
print(f"Data range: [{data.min():.2f}, {data.max():.2f}] (pressure units)")


# ### Visualize the Generated Data

# In[ ]:


# Plot time series from each instrument
fig, axes = plt.subplots(ninst, 1, figsize=(12, 6), sharex=True)
for i in range(ninst):
    axes[i].plot(t[:500], data[:500, i])
    axes[i].set_ylabel(f'Sensor {i+1}\n(pressure)')
    axes[i].grid(True, alpha=0.3)

axes[-1].set_xlabel('Time (seconds)')
fig.suptitle('Synthetic Wave Measurements (first 250 seconds)', fontsize=14)
plt.tight_layout()
plt.show()


# ### Step 2: Set Up the Instrument Data Structure
# 
# The Instrument Data (ID) structure contains all information about the measurement array:

# In[ ]:


# Create instrument data structure
ID = {
    'layout': layout,
    'datatypes': ['pres', 'pres', 'pres'],  # all pressure sensors
    'depth': depth,
    'fs': fs,
    'data': data
}

print("Instrument Data (ID) structure created:")
print(f"  Layout shape: {ID['layout'].shape}")
print(f"  Data types: {ID['datatypes']}")
print(f"  Depth: {ID['depth']} m")
print(f"  Sampling frequency: {ID['fs']} Hz")
print(f"  Data shape: {ID['data'].shape}")


# ### Step 3: Define the Spectral Matrix Structure
# 
# The Spectral Matrix (SM) structure defines the frequency and directional resolution of the output:

# In[ ]:


# Define output spectral matrix
SM = {
    'freqs': np.linspace(0.05, 0.3, 30),  # frequency bins (Hz)
    'dirs': np.linspace(-np.pi, np.pi, 36)  # direction bins (radians)
}

print("Spectral Matrix (SM) structure created:")
print(f"  Frequency range: {SM['freqs'][0]:.3f} - {SM['freqs'][-1]:.3f} Hz")
print(f"  Number of frequency bins: {len(SM['freqs'])}")
print(f"  Direction range: {SM['dirs'][0]:.2f} - {SM['dirs'][-1]:.2f} radians")
print(f"  Number of direction bins: {len(SM['dirs'])}")
print(f"  Directional resolution: {np.degrees(SM['dirs'][1] - SM['dirs'][0]):.1f} degrees")


# ### Step 4: Set Estimation Parameters
# 
# The Estimation Parameters (EP) structure controls the analysis method:

# In[ ]:


# Define estimation parameters
EP = {
    'method': 'IMLM',  # Iterated Maximum Likelihood Method
    'iter': 100,       # number of iterations
    'smooth': 'ON'     # enable spectral smoothing
}

print("Estimation Parameters (EP) structure created:")
print(f"  Method: {EP['method']}")
print(f"  Iterations: {EP['iter']}")
print(f"  Smoothing: {EP['smooth']}")


# ### Step 5: Compute the Directional Spectrum
# 
# Now we can run the main analysis function:

# In[ ]:


# Compute directional spectrum
print("Computing directional spectrum...")
print("=" * 50)

# Set plot type to 0 (no automatic plotting) so we can customize
options = ['PLOTTYPE', 0]

SMout, EPout = dirspec(ID, SM, EP, options)

print("=" * 50)
print("\nDirectional spectrum computed successfully!")
print(f"Output spectrum shape: {SMout['S'].shape}")


# ### Step 6: Analyze Results
# 
# Use `infospec` to get key wave statistics:

# In[ ]:


# Get wave information
Hsig, Tp, DTp, Dp = infospec(SMout)

print("\n" + "="*50)
print("WAVE ANALYSIS RESULTS")
print("="*50)
print(f"Significant Wave Height (Hsig): {Hsig:.2f} m")
print(f"Peak Period (Tp): {Tp:.2f} s")
print(f"Direction at Peak (DTp): {DTp:.2f} rad = {np.degrees(DTp):.1f}°")
print(f"Dominant Direction (Dp): {Dp:.2f} rad = {np.degrees(Dp):.1f}°")
print("="*50)


# ### Step 7: Visualize the Directional Spectrum
# 
# Create custom visualizations of the results:

# In[ ]:


# Create a 1D frequency spectrum (integrated over directions)
freq_spectrum = np.sum(np.real(SMout['S']), axis=1) * (SMout['dirs'][1] - SMout['dirs'][0])

# Create figure with subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1D frequency spectrum
axes[0].plot(SMout['freqs'], freq_spectrum, 'b-', linewidth=2)
axes[0].axvline(1/Tp, color='r', linestyle='--', label=f'Peak Period = {Tp:.1f}s')
axes[0].set_xlabel('Frequency (Hz)', fontsize=12)
axes[0].set_ylabel('Spectral Density (m²/Hz)', fontsize=12)
axes[0].set_title('Frequency Spectrum (Directionally Integrated)', fontsize=13)
axes[0].grid(True, alpha=0.3)
axes[0].legend()

# Plot 1D directional distribution (integrated over frequencies)
dir_spectrum = np.sum(np.real(SMout['S']), axis=0) * (SMout['freqs'][1] - SMout['freqs'][0])
axes[1].plot(np.degrees(SMout['dirs']), dir_spectrum, 'g-', linewidth=2)
axes[1].axvline(np.degrees(Dp), color='r', linestyle='--', label=f'Dominant Dir = {np.degrees(Dp):.1f}°')
axes[1].set_xlabel('Direction (degrees)', fontsize=12)
axes[1].set_ylabel('Spectral Density (m²/degree)', fontsize=12)
axes[1].set_title('Directional Distribution (Frequency Integrated)', fontsize=13)
axes[1].grid(True, alpha=0.3)
axes[1].legend()

plt.tight_layout()
plt.show()


# In[ ]:


# Create 2D contour plot of directional spectrum
fig, ax = plt.subplots(figsize=(10, 8))

# Convert directions to degrees for better readability
dirs_deg = np.degrees(SMout['dirs'])

# Create meshgrid
F, D = np.meshgrid(SMout['freqs'], dirs_deg)

# Plot filled contours
levels = 20
contourf = ax.contourf(F, D, np.real(SMout['S']).T, levels=levels, cmap='viridis')
contour = ax.contour(F, D, np.real(SMout['S']).T, levels=levels, colors='k', alpha=0.3, linewidths=0.5)

# Add colorbar
cbar = plt.colorbar(contourf, ax=ax, label='Spectral Density (m²s/deg)')

# Mark peak
ax.plot(1/Tp, np.degrees(DTp), 'r*', markersize=15, label=f'Peak: T={Tp:.1f}s, θ={np.degrees(DTp):.1f}°')

ax.set_xlabel('Frequency (Hz)', fontsize=12)
ax.set_ylabel('Direction (degrees)', fontsize=12)
ax.set_title('2D Directional Wave Spectrum', fontsize=14, fontweight='bold')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# ### Step 8: Use Built-in Plotting Functions
# 
# pyDIWASP includes built-in plotting functions for standard visualizations:

# In[ ]:


# 3D surface plot
plotspec(SMout, ptype=1)
plt.title('3D Surface Plot - Cartesian Directions', fontsize=14, fontweight='bold')
plt.show()


# In[ ]:


# Polar contour plot
plotspec(SMout, ptype=2)
plt.title('Polar Contour Plot - Cartesian Directions', fontsize=14, fontweight='bold')
plt.show()


# ## Example 2: Comparing Different Estimation Methods
# 
# pyDIWASP supports several estimation methods. Let's compare two common ones:
# - **IMLM**: Iterated Maximum Likelihood Method (default)
# - **EMEP**: Extended Maximum Entropy Principle

# In[ ]:


# Compute spectrum using EMEP method
EP_emep = {
    'method': 'EMEP',
    'iter': 100,
    'smooth': 'ON'
}

print("Computing directional spectrum using EMEP method...")
print("=" * 50)
SMout_emep, _ = dirspec(ID, SM, EP_emep, ['PLOTTYPE', 0])
print("=" * 50)
print("Complete!\n")

# Get statistics for EMEP
Hsig_emep, Tp_emep, DTp_emep, Dp_emep = infospec(SMout_emep)


# In[ ]:


# Compare the two methods
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# IMLM method
F, D = np.meshgrid(SMout['freqs'], np.degrees(SMout['dirs']))
c1 = axes[0].contourf(F, D, np.real(SMout['S']).T, levels=15, cmap='viridis')
axes[0].plot(1/Tp, np.degrees(DTp), 'r*', markersize=12, label=f'Peak')
axes[0].set_xlabel('Frequency (Hz)')
axes[0].set_ylabel('Direction (degrees)')
axes[0].set_title(f'IMLM Method\nHsig={Hsig:.2f}m, Tp={Tp:.1f}s', fontweight='bold')
plt.colorbar(c1, ax=axes[0], label='Density')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# EMEP method
c2 = axes[1].contourf(F, D, np.real(SMout_emep['S']).T, levels=15, cmap='viridis')
axes[1].plot(1/Tp_emep, np.degrees(DTp_emep), 'r*', markersize=12, label=f'Peak')
axes[1].set_xlabel('Frequency (Hz)')
axes[1].set_ylabel('Direction (degrees)')
axes[1].set_title(f'EMEP Method\nHsig={Hsig_emep:.2f}m, Tp={Tp_emep:.1f}s', fontweight='bold')
plt.colorbar(c2, ax=axes[1], label='Density')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\nComparison of Results:")
print("=" * 50)
print(f"{'Parameter':<20} {'IMLM':<15} {'EMEP':<15}")
print("=" * 50)
print(f"{'Hsig (m)':<20} {Hsig:<15.2f} {Hsig_emep:<15.2f}")
print(f"{'Tp (s)':<20} {Tp:<15.2f} {Tp_emep:<15.2f}")
print(f"{'DTp (degrees)':<20} {np.degrees(DTp):<15.1f} {np.degrees(DTp_emep):<15.1f}")
print(f"{'Dp (degrees)':<20} {np.degrees(Dp):<15.1f} {np.degrees(Dp_emep):<15.1f}")
print("=" * 50)


# ## Summary
# 
# This notebook demonstrated:
# 
# 1. **Setting up input data structures** (ID, SM, EP)
# 2. **Running directional spectrum analysis** using `dirspec()`
# 3. **Extracting wave statistics** using `infospec()`
# 4. **Visualizing results** with both custom plots and built-in functions
# 5. **Comparing different estimation methods** (IMLM vs EMEP)
# 
# ### Key Takeaways
# 
# - pyDIWASP requires three main input structures: ID (instrument data), SM (spectral matrix), and EP (estimation parameters)
# - The IMLM method is the default and works well for most applications
# - Different estimation methods may give slightly different results
# - The output includes both the full 2D spectrum and integrated statistics
# 
# ### Next Steps
# 
# To use pyDIWASP with your own data:
# 1. Load your wave measurement data
# 2. Set up the ID structure with your instrument configuration
# 3. Define appropriate frequency and direction ranges in SM
# 4. Choose an estimation method in EP
# 5. Run `dirspec()` and analyze the results
# 
# For more information, see the [pyDIWASP README](../README.md).
