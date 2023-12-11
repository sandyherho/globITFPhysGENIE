# `globITFPhysGENIE`: Role of Indonesian Archipelago on Global Thermohaline Circulation: Insights from Numerical Experiments


[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![GitHub watchers](https://img.shields.io/github/watchers/Naereen/StrapDown.js.svg?style=social&label=Watch&maxAge=2592000)](https://github.com/sandyherho/globITFPhysGENIE/watchers)
[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

![latex](https://img.shields.io/badge/LaTeX-47A141?style=for-the-badge&logo=LaTeX&logoColor=white)
![Overleaf](https://img.shields.io/badge/-Overleaf-47A141?logo=Overleaf&style=for-the-badge&logoColor=white)

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![numpy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![SCIPY](https://img.shields.io/badge/SciPy-654FF0?style=for-the-badge&logo=SciPy&logoColor=white)

![Arch](https://img.shields.io/badge/Arch_Linux-1793D1?style=for-the-badge&logo=arch-linux&logoColor=white)
![sublime](https://img.shields.io/badge/sublime_text-%23575757.svg?&style=for-the-badge&logo=sublime-text&logoColor=important)


![CentOS](https://img.shields.io/badge/Cent%20OS-262577?style=for-the-badge&logo=CentOS&logoColor=white)
![vim](https://img.shields.io/badge/VIM-%2311AB00.svg?&style=for-the-badge&logo=vim&logoColor=white)



This repository contains the code associated with the study employing the cGENIE Earth System Model to investigate the effects of the Indonesian Throughflow (ITF) and Indonesian Archipelago (IA) closure on global meridional thermohaline circulation (THC). The study spans a simulated period of 10,000 years, focusing on critical variables such as surface density, vertical density profiles, global overturning circulation, and ocean ventilation age.



The following are the individuals involved in this project: [S. H. S. Herho](https://scholar.google.com/citations?user=uYQgjxMAAAAJ&hl=id), [I. P. Anwar](https://scholar.google.co.id/citations?user=NMs_TswAAAAJ&hl=id), [R. D. Susanto](https://scholar.google.com/citations?user=xony5H4AAAAJ&hl=en), [G. A. Firdaus](https://www.linkedin.com/in/gisma2/?originalSubdomain=id), [D. E. Irawan](https://scholar.google.com/citations?user=Myvc78MAAAAJ&hl=en), and [R. Kapid](https://scholar.google.co.id/citations?user=oArSkkYAAAAJ&hl=en).

## License
These data and code were released under the [GPL-3.0 License](https://github.com/sandyherho/globITFPhysGENIE/blob/main/LICENSE.txt).

## Citation
If you find these data useful, please  consider citing our paper:


`
@article{herhoEtAl24a_itf,
         author={Herho, S. H. S. and Anwar, I. A. and Firdaus, G. A. and Susanto, R. D. and Irawan, D. E. and Kapid, R.},
         title={Role of Indonesian Archipelago on Global Thermohaline Circulation: Insights from Numerical Experiments},
         journal={xxxxx},
         year={2024},
         volume={x},
         number={x},
         pages={x - x},
         doi={xx}
}
`

## Requirements

### Numerical Experiments
cGENIE muffin version can be obtained from [here](https://github.com/derpycode/cgenie.muffin). Meanwhile muffingen can be obtained from [here](https://zenodo.org/records/4615664). The baseconfigs and userconfigs used in this experiment can be seen [here](https://github.com/sandyherho/globITFPhysGENIE/tree/main/configs). For installation and running the model, you can follow the instructions from [Ridgwell et al. (2018)](https://zenodo.org/records/1407658).

### Data Analysis
We analyzed the data under the [Python 3](https://www.python.org/) computing environment by using the following libraries:

- [cmocean](https://matplotlib.org/cmocean/)
- [Matplotlib](https://matplotlib.org/)
- [NumPy](https://numpy.org/)
- [SciPy](https://pandas.pydata.org/)
- [seaborn](https://seaborn.pydata.org/)
- [xarray](https://docs.xarray.dev/en/stable/)

The computing environment can be reproduced by running the following command:

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

or as follows (for Anaconda users):

```bash
conda env create -f environment.yml
conda activate globITFPhysGENIE
```

## Hardware Specifications
We conducted numerical experiments on the sterling.ucr.edu server, which possesses the following specifications:

- Operating System: CentOS Linux release 7.4.1708 (Core)
- CPU Model: Intel(R) Xeon(R) CPU E5-2637 v4 @ 3.50GHz - 16 CPU(s)

This server was graciously provided by the [Department of Earth and Planetary Sciences](https://epsci.ucr.edu/) at the [University of California, Riverside](https://www.ucr.edu/).

Simultaneously, the analysis of the model output data was performed on a personal computer with the following configuration:

- Operating System: ArchLinux 6.1.58-1-lts (kernel)
- CPU Model: Intel i7-5600U (4) @ 3,200GHz

## Acknowledgements
We express profound gratitude to Andrew J. Ridgwell for enriching discussions and invaluable guidance in refining the numerical experiment setup. This study received financial support from the Dean's Distinguished Fellowship at the University of California, Riverside, and the ITB Research, Community Service, and Innovation Program (PPMI-ITB).  
