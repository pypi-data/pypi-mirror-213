# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['smart_data_science',
 'smart_data_science.analysis',
 'smart_data_science.cloud',
 'smart_data_science.core',
 'smart_data_science.core.samples_scenario',
 'smart_data_science.dev.modelling.ml_classifier_old_format',
 'smart_data_science.graph_data',
 'smart_data_science.llm',
 'smart_data_science.ml',
 'smart_data_science.nlp',
 'smart_data_science.optimization',
 'smart_data_science.process',
 'smart_data_science.time_series',
 'smart_data_science.ui']

package_data = \
{'': ['*'], 'smart_data_science.core': ['samples_data/*']}

install_requires = \
['chart-studio>=1.1.0',
 'fastapi>=0.93.0',
 'graphviz>=0.20.1',
 'gunicorn>=20.1.0',
 'ipython>=8.10',
 'jupyter-contrib-nbextensions>=0.7.0',
 'jupyter>=1.0.0',
 'langchain>=0.0.186',
 'pandarallel>=1.6.3',
 'pandas>=1.5.0',
 'pandera>=0.13.4',
 'psutil>=5.9.4',
 'py-cpuinfo>=9.0.0',
 'pyarrow>=9.0.0',
 'python-dotenv>=1.0.0',
 'tabulate>=0.9.0',
 'tqdm>=4.64.1',
 'ua-parser>=0.16.1']

extras_require = \
{'full': ['scikit-learn>=1.2.0',
          'lightgbm>=3.3.4',
          'explainerdashboard>=0.4.2.1',
          'flask-simplelogin>=0.1.2',
          'mapie>=0.6.4',
          'shap>=0.41.0',
          'plotly>=5.10.0',
          'openai>=0.27.6',
          'google-cloud-aiplatform>=1.25.0'],
 'full:python_version >= "3.10" and python_version < "3.11"': ['pandas-profiling>=3.4.0'],
 'full:python_version >= "3.10" and python_version < "4.0"': ['streamlit>=1.15.0',
                                                              'sentence-transformers>=2.2.2'],
 'ml': ['scikit-learn>=1.2.0',
        'lightgbm>=3.3.4',
        'xgboost>=1.7.3',
        'scikit-optimize>=0.9.0',
        'explainerdashboard>=0.4.2.1',
        'mapie>=0.6.4',
        'shap>=0.41.0'],
 'plot': ['plotly>=5.10.0', 'matplotlib>=3.6.3', 'seaborn>=0.12.2'],
 'ui:python_version >= "3.10" and python_version < "4.0"': ['streamlit>=1.15.0']}

setup_kwargs = {
    'name': 'smart-data-science',
    'version': '0.1.2',
    'description': 'Personal side project to streamline the most common tasks of data science solutions in an efficient manner. This project is based on my experience as a lead data scientist in the industry and financial services sectors, where I have gained expertise in delivering effective data-driven insights and solutions',
    'long_description': '# smart_data_science\n\nPersonal side project to streamline the most common tasks of data science solutions in an efficient manner. This project is based on my experience as a lead data scientist in the industry and financial services sectors, where I have gained expertise in delivering effective data-driven insights and solutions\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)<br>\n\n## Installation in Dev / Editor mode\n\nNote: A Debian/Ubuntu Machine, VM or container is highly recommended\n\n\n**Step 0: One-time Machine setup only valid for all Data Science Projects**\n\nCreate or use a Machine with Conda, Git and Poetry as closely as defined in `.devcontainer/Dockerfile`:\n\n- This Dockerfile contains a non-root user so the same configuration can be applied to a WSL Ubuntu Machine and any Debian/Ubuntu CLoud Machine (Vertex AI workbench, Azure VM ...)\n- In case of having an Ubuntu/Debian machine with non-root user (e.g.: Ubuntu in WSL, Vertex AI VM ...), just install the tools from  "non-root user" (no sudo) section of the Dockerfile  (sudo apt-get install \\<software\\> may be required)\n- A pre-configured Cloud VM usually has Git and Conda pre-installed, those steps can be skipped\n- The development container defined in `.devcontainer/Dockerfile` can be directly used for a fast setup (Docker required).  With Visual Studio Code, just open the root folder of this repo, press `F1` and select the option **Dev Containers: Open Workspace in Container**. The container will open the same workspace after the Docker Image is built.\n\n\n**Step 1**. Enter to the root path of the repo and use or create a new conda environment for development:\n\n```bash\n$ conda create -n dev python=3.10 -y && conda activate dev\n```\n\n**Step 2**. Install all the Dependencies and the package in editor mode:\n\n```bash\n$ make setup\n```\n\n## Installation for Production/Usage (Not published in PyPi yet)\n```bash\n$ conda create -n smart python=3.10 -y && conda activate smart\n$ pip install dist/smart-data-science-0.1.1-py3-none-any.whl\n```\n\n## Installation for Production/Usage (after the package is published in PyPi)\n\n```bash\n$ pip install smart_data_science\n```\n\n\n## Usage\n\n- Still under development. Please refer to the notebooks and examples folders for usage examples\n\n## Contributing\n\nCheck out the contributing guidelines\n\n## License\n\n`smart_data_science` was created by Angel Martinez-Tenor. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`smart_data_science` was created from a Data Science Template developed by Angel Martinez-Tenor. The template was built upon `py-pkgs-cookiecutter` [template] (https://github.com/py-pkgs/py-pkgs-cookiecutter)\n',
    'author': 'Angel Martinez-Tenor',
    'author_email': 'angelmtenor@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
