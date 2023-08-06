# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['roseingrave']

package_data = \
{'': ['*'], 'roseingrave': ['defaults/*']}

install_requires = \
['cachetools==5.2.0',
 'certifi==2022.6.15',
 'charset-normalizer==2.0.12',
 'click==8.1.3',
 'google-auth-oauthlib==0.5.2',
 'google-auth==2.9.0',
 'gspread==5.5.0',
 'idna==3.3',
 'loguru==0.6.0',
 'oauthlib==3.2.0',
 'pyasn1-modules==0.2.8',
 'pyasn1==0.4.8',
 'requests-oauthlib==1.3.1',
 'requests==2.28.0',
 'rsa==4.8',
 'six==1.16.0',
 'urllib3==1.26.9']

entry_points = \
{'console_scripts': ['roseingrave = roseingrave.__main__:cli']}

setup_kwargs = {
    'name': 'roseingrave',
    'version': '1.1.0',
    'description': 'A massively scalable document source comparator, using Google Spreadsheets API + Python.',
    'long_description': '# Roseingrave\n\nMassively scalable musical source comparator.\n\nSee the\n[documentation](https://github.com/scarlatti/roseingrave/blob/main/Documentation.md)\nfor detailed documentation.\n\n## Installation\n\nInstall the package through pip (recommended to do in a virtual environment):\n\n```bash\n$ python3 -m pip install roseingrave\n```\n\nThe package will be added as a top-level command:\n\n```bash\n$ roseingrave --help\n```\n\nCreate a folder to store all your input/output files. In this folder, place your\nOAuth credentials file (see\n[Credentials](https://github.com/scarlatti/roseingrave#credentials))\nand all required and optional input files.\n\nSee the\n[documentation](https://github.com/scarlatti/roseingrave/blob/main/Documentation.md)\nfor customizing filepaths and the expected input file formats.\n\n## Credentials\n\nThe package interacts with Google Sheets through the\n[`gspread` package](https://docs.gspread.org/en/latest/).\nYou can enable an OAuth Client to create, access, and edit spreadsheets with\nyour email.\n\nTo enable the OAuth Client, follow these steps:\n\n1. Go to the [Google Developers Console](https://console.cloud.google.com/).\n2. Log in with the email account you want to use with the OAuth Client. All\n   created spreadsheets will be owned by this account in Google Drive.\n3. Create a new project.\n4. Go to the [API Library](https://console.cloud.google.com/apis/library).\n5. In the search bar, search for "Google Drive API", select it, and enable it.\n6. Go back to the API library. In the search bar, search for "Google Sheets\n   API", select it, and enable it.\n7. Go to the\n   [OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent)\n   tab.\n8. If prompted, select "External" for the User Type.\n9. On the "App Information" page, enter an app name. Select your email address\n   for the support email. Scroll down to the bottom and enter your email address\n   for the developer contact information. Click "Save and Continue".\n10. On the "Scopes" page, click "Save and Continue".\n11. On the "Test Users" page, add your email address as a user. Click "Save and\n    Continue".\n12. On the summary page, scroll to the bottom and click "Back to Dashboard".\n13. Go to the [Credentials](https://console.cloud.google.com/apis/credentials)\n    tab.\n14. At the top of the page, select "+ Create credentials" > "OAuth client ID".\n15. For the application type, select "Desktop app". Name your credentials.\n    Click "Create". Click "Ok" at the popup.\n16. In the table labeled "OAuth 2.0 Client IDs", locate the credentials you just\n    created. Click the download button at the end of the row.\n17. Rename the file to `credentials.json` and place it in the root directory of\n    where you\'ll be running the commands. (You can customize this in the\n    [settings](https://github.com/scarlatti/roseingrave/blob/main/Documentation.md#settings-optional)\n    file).\n\nIf you\'ve never authorized the app or if your authorization has expired, you\'ll\nbe given a link in the console for you to visit in order to refresh or create\nan authorization token. Go to the url, select your email, click "Continue",\nallow access to your Drive files and Sheets spreadsheets, and click "Continue".\nThis should authenticate you, and the command should continue running.\n\nOnce the authorization is successful, the `authorized_user.json` file will be\ncreated in the same directory as `"credentials"`.\n\n## Basic Usage\n\nCreate the piece definitions and volunteer definitions files as explained in the\n[documentation](https://github.com/scarlatti/roseingrave/blob/main/Documentation.md#input-files).\nIf desired, create the settings file and/or the template file. Save all the\nfiles in the proper locations as defined by the\n[default settings file](https://github.com/scarlatti/roseingrave/blob/main/src/roseingrave/defaults/roseingrave.json)\nor by your own settings file.\n\nBased on your definition files, create the volunteer spreadsheets:\n\n```bash\n$ roseingrave create_sheet\n```\n\nAfter volunteers have filled out their spreadsheets, export the data:\n\n```bash\n$ roseingrave volunteer_summary\n```\n\nExtract the data for each piece:\n\n```bash\n$ roseingrave piece_summary\n```\n\nCompile all the piece data into the summary file:\n\n```bash\n$ roseingrave compile_pieces\n```\n\nCreate the summary spreadsheet with the data from the summary file:\n\n```bash\n$ roseingrave import_summary\n```\n\nFill out the summary columns as appropriate, then export the summary spreadsheet\ninto the summary file:\n\n```bash\n$ roseingrave export_summary\n```\n\nSee the\n[commands documentation](https://github.com/scarlatti/roseingrave/blob/main/Documentation.md#commands)\nfor all commands and their arguments and options.\n',
    'author': 'Joseph Lou',
    'author_email': 'jdlou@princeton.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/scarlatti/roseingrave',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
