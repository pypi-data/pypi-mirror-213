# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['regenbib']

package_data = \
{'': ['*']}

install_requires = \
['arxiv>=1.4.7,<2.0.0',
 'beautifulsoup4>=4.12.2,<5.0.0',
 'bibtex-dblp>=0.9,<0.10',
 'marshmallow-dataclass[enum,union]==8.5.14',
 'requests>=2.29.0,<3.0.0']

entry_points = \
{'console_scripts': ['regenbib = regenbib.cli_render:run',
                     'regenbib-import = regenbib.cli_import:run']}

setup_kwargs = {
    'name': 'regenbib',
    'version': '0.0.5',
    'description': '(Re-)generate tidy .bib files from online sources',
    'long_description': '# regenbib\n\n*(Re-)generate tidy `.bib` files from online sources*\n\n\n## Motivation\n\nThe gist of `regenbib` is as follows.\nInstead of manually maintaining a `references.bib` file with a bunch of entries like this ...\n```bibtex\n@inproceedings{streamlet,\n    author = "Chan, Benjamin Y. and Shi, Elaine",\n    title = "Streamlet: Textbook Streamlined Blockchains",\n    booktitle = "{AFT}",\n    pages = "1--11",\n    publisher = "{ACM}",\n    year = "2020"\n}\n```\n... you should maintain a `references.yaml` file with corresponding entries like that:\n```yaml\nentries:\n- bibtexid: streamlet\n  dblpid: conf/aft/ChanS20\n```\nThe tool `regenbib` can then automatically (re-)generate the `references.bib` from the `references.yaml` in a consistent way by retrieving high-quality metadata information from the corresponding online source (in the example above: [dblp](https://dblp.org/)\'s entry [conf/aft/ChanS20](https://dblp.org/rec/conf/aft/ChanS20.html?view=bibtex&param=0)).\n\nThe tool `regenbib-import` helps to maintain the `references.yaml` file. Using LaTeX\'s `.aux` file, it determines entries that are cited but are currently missing from the `references.yaml` file. It then helps the user determine an appropriate online reference through an interactive lookup right from the command line. In the lookup process, an old (possibly messy) `references.bib` file can be used to obtain starting points for the search (eg, title/author in an old `references.bib` entry can be used to lookup the paper on dblp).\n\nSee the usage example below for details.\n\n\n## Installation\n\nIf your LaTeX project already has a Python virtual environment, activate it.\nOtherwise, setup and activate a virtual environment like this:\n```bash\n$ python -m venv venv\n$ echo "venv/" >> .gitignore\n$ source venv/bin/activate\n```\nThen install `regenbib`:\n```bash\n$ pip install git+https://github.com/joachimneu/regenbib.git\n```\nYou should now have the commands `regenbib` and `regenbib-import` available to you.\n\n\n## Example Usage\n\nSuppose we have an old `references.bib` file with this entry (and suppose it does not have a corresponding entry in our `references.yaml` file):\n```bibtex\n@misc{streamlet,\n  author = {Chan and Shi},\n  title  = {Streamlet Textbook Streamlined Blockchains}\n}\n```\nWe can easily import a corresponding entry to our `references.yaml` file with `regenbib-import`:\n```\n$ regenbib-import --bib references.bib --aux _build/main.aux --yaml references.yaml\nImporting entry: streamlet\n-> Current entry: Entry(\'misc\',\n  fields=[\n    (\'title\', \'Streamlet Textbook Streamlined Blockchains\')],\n  persons=OrderedCaseInsensitiveDict([(\'author\', [Person(\'Chan\'), Person(\'Shi\')])]))\n-> Import method? [0=skip, 1=dblp-free-search, 2=arxiv-manual-id, 3=eprint-manual-id, 4=current-entry, 5=dblp-search-title, 6=dblp-search-authorstitle]: 6\n-----> The search returned 2 matches:\n-----> (1)\tBenjamin Y. Chan, Elaine Shi:\n\t\tStreamlet: Textbook Streamlined Blockchains. AFT 2020\n\t\thttps://doi.org/10.1145/3419614.3423256  https://dblp.org/rec/conf/aft/ChanS20\n-----> (2)\tBenjamin Y. Chan, Elaine Shi:\n\t\tStreamlet: Textbook Streamlined Blockchains. IACR Cryptol. ePrint Arch. (2020) 2020\n\t\thttps://eprint.iacr.org/2020/088  https://dblp.org/rec/journals/iacr/ChanS20\n-----> Intended publication? [0=abort]: 1\n```\nAs you see, `regenbib-import` uses the messy/incomplete information from the old `references.bib` file to help us quickly determine the appropriate dblp entry. This adds the following entry to `references.yaml`:\n```yaml\nentries:\n- bibtexid: streamlet\n  dblpid: conf/aft/ChanS20\n```\nWe can then re-generate a tidy `references.bib` file based on the `references.yaml` file:\n```\n$ regenbib --yaml references.yaml --bib references.bib\nDblpEntry(bibtexid=\'streamlet\', dblpid=\'conf/aft/ChanS20\')\nEntry(\'inproceedings\',\n  fields=[\n    (\'title\', \'Streamlet: Textbook Streamlined Blockchains\'),\n    (\'booktitle\', \'{AFT}\'),\n    (\'pages\', \'1--11\'),\n    (\'publisher\', \'{ACM}\'),\n    (\'year\', \'2020\')],\n  persons=OrderedCaseInsensitiveDict([(\'author\', [Person(\'Chan, Benjamin Y.\'), Person(\'Shi, Elaine\')])]))\n$ cat references.bib\n@inproceedings{streamlet,\n    author = "Chan, Benjamin Y. and Shi, Elaine",\n    title = "Streamlet: Textbook Streamlined Blockchains",\n    booktitle = "{AFT}",\n    pages = "1--11",\n    publisher = "{ACM}",\n    year = "2020"\n}\n```\n\n\n## Supported Entry Types & Online Metadata Sources\n\nSee entry types in `regenbib/store.py`:\n* dblp\n* arXiv\n* IACR ePrint\n* Raw `.bib` entry\n',
    'author': 'Joachim Neu',
    'author_email': 'jneu@stanford.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/joachimneu/regenbib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
