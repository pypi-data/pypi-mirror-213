# adjustpy

a simple utility python module to calculate adjusted p-values.

## Introduction

I was tired to copying over the same function between python scripts so
I decided to write this into a simple utilty you can install via pip.

The computation is done with my [`adjustp`](https://crates.io/crates/adjustp)
rust crate which I created to replicate the same p-value corrections done in R.

## Installation

You can install this python module using pip.

``` bash
pip install adjustpy
```

## Usage

This is a single-function library which expects any dimension numpy arrays.

### 1 Dimensional Input

``` python
import numpy as np
from adjustpy import adjust

p_values = np.array([0.02, 0.05, 0.08, 0.11, 0.04])
q_values = adjust(p_values, method="bh")

# array([0.08333333, 0.08333333, 0.1       , 0.11      , 0.08333333])
print(q_values)
```

### 2 Dimensional Input

This works with multidimensional input as well, but will return a 1D output.
This is easy to work around though as you can just reshape to your original
input shape.

``` python
import numpy as np
from adjustpy import adjust

p_values = np.random.random((10, 10))
q_values_flat = adjust(p_values, method="bh")
q_values = adjust(p_values, method="bh").reshape(p_values.shape)

# (100,)
print(q_values_flat.shape)

# (10, 10)
print(q_values.shape)
```
