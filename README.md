# Photogrammetry with Neural Network & Image Generation Service

# Installation

- Install anaconda (Python 3.10) from [anaconda](https://www.anaconda.com/distribution/#download-section)

All commands should be run inside the CMD (Command Line) inside the folder of the code.

- Create environment:

```
conda env remove --name catnet
conda create -n catnet python=3.10
```

- Activate environment:

```
conda activate catnet
```

- Install pip:

```
conda install pip
```

- Install dependencies:

```
pip install -r requirements.txt
```

# Running

Run CMD (Win+X and choose Command Line) and CD to the active directory of the project.

Activate your environment:

```
activate catnet
```

Inside the directory execute:

```
jupyter notebook
```

(it should open browser)
and then navigate to **/notebooks** folder.

# Project structure
- **/notebooks** folder consists of notebooks for data analysis / model training / other experiments. 
- **/src** folder consists of the main production code:
    - **/core_features** folder - general collection of basic scripts, files, etc. that are needed for application.
    - **/domain_features** folder - domain features of application such as model classes, services, resources, etc.
- **/tests** folder consists of unit and integration tests for the project.
