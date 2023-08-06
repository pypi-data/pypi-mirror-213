# smart_data_science

Personal side project to streamline the most common tasks of data science solutions in an efficient manner. This project is based on my experience as a lead data scientist in the industry and financial services sectors, where I have gained expertise in delivering effective data-driven insights and solutions

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)<br>

## Installation in Dev / Editor mode

Note: A Debian/Ubuntu Machine, VM or container is highly recommended


**Step 0: One-time Machine setup only valid for all Data Science Projects**

Create or use a Machine with Conda, Git and Poetry as closely as defined in `.devcontainer/Dockerfile`:

- This Dockerfile contains a non-root user so the same configuration can be applied to a WSL Ubuntu Machine and any Debian/Ubuntu CLoud Machine (Vertex AI workbench, Azure VM ...)
- In case of having an Ubuntu/Debian machine with non-root user (e.g.: Ubuntu in WSL, Vertex AI VM ...), just install the tools from  "non-root user" (no sudo) section of the Dockerfile  (sudo apt-get install \<software\> may be required)
- A pre-configured Cloud VM usually has Git and Conda pre-installed, those steps can be skipped
- The development container defined in `.devcontainer/Dockerfile` can be directly used for a fast setup (Docker required).  With Visual Studio Code, just open the root folder of this repo, press `F1` and select the option **Dev Containers: Open Workspace in Container**. The container will open the same workspace after the Docker Image is built.


**Step 1**. Enter to the root path of the repo and use or create a new conda environment for development:

```bash
$ conda create -n dev python=3.10 -y && conda activate dev
```

**Step 2**. Install all the Dependencies and the package in editor mode:

```bash
$ make setup
```

## Installation for Production/Usage (Not published in PyPi yet)
```bash
$ conda create -n smart python=3.10 -y && conda activate smart
$ pip install dist/smart-data-science-0.1.1-py3-none-any.whl
```

## Installation for Production/Usage (after the package is published in PyPi)

```bash
$ pip install smart_data_science
```


## Usage

- Still under development. Please refer to the notebooks and examples folders for usage examples

## Contributing

Check out the contributing guidelines

## License

`smart_data_science` was created by Angel Martinez-Tenor. It is licensed under the terms of the MIT license.

## Credits

`smart_data_science` was created from a Data Science Template developed by Angel Martinez-Tenor. The template was built upon `py-pkgs-cookiecutter` [template] (https://github.com/py-pkgs/py-pkgs-cookiecutter)
