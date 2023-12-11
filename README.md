# `globITFPhysGENIE`: Role of Indonesian Archipelago on Global Thermohaline Circulation: Insights from Numerical Experiments

[![DOI](https://zenodo.org/badge/671343723.svg)](https://zenodo.org/badge/latestdoi/671343723)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![GitHub watchers](https://img.shields.io/github/watchers/Naereen/StrapDown.js.svg?style=social&label=Watch&maxAge=2592000)](https://github.com/sandyherho/globITFPhysGENIE/watchers)
[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

[![python](https://img.shields.io/badge/python-★★★-lightgrey?labelColor=3776AB&logo=Python&style=for-the-badge&logoColor=white)](https://www.python.org/)
![Overleaf](https://img.shields.io/badge/-Overleaf-47A141?logo=Overleaf&style=for-the-badge&logoColor=white)


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

## Acknowledgements
We express profound gratitude to Andrew J. Ridgwell for enriching discussions and invaluable guidance in refining the numerical experiment setup. This study received financial support from the Dean's Distinguished Fellowship at the University of California, Riverside, and the ITB Research, Community Service, and Innovation Program (PPMI-ITB).  
