![licence](https://img.shields.io/github/license/Zncl2222/Stochastic_UC_SGSIM)
![python](https://img.shields.io/pypi/pyversions/uc-sgsim)
![language](https://img.shields.io/badge/Solutions-black.svg?style=flat&logo=c%2B%2B)
![language](https://img.shields.io/badge/Solutions-black.svg?style=flat&logo=python)
[![ci](https://github.com/Zncl2222/Stochastic_UC_SGSIM/actions/workflows/github-pre-commit.yml/badge.svg)](https://github.com/Zncl2222/Stochastic_UC_SGSIM/actions/workflows/github-pre-commit.yml)
[![build](https://github.com/Zncl2222/Stochastic_UC_SGSIM/actions/workflows/cmake.yml/badge.svg)](https://github.com/Zncl2222/Stochastic_UC_SGSIM/actions/workflows/cmake.yml)
[![build](https://github.com/Zncl2222/Stochastic_UC_SGSIM/actions/workflows/codeql.yml/badge.svg)](https://github.com/Zncl2222/Stochastic_UC_SGSIM/actions/workflows/codeql.yml)
[![codecov](https://codecov.io/gh/Zncl2222/uc_sgsim/branch/main/graph/badge.svg?token=3qZt0OqDNI)](https://codecov.io/gh/Zncl2222/uc_sgsim)

#### Python Sonar Cloud state
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_py&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_py)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_py&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_py)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_py&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_py)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_py&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_py)


#### C Sonar Cloud state
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_c&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_c)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_c&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_c)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_c&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_c)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_c&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_c)


<h3 align="center">

> __Warning__
> This project is still in the pre-dev stage, the API usuage may be subject to change

</h3>

## UnConditional Sequential Gaussian SIMulation (UCSGSIM)

<h3 align="center">An unconditional random field generation tools that are easy to use.</h3>

## Introduction of UCSGSIM
Sequential Gaussian Simulation is a random field generation method which was based on the kriging interporlation method.

Unconditonal simulation don't follow the patterns of "data", but follow the users's settings like mean and variance.

**The core ideas of UCSGSIM are:**
1. Create the grid (no any data value exist now).

$$ \Omega\to R $$

2. Visit random point of the model (draw one random value of the x_grid)

$$ X = RandomValue(\Omega),  X:\Omega\to R $$

3. Select the **theoritical covariance model** to use, and set the **sill** and **range** properly.

$$ Gaussian = (C_{0} - s)(1 - e^{-h^{2}/r^{2}a})$$

$$ Spherical = (C_{0} - s)(3h/2r - h^3/2r^3)$$

$$ Exponential = (C_{0} - s)(1 - e^{-h/ra})$$

4. If there have more than 1 data value closed to the visted point (depend on the **range** of covariance model), then go next step. Else draw the random value from normal distribution as the simulation results of this iteration.

$$ Z_{k}({X_{simulation}}) = RandomNormal(m = 0 ,\sigma^2 = Sill)$$

5. Calculate **weights** from the **data covaraince** and **distance coavariance**

$$ \sum_{j=1}^{n}\omega_{j} = C(X_{data}^{i},X_{data}^{i})C^{-1}(X_i,X_i), i=1...N $$

6. Calculate the **kriging estimate** from the **weight** and **data value**

$$ Z_{k}(X_{estimate}) = \sum_{i=1}^{n} \omega_{i} Z(X_{data}) + (1- \sum_{i=1}^{n} \omega_{i} m_{g}) $$

7. Calculate the **kriging error (kriging variance)** from **weights** and **data covariance**

$$ \sigma_{krige}^{2} = \sum_{i=1}^{n}\omega_{i}C(X_{data}^{i},X_{data}^{i}) $$

8. Draw the random value from the normal distribution and add to the **kriging estimate**.

$$ Z(X_{simulation}) = Z(X_{estimate}) + RandomNormal(m = 0, \sigma^2 = \sigma_{krige}^{2}) $$

9. Repeat 2 ~ 8 until the whole model are simulated.

10. Repeat 1 ~ 9 with different **randomseed number** to produceed mutiple realizations.

## Installation
```bash
pip install uc-sgsim
```

## Features
* One dimensional unconditional randomfield generation with sequential gaussian simulation algorithm
* Muti-cores simulation (mutiprocessing)
* Run C to generate randomfield in python via ctype interface, or just generate randomfield in python with numpy and scipy library.

## Example
```py
import matplotlib.pyplot as plt
import uc_sgsim as uc
from uc_sgsim.cov_model import Gaussian

if __name__ == '__main__':
    x = 151  # Model grid, only 1D case is support now

    bw_s = 1  # lag step
    bw_l = 35  # lag range
    randomseed = 151  # randomseed for simulation
    k_range = 17.32  # effective range of covariance model
    sill = 1  # sill of covariance model

    nR = 10  # numbers of realizations in each CPU cores,
    # if nR = 1 n_process = 8
    # than you will compute total 8 realizations

    # Create Covariance model first
    cov_model = Gaussian(bw_l, bw_s, k_range, sill)

    # Create simulation and input the Cov model
    sgsim_py = uc.UCSgsim(x, nR, cov_model) # run sgsim with python
    sgsim_c = uc.UCSgsimDLL(x, nR, cov_model) # run sgsim with c

    # Start compute with n CPUs
    sgsim_c.compute(n_process=2, randomseed=randomseed)
    sgsim_py.compute(n_process=2, randomseed=987654)

    sgsim_c.mean_plot('ALL')  # Plot mean
    sgsim_c.variance_plot()  # Plot variance
    sgsim_c.cdf_plot(x_location=10)  # CDF
    sgsim_c.hist_plot(x_location=10)  # Hist
    sgsim_c.variogram_compute(n_process=2)  # Compute variogram before plotting
    # Plot variogram and mean variogram for validation
    sgsim.variogram_plot()
    # Save random_field and variogram
    sgsim_c.save_random_field('randomfields.csv', save_single=True)
    sgsim_c.save_variogram('variograms.csv', save_single=True)

    # show figure
    plt.show()
```

<p align="center">
   <img src="https://github.com/Zncl2222/Stochastic_SGSIM/blob/main/figure/Realizations.png"  width="40%"/>
   <img src="https://github.com/Zncl2222/Stochastic_SGSIM/blob/main/figure/Mean.png"  width="40%"/>
   <img src="https://github.com/Zncl2222/Stochastic_SGSIM/blob/main/figure/Variance.png"  width="40%"/>
   <img src="https://github.com/Zncl2222/Stochastic_SGSIM/blob/main/figure/Variogram.png"  width="50%"/>
   <img src="https://github.com/Zncl2222/Stochastic_SGSIM/blob/main/figure/HIST.png"  width="40%"/>
   <img src="https://github.com/Zncl2222/Stochastic_SGSIM/blob/main/figure/CDF.png"  width="50%"/>
</p>

## Future plans
* 2D unconditional randomfield generation
* GUI (pyhton)
* More covariance models
* More kriging methods (etc. Oridinary Kriging)
* Performance enhancement
* More completely documents and easy to use designs.

## Performance
<p align="center">
<img src="https://github.com/Zncl2222/Stochastic_SGSIM/blob/main/figure/C_Cpp_py_comparision.png"  width="70%"/>
</p>

```
Parameters:

model len = 150

number of realizations = 1000

Range scale = 17.32

Variogram model = Gaussian model

---------------------------------------------------------------------------------------

Testing platform:

CPU: AMD Ryzen 9 4900 hs

RAM: DDR4 - 3200 40GB (Dual channel 16GB)

Disk: WD SN530
```
