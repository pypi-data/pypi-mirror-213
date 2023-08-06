# Description
Python implementation of model-based image coregistration 
for quantitative medical imaging applications. 

The distribution comes with a number of common signal models and uses [ITK-Elastix](https://github.com/InsightSoftwareConsortium/ITKElastix) for deformable image registration.

***CAUTION: mdreg is developed in public but is work in progress and backwards compatibility is not guaranteed. It is likely there WILL be breaking changes in future versions***

## Installation
Run `pip install mdreg`. 

## Example data
Example data in [DICOM format](https://shorturl.at/rwCUV) are provided for testing the setup.

## How to run
Input data must be image arrays in numpy format, with dimensions `(x,y,z,t)` or `(x,y,t)`. 
To perform MDR on an image array `im` with default settings do: 

```python
from mdreg import MDReg

mdr = MDReg()
mdr.set_array(im)
mdr.fit()
```

These default settings will apply a linear signal model and coregistration 
as defined in the elastix parameter file `Bsplines.txt`. 

## Outputs
When fitting is complete the following data are available:

- `mdr.coreg`: motion-corrected data are in the same dimensions as the original `im`. 
- `mdr.deformation`: the calculated deformation fields in format `(x,y,d,t)` or `(x,y,z,d,t)`. The dimension `d` holds `x`, `y` components of the deformation field. The third `z` component exists if the input array is 3D. 
- `mdr.fit`: the model fit to the coregistered images in the same dimensions `(x,y,z,t)` or `(x,y,t)` as the original `im`. 
- `mdr.par`: the fitted parameters are in dimensions `(x,z,p)` or `(x,y,z,p)` (for 3D data), where `p` enumerates the model parameters.

# Customization

MDR can be configured to apply different signal models and elastix coregistration settings.
A number of example models and alternative elastix parameter files are included 
in the distribution as templates.

The following example fits a mono-exponential decay, uses a mask `im_mask` for co-registration and applies an elastix parameter file `par_file` optimized for a previous DTI-MRI study:

```python
from mdreg import MDReg
from mdreg.models import exponential_decay

mdr = MDReg()
mdr.set_array(im)
mdr.set_mask(im_mask)
mdr.signal_model = exponential_decay
mdr.read_elastix(par_file)
mdr.fit()
```

`im_mask` must be a binary (0's and 1's) or boolean (True's and False's) image array in numpy format with the same dimensions as `im`.

The signal model often depends on fixed constants and signal parameters 
such as sequence parameters in MRI, or patient-specific constants. These 
should all be grouped in a list and set before running the signal model. 

Equally elastix parameters can be fine tuned, either by importing a 
dedicated elastix file, or by modifying the settings. 

You may also choose if you wish to run the process in multiple cores (`parallel`) and to print the co-registration progress to the terminal plus a text file (`log`) or not.

Then, a number of parameters are available to optimize MDR such as 
the precision (stopping criterion) and maximum number of iterations.

Some examples:

```python
from mdreg import MDReg
from mdreg.models import exponential_decay

t = [0.0, 1.25, 2.50, 3.75]     # time points for exponential in sec

mdr = MDReg()
mdr.set_array(im)
mdr.signal_parameters = t
mdr.signal_model = exponential_decay
mdr.set_elastix(MaximumNumberOfIterations = 256)   # change defaults
mdr.precision = 0.5         # default = 1
mdr.max_iterations = 3      # default = 5
mdr.parallel = False        # default = True
mdr.log = True              # default = False
mdr.fit()
```

`mdreg` comes with a number of options to 
export results and diagnostics:

```python
mdr.export_unregistered = True      # export parameters and fit without registration
mdr.export_path = filepath          # default is a results folder in the current working directory
mdr.export()                        # export results after calling fit. 
```

This export creates movies of original images, motion corrected images, 
modelfits, and maps of the fitted parameters.

# Model fitting without motion correction

`MDReg` also can be used to perform model fitting 
without correcting the motion. The following script 
fits a linearised exponential model to each pixel and exports data 
of model and fit:

```python
from mdreg import MDReg
from mdreg.models import exponential_decay

mdr = MDReg()
mdr.set_array(im)
mdr.signal_model = linear_exponential_decay
mdr.fit_signal()
mdr.export_data()
mdr.export_fit()
```

# Defining new MDR models

A model must be defined as a separate module or class with two required functions `main()` and `pars()`.

`pars()` must return a list of strings specifying the names of the model parameters.
`main(im, const)` performs the pixel based model fitting and has two required arguments. 
`im` is a numpy ndarray with dimensions `(x,y,z,t)`, `(x,y,t)` or `(x,t)`. `const` is a list 
of any constant model parameters.

The function must return the fit to the model as an numpy ndarray with the same dimensions 
as `im`, and an ndarray `pars` with dimensions `(x,y,z,p)`, `(x,y,p)` or `(x,p)`. Here `p` enumerates 
the model parameters. 

## Context

`mdreg` was first developed for use in quantitative renal MRI in the iBEAt study, 
and validated against group-wise model-free registration 
(Tagkalakis F, et al. Model-based motion correction outperforms a model-free method in quantitative renal MRI. Abstract-1383, ISMRM 2021).

## Acknowledgement

The iBEAt study is part of the BEAt-DKD project. The BEAt-DKD project has received funding from the Innovative Medicines Initiative 2 Joint Undertaking under grant agreement No 115974. This Joint Undertaking receives support from the European Union’s Horizon 2020 research and innovation programme and EFPIA with JDRF. For a full list of BEAt-DKD partners, see www.beat-dkd.eu.

## Authors

Kanishka Sharma, Joao Almeida e Sousa, Steven Sourbron
