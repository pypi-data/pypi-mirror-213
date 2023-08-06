# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['i_xero2']

package_data = \
{'': ['*']}

install_requires = \
['aracnid-logger>=1.0,<2.0',
 'flask-oauthlib>=0.9,<0.10',
 'flask-session>=0.4,<0.5',
 'flask>=2.1,<3.0',
 'i-mongodb>=2.0,<3.0',
 'pytz>=2022.1,<2023.0',
 'xero-python>=1.16,<2.0']

setup_kwargs = {
    'name': 'i-xero2',
    'version': '2.7.0',
    'description': 'Custom connector to Xero',
    'long_description': '# i-Xero2\n\nThis is a standardized and customized connector to Xero.\n\n## Getting Started\n\nThese instructions will get you a copy of the project up and running on your local machine for development and testing purposes.\n\n### Prerequisites\n\nThis package supports the following version of Python. It probably supports older versions, but they have not been tested.\n\n- Python 3.10 or later\n\n### Installing\n\nInstall the latest package using pip.\n\n```bash\n$ pip install i-xero2\n```\n\nEnd with an example of getting some data out of the system or using it for a little demo\n\n## Running the tests\n\nBefore running the tests, you need to authorize the app with Xero and save the tenant ID in the environment.\n\n1. In Xero, switch to the "Demo Company".\n1. Run the app locally.\n\n    ```bash\n    $ python app.py\n    ```\n\n1. In the browser, navigate to `http://localhost:5000/`\n1. Follow the prompts to allow app to access Xero.\n1. Read tenants.\n1. Copy the `tenantId`.\n1. Save the tenant id as an environment variable named `XERO_TENANT_ID`.\n1. Run the tests.\n\n    ```bash\n    $ python -m pytest\n    ```\n\n## Usage\n\nTODO\n\n## Authors\n\n- **Jason Romano** - [Aracnid](https://github.com/aracnid)\n\nSee also the list of [contributors](https://github.com/aracnid/i-xero2/contributors) who participated in this project.\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n',
    'author': 'Jason Romano',
    'author_email': 'aracnid@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aracnid/i-xero2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
