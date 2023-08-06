# RBasisPy
***
**RBasisPy** is a library that allows you to implement a Radial Basis Network in Python. This library has 3 radial basis function that can be use in the hidden layer of the network.

## How to install RBasisPy?
It can be installed from terminal using pip: `pip install RBasisPy`

## License
License for **RBasisPy** is [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html).
***
# RBasisPy documentation
Once the library is installed, it is necessary to call the network module: `from RBasisPy import rbn`, rbn is the Radial Basis Network and can be instaced with two parameters: `K` and `f`, `K` means numbers of units in the hidden layer and `f` the radial basis function.

***Parameters***
 - **K:** `numbers of units in the hidden layer.`
 - **f:** `{'gaussian', 'inv_sqr', 'inv_mul'} default='gaussian'`
		'gaussian': Gaussian function.
		'inv_sqr': Inverse Quadratic function.
		'inv_mul': Inverse Multiquadratic function.

***Methods***

 - **fit(X, y):** fit the model, X: input data with shape (number of samples, number of features). Y: target vector with shape(n_samples).
 - **predict(X)**: predict X using the RBN. 

***Contact***

 - E-mail: michael.guzman.personal@gmail.com
 - LinkedIn: [Click here](https://www.linkedin.com/in/dguzmanmichael/)
