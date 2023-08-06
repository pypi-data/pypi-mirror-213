## Calcul_DuréeDeVie_IGBT

Open-source project for thermal analysis and modeling of power electronic components. This project aims to provide a software platform for performing power loss calculations, estimating component temperatures, and predicting their operational lifetime. It includes features for data retrieval from Excel files, signal processing, power loss calculations, thermal modeling, and cumulative damage analysis. The project utilizes popular libraries such as NumPy, Pandas, SciPy, Matplotlib, and Rainflow for data manipulation, scientific computation, and result visualization.

This project is open to contributions from the open-source community. Feel free to explore the source code, submit issues, propose improvements, and contribute to the project's development.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contribution](#contribution)
- [License](#license)

## Installation
This project comes in the form of a library that needs to be installed in your Python environment. To install the library, simply use the command `pip install PowDeRUL`. Make sure you have the latest version of pip so that the latest dependencies of the library can be installed. The project dependencies are as follows:

- scipy==1.10.1
- pandas==2.0.1
- matplotlib==3.7.1
- numpy==1.24.1
- rainflow==3.2.0
- openpyxl==3.1.2

It is also possible to use the project without installing the library. Please refer to [OLDREADME.md](https://gitlab.com/PGarn/LifeTime_IGBT_Calculation/-/blob/main/OLDREADME.md) if you're interested in that.

## Usage
To use the library, you need two files:
- A dictionary containing all the simulation variables
- The Excel file with the simulation input data
You must adhere to the format, variable names, and internal structure of the files for your project to work smoothly.

An example of each file is available here: [Example Files](https://gitlab.com/PGarn/LifeTime_IGBT_Calculation/-/tree/main/example)

To use the installed library, simply import it into your project with the following line:

`import powderul.lifetime`

Once this module is loaded, you can use the `global_calculation` function by providing the path to your variable dictionary, for example ("C:/Your/path/to/variables.py"). In your code, the function call should look like this:

`results = global_calculation("C:/Your/path/to/variables.py")`

You can also display different graphs using the following function call:

`global_graph("C:/Your/path/to/variables.py")`

## Example
An example of the code in action is detailed in the file [DetailedExample.md](https://gitlab.com/PGarn/LifeTime_IGBT_Calculation/-/blob/main/details/DetailedExample.md)

## Contribution
We welcome all kinds of contributions! To contribute to the project, start by forking the repository, make your proposed changes in a new branch, and create a pull request. Make sure your code is readable and well-documented. Include unit tests if possible.

You can also contribute by submitting bug reports, feature requests, and following the issues.

## License
This project is licensed under the terms of the MIT license. By contributing to the project, you agree that your contributions will be licensed under its MIT license.
