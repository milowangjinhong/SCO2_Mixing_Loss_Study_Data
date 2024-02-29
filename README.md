# Non-ideal Fluid Mixing Study for $\textrm{sCO}_2$

## Description

This is a repository created for non-ideal fluid mixing study for $\textrm{sCO}_2$. It includes the data for the paper *Supercritical Carbon Dioxide Mixing Loss Characteristics Near the Critical Point (under review)*. The data was generated using [CoolProp](https://github.com/CoolProp/CoolProp) library.

- Data were saved in **.txt** files in [*Result_Data*](Result_Data) directory. Please check out our paper for detailed data generation methods.
- Python functions for data loading and saving are included in [*data_process_functions.py*](data_process_functions.py).

## Requirements

This module only requries [NumPy](https://numpy.org/) for array calculations.

## Studied Cases

Please read our paper (under review) for details in the calculation case information.

## Data Structure

The data saving and reading are carried out using **numpy.savetxt()** and **numpy.loadtxt()** methods from [NumPy](https://numpy.org/). Two types of data are included in this repository, 1D and 3D data.

### 1D Data

#### Data Information

1D data are stored in directory [*Result_Data/1DOF*](Result_Data/1DOF) and were used to carry out 1DOF investigations. The *dT*, *dU*, *dP* in the file name indicates the variable that is changed in the study. The number in the file name is the average static temperature used for this calculation.

In each 1D file, the following information are stored:

| Row No.     | Description                   |
| -----       | -----------                   |
| 1           | Data info and notes           |
| 3           | x values                      |
| 5           | Number of y value arrays      |
| 6 - End     | Each row is a set of y value  |

In this study, X values are the non-dimensional property difference values for the specific 1DOF study ($\widetilde{\Delta T}$, $\widetilde{\Delta U}$, or $\widetilde{\Delta P}$). Six y arrays are included in the results: the first 5 are the corresponding mixing loss for different average specific entropy cases. The sixth set of y value are the corresponding perfect gas calculation for $\textrm{CO}_2$ when $\gamma=1.37$. 

#### Data Loading

1D data can be loaded using the **reading_XY()** function in [*data_process_functions.py*](data_process_functions.py). 

```python
x, y_list = reading_XY('Result_Data/1DOF/dT_305.00.txt')
```

By executing the code above, **x** will be loaded with the x-coordinate of the text file, and **y_list** will be loaded with a list of corresponding y values for plotting.

### 3D Data

#### Data Information

3D data are stored in directories with two numbers in [*Result_Data*](Result_Data), which indicates the average static states of the calculation. The first value is the average static temperature and the second is the average specific entropy.

In each subfolder, results are saved in different slicing directions: P-U, Y-P, and T-U. The *real* labels in the file names indicate that the results are non-ideal fluid calculations and the *ideal* labels are the perfect gas results. Since there is only 1 perfect gas calculation for each average static temperature, they are only storied in folder with $S_{avg}=1425$ $\textrm{JK}^{-1}\textrm{kg}^{-1}$.

In each data file, the data are structured slightly differently:

| Row No.     | Description                     |
| -----       | -----------                     |
| 1           | Array shape stored in this file (Nx, Ny, Nz) |
| 3           | x values                        |
| 5           | y values                        |
| 7           | z values                        |
| 8 - End     | z value title followed by the matrix slice in z direction|

#### Data Loading

3D data can be loaded using the **reading_3D_array()** function in [*data_process_functions.py*](data_process_functions.py). 

```python
X, Y, Z, result = reading_3D_array('Result_Data/305.00-1300.00/305.00-1300.00-realTU.txt')
```

The returned values **X, Y, Z, result** are 3-dimensional Numpy arrays with dimension (Nx, Ny, Nz). **X, Y, Z** are generated using **numpy.meshgrid()** method using x,y,z values read from $3^{\textrm{rd}}$, $5^{\textrm{th}}$, and $7^{\textrm{th}}$ row of the data file and **result** is the corresponding mixing loss coefficient.

#### 3D Data Transformation

The default assignment of **X, Y, Z** are 

- **X** - Temperature difference $\widetilde{\Delta T}$
- **Y** - Velocity difference $\widetilde{\Delta U}$
- **Z** - Pressure difference $\widetilde{\Delta P}$

The transformation of data can be achieved using **XYZ_transfomration**

```python
X_new, Y_new, Z_new, res_list_new = XYZ_transfomration(X, Y, Z, res_list, out = 'XZY')
```

so that the assignment of **X_new, Y_new, Z_new** can be updated using the specified argument **out**.

If there are 3 x-values, 4 y-values, and 5 z-values, the original array dimensions produced by **numpy.meshgrid()** is (4,3,5). The possible returned shape of **X_new, Y_new, Z_new**, and arrays in **res_list_new** given different **out** are listed below:

| **out**     | Output Array Shape  |
| -----       | -----------         |
| 'XYZ'       | (4,3,5) (unchanged) |
| 'XZY'       | (5,3,4)             |
| 'YZX'       | (5,4,3)             |
| 'YXZ'       | (3,4,5)             |
| 'ZXY'       | (3,5,4)             |
| 'ZYX'       | (4,5,3)             |



## Reference

J Wang, T Cao, R Martinez-Botas (2024) *Supercritical Carbon Dioxide Mixing Loss Characteristics Near the Critical Point* (under-review), Department of Mechanical Engineering, Imperial College London


## Maintainers

Please use the Discussions section to add any comments and feedback. Useful feedback is always appreciated.
