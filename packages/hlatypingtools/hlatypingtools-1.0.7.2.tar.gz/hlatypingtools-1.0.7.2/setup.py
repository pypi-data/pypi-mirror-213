# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hlatypingtools']

package_data = \
{'': ['*'], 'hlatypingtools': ['data/data.pickle.aes']}

install_requires = \
['openpyxl>=3.1.2,<4.0.0',
 'pandas-stubs>=2.0.0.230412,<3.0.0.0',
 'pandas>=2.0.0,<3.0.0',
 'pyaescrypt>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'hlatypingtools',
    'version': '1.0.7.2',
    'description': '',
    'long_description': '# HLATypingTools\n\n## Getting Started\n#### Install from PyPI (recommended)\nTo use `HLATypingTools`, run `pip install HLATypingTools` in your terminal.\nAll python packages necessary for `HLATypingTools` will automatically be downloaded.\n\n#### Usage\nIf you haven\'t decrypted the data yet (first time you are using the package and you did request access to the product),\nrun:\n```py\nfrom hlatypingtools.decrypt_file import decrypt_file\n\npassword: str = "___"   # Replace with password provided by the author \ndecrypt_file(password)\n```\nIt should print `File decrypted successfully`.\n\nThen you can use the package as follows:\n```py\nfrom hlatypingtools.get_info import get_allele_info\n\nallele: str = "A*01:01"\nprint(get_allele_info(allele, "Broad"))  # will output A1\nprint(get_allele_info(allele, "G Group"))  # will output A*01:01:01G\nprint(get_allele_info(allele, "P Group"))  # will output A*01:01P\nprint(get_allele_info(allele, "% locus"))  # will output 11.906\n```\n\nOr as follows:\n```py\nfrom hlatypingtools.get_info import get_locus\nprint(get_locus("A*01:01"))  # will output HLA_A\n```\n\nOr as follows to output all possible high-resolution alleles for a given low-resolution typing:\n```py\nfrom hlatypingtools.get_info import get_same_low_res_broad, get_same_low_res_assigned_type\nbroad = "DQ3"\nprint("DQB1*03:01" in get_same_low_res_broad(broad))  # will output True\nprint("DQB1*03:02" in get_same_low_res_broad(broad))  # will output True\n\nassigned_type = "DQ7"\nprint("DQB1*03:01" in get_same_low_res_assigned_type(assigned_type))  # will output True\nprint("DQB1*03:02" in get_same_low_res_assigned_type(assigned_type))  # will output False\n```\nNote:\n- Broad = something like A1, B7, Cw1, DR1, **DQ3** (!!!), DQA1&ast;01, DR52, DPB1&ast;01, or DPA1&ast;01\n- Assigned Type = something like A1, B7, Cw1, DR1, **DQ7** (!!!), DQA1&ast;01, DR52, DPB1&ast;01, or DPA1&ast;01\n\n#### Exit codes\n```\n0: Wrong password.\n1: Tried to acess the functions of the package without decrypting the data first.\n2: type_info requested is not available.\n3: wrong format for a low-resolution input. Has to be of the form A1, B7, Cw1, DR1, DQ3, DQA1*01, DR52, DPB1*01, or \nDPA1*01.\n```\n\n## About the source code\n- Follows [PEP8](https://peps.python.org/pep-0008/) Style Guidelines.\n- All functions are unit-tested with [pytest](https://docs.pytest.org/en/stable/).\n- All variables are correctly type-hinted, reviewed with [static type checker](https://mypy.readthedocs.io/en/stable/)\n`mypy`.\n- All functions are documented with [docstrings](https://www.python.org/dev/peps/pep-0257/).\n\n\n## Useful links:\n- [Corresponding GitHub repository](https://github.com/JasonMendoza2008/HLATypingTools)\n- [Corresponding PyPI page](https://pypi.org/project/HLATypingTools)\n',
    'author': 'JasonMendoza2008',
    'author_email': 'lhotteromain@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
