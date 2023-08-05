# About

The `gravitas` package has one primary goal: to provide lighting fast acceleration vectors for satellite orbit propagation. It currently supports:

| **Model** | **Central Body** | **Maximum Degree/Order** |
|-----------|------------------|--------------------------|
| EGM96     | Earth            | 360                      |
| GRGM360   | Moon             | 360                      |
| MRO120F   | Mars             | 120                      |

# Setup

`pip install gravitas`

# Example Usage

```python
import gravitas
import numpy as np

r_ecef = np.array([[7000.0, 0.0, 0.0], [0.0, 7000.0, 0.0]]) 
# Define an [nx3] numpy array in Earth-Centered, Earth-Fixed (ECEF) coordinates [km]
g_vector = gravitas.acceleration(r_ecef, max_order=360, use_model="EGM96") 
# Query the acceneration at these positions using a maximum degree/order of 360 and the EGM96 Earth gravity model
>>> [[-8.14574564e-03 -2.19120213e-08  3.01312643e-08]
     [-2.25445258e-07 -8.14546631e-03 -1.50901874e-08]]

```

# Source

Right now, the core `gravitas.acceleration` algorithm is based on Pines' method, implemented (and stabalized) by DeMars. The DeMars implementation was translated from MATLAB into ANSI C and is imported as an extension.
