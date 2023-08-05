# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dyndns_updater']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'dnspython>=2.1.0,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'schedule>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['dyndns_updater = dyndns_updater.__main__:main']}

setup_kwargs = {
    'name': 'dyndns-updater',
    'version': '0.2.0',
    'description': 'standalone DNS updater for Gandi',
    'long_description': '# dynDNS_updater\n\n![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/zar3bski/dynDNS_updater/CI/main)\n![PyPI](https://img.shields.io/pypi/v/dynDNS_updater)\n\nstandalone DNS updater for Gandi\n\n\nThe main purpose of **dynDNS_updater** is to keep the DNS records pointing to your servers up to date **without any system dependencies** (except python, of course) nor any fancy web services to identify their public IPv4 / IPv6\n\n## Usage\n\n### Install\n\n```bash\npip install dyndns-updater\n```\n\n### CLI\n\n```\ndyndns_updater {now,scheduled} /path/to/your/conf.yaml\n```\n\nor\n\n```\npython -m  dyndns_updater {now,scheduled} /path/to/your/conf.yaml\n```\n\nMode: \n\n* **now**: perform action once\n* **scheduled**: perform action every `${delta}` seconds (see below)\n\n\n### Configuration\n\n```yaml\nip_identifier: cloudflare\ndelta : 900\ndns_providers: \n  - gandi: GKDNzPZsdHB8vxA56voERCiC\n    somedomain.io:\n      subdomain1: A\n      subdomain2: AAAA\n      subdomain3: AAAA\n```\n\n|    variables    | description                                                                                        |\n| :-------------: | :------------------------------------------------------------------------------------------------- |\n| `ip_identifier` | DNS server used to determine your current IP (currently supporting **cloudflare** and **opendns**) |\n|     `delta`     | How often should dynDNS_updater check and update (in seconds)                                      |\n| `dns_providers` | list of `provider: API-KEY`                                                                        |\n\n\n## Features\n\nTypes of records\n\n* A\n* AAAA\n\n### Supported DNS provider\n\n|      Name | API root                         |\n| --------: | :------------------------------- |\n| **Gandi** | https://api.gandi.net/v5/livedns |\n\n## Developpers \n\nIf your favorite DNS provider is missing from the list, please consider contributing. Your class just needs to inherit from `Updater` and possess the following methods to work in dynDNS_updater\n\n```python\nclass YourProviderUpdater(Updater):\n    def initialize(self):\n        your_logic = "please write unit tests along the way"\n\n    def check_and_update(self):\n        your_logic = "please write unit tests along the way"\n```\n\n### Onboarding\n\n* [poetry](https://python-poetry.org/): dependency manager\n* [black](https://black.readthedocs.io/en/stable/): code formater\n\n```bash\ngit clone https://github.com/zar3bski/dynDNS_updater.git\ncd dynDNS_updater\npoetry install \n```\n\nThis will create a virtual env with all dev dependencies\n\n#### Some usefull commands\n\n* run **unit tests** : `poetry run pytest`\n* add dependencies : `poetry add some-lib`\n\n\n',
    'author': 'David Zarebski',
    'author_email': 'zarebskidavid@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zar3bski/dynDNS_updater',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
