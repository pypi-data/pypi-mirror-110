# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pmcli']
install_requires = \
['click>=8.0.1,<9.0.0', 'cryptocode>=0.1,<0.2']

entry_points = \
{'console_scripts': ['pm = pmcli:main']}

setup_kwargs = {
    'name': 'pmcli',
    'version': '0.2.1',
    'description': 'A Command Line Interface to encrypt, decrypt and save passwords dor windows',
    'long_description': "# PMCLI\n\n## A password encrypter and decrypter\n\nHave important passwords to store? Use pmcli to encrypt your passwords into files and decrypt them whenever you want!\n\n## Install\n\n```\npip3 install pmcli \n```\n\n## How to use\n\nOpen powershell for Windows or Terminal for Linux/Mac and  and type ```pm```\n\nIf this result comes, then you have successfully installed pmcli on your system\n\n```\n  PM: Encrypt, decrypt and save your passwords\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  clear     Clear existing data\n  config    Set your configuration for pm\n  decrypt   Decrypt any of your passwords\n  decryptf  Decrypt all your passwords\n  encrypt   Encrypt your message\n  init      Initialize pmcli for you to get started with it\n```\n\nelse, try the above steps again!\n\n#### Setup\n\nFirst you need to setup pm for yourself\n\nProcedure:\n\n- Run `pm init` to initialize pm for your directory\n\nThere should be no output\n\n- Run `pm config -ps <password>` to set your password for PM. It will ask you for your OLD PASSWORD\n  - Now if you haven't configured your passowrd before, enter `fetcher` in the OLD PASSWORD INPUT which is the default password\n\n**NOTE: THIS STORES YOUR PASSWORD FOR PM AND DOES NOT INDICATE A PASSWORD FOR PASSWORD MANAGEMENT**\n\n- Now you are set up to use PM\n\n##### Encryption:\n\n```\npm encrypt {directory} {note(optional)}\n```\n\nFor example:\n\n```\npm encrypt C://Users//doge//Desktop//Office//files 'Welcome982' -n google\n```\n\nThis makes a data_encr.dat file which consists the message 'Hello World' in the files folder located in Office folder present in your Desktop.\n\nFor using current directory, just provide `current` instead of the directory.\n\nIn the above example, 'google' is an ID that gives the encrypted data and identity.\n\nYou can even use `--note` instead of `-n` to add an ID\n\nGiving an ID is completely optional, but highly recommended for every user. This helps you decrypt your messages easily\n\n##### Decryption\n\nThere are two methods of decrypting/obtaining your passwords\n\n###### SPECIFIC DECRYPTION\n\n```\npm decrypt {directory} -n {note}\n```\n\nFor example:\n\n```\npm decrypt C://Users//arghy//Desktop//Office//files -n google\n```\n\nThis gives you the stored password identified by `google` NOTE/ID.\n\nFor using current directory, just provide `current` instead of the directory.\n\n###### MASS DECRYPTION\n\n```\npm decryptf {directory} \n```\n\nThis gives you all of your stored passwords\n\n```\npm decryptf C://Users//arghy//Desktop//Office//files\n```\n\n**NOTE: EVERY DECRYPTION METHOD NEEDS YOUT PM PASSWORD, HENCE IF YOU HAVE NOT SETUP YOUR PM, DECRYPTION WONT WORK**\n\n##### CLEAR\n\n`pm clear {directory}` cleans the data from data file\n\n### Developer Tools\n\n[Visual Studio Code](https://github.com/microsoft/vscode)\n\n[Python 3.9.5](https://python.org)\n\n[Git](https://git-scm.com)\n",
    'author': 'Avanindra Chakraborty',
    'author_email': 'avanindra.d2.chakraborty@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AvanindraC/PMCLI',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
