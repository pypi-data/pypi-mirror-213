# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['p360_export',
 'p360_export.config',
 'p360_export.containers',
 'p360_export.data',
 'p360_export.data.build',
 'p360_export.data.extra',
 'p360_export.data.fix',
 'p360_export.data.type.resolve',
 'p360_export.data.type.validate',
 'p360_export.exceptions',
 'p360_export.export',
 'p360_export.export.facebook',
 'p360_export.export.google.ads',
 'p360_export.export.google.ga4',
 'p360_export.export.sfmc',
 'p360_export.query',
 'p360_export.test',
 'p360_export.utils',
 'p360_export.utils.secret_getters']

package_data = \
{'': ['*'], 'p360_export': ['_config/*']}

install_requires = \
['Salesforce-FuelSDK-Sans>=1.3.0,<2.0.0',
 'dependency-injector>=4.40.0,<5.0.0',
 'facebook-business>=13.0.0,<14.0.0',
 'google-ads>=16.0.0,<17.0.0',
 'ipython>=8.7.0,<9.0.0',
 'jsonschema>=4.4.0,<5.0.0',
 'pandas>=1.5.2,<2.0.0',
 'paramiko>=2.11.0,<3.0.0',
 'pyarrow>=10.0.1,<11.0.0']

setup_kwargs = {
    'name': 'p360-export',
    'version': '1.5.5',
    'description': 'Persona360 data export',
    'long_description': "# p360-export\n\nPersona360 exporters.\n\n### Latest Changes\n* :sparkles: Added Google Analytics 4 exporter. PR [#82](https://github.com/DataSentics/p360-export/pull/82) by [@guderkar](https://github.com/guderkar).\n#### 1.4.0\n* :construction_worker: Fixed release workflow PR [#81](https://github.com/DataSentics/p360-export/pull/81) by [@Vinsho](https://github.com/Vinsho).\n* :recycle: Typo fix. PR [#79](https://github.com/DataSentics/p360-export/pull/79) by [@Vinsho](https://github.com/Vinsho).\n* :sparkles: Fixed backward compatibility. PR [#77](https://github.com/DataSentics/p360-export/pull/77) by [@Vinsho](https://github.com/Vinsho).\n* :sparkles: Added logic for loading env specific config. PR [#76](https://github.com/DataSentics/p360-export/pull/76) by [@Vinsho](https://github.com/Vinsho).\n* :recycle: Odap integration. PR [#75](https://github.com/DataSentics/p360-export/pull/75) by [@Vinsho](https://github.com/Vinsho).\n* :art: Replaced pyfony with dependency-injector PR [#74](https://github.com/DataSentics/p360-export/pull/74) by [@Vinsho](https://github.com/Vinsho)\n#### 1.3.1\n* :bug: Don't fail on empty columns, don't send them to SFMC. PR [#72](https://github.com/DataSentics/p360-export/pull/72) by [@Vinsho](https://github.com/Vinsho).\n* :sparkles: Added SFMC Field Name Fixer. PR [#71](https://github.com/DataSentics/p360-export/pull/71) by [@Vinsho](https://github.com/Vinsho).\n* :bug: Fixed missing _ in less than and greater than. PR [#70](https://github.com/DataSentics/p360-export/pull/70) by [@Vinsho](https://github.com/Vinsho).\n#### 1.3.0\n* :recycle: Target user_list by export_id. PR [#68](https://github.com/DataSentics/p360-export/pull/68) by [@Vinsho](https://github.com/Vinsho).\n* :recycle: Google ads export send User ID instead of email. PR [#67](https://github.com/DataSentics/p360-export/pull/67) by [@Vinsho](https://github.com/Vinsho).\n* :recycle: Target audience based on its id part. PR [#66](https://github.com/DataSentics/p360-export/pull/66) by [@Vinsho](https://github.com/Vinsho).\n* :sparkles: Work with SFMC Customer Keys. PR [#65](https://github.com/DataSentics/p360-export/pull/65) by [@Vinsho](https://github.com/Vinsho).\n#### 1.2.1\n* :technologist: Replace asserts with native unittest assertions. PR [#63](https://github.com/DataSentics/p360-export/pull/63) by [@Vinsho](https://github.com/Vinsho).\n* :sparkles: Added not_equals to QueryBuilder. PR [#62](https://github.com/DataSentics/p360-export/pull/62) by [@Vinsho](https://github.com/Vinsho).\n* :bug: Fixed query equals with multiple values. PR [#61](https://github.com/DataSentics/p360-export/pull/61) by [@Vinsho](https://github.com/Vinsho).\n* :bug: Fixed attributes only export. PR [#60](https://github.com/DataSentics/p360-export/pull/60) by [@Vinsho](https://github.com/Vinsho).\n#### 1.2.0\n* :arrow_up: Feature store bundle upgrade to 2.7.1. PR [#57](https://github.com/DataSentics/p360-export/pull/57) by [@Vinsho](https://github.com/Vinsho).\n* :sparkles: Enabled export without segment. PR [#56](https://github.com/DataSentics/p360-export/pull/56) by [@Vinsho](https://github.com/Vinsho).\n* :recycle: Persona renamed to Segment. PR [#55](https://github.com/DataSentics/p360-export/pull/55) by [@Vinsho](https://github.com/Vinsho).\n* :boom: Config is recieved as argument in runner. PR [#53](https://github.com/DataSentics/p360-export/pull/53) by [@Vinsho](https://github.com/Vinsho).\n* :arrow_up: pyre-check-nightly replaced by pyre-check. PR [#54](https://github.com/DataSentics/p360-export/pull/54) by [@Vinsho](https://github.com/Vinsho).\n#### 1.1.0\n* :recycle: SFMC Exporter refactor. PR [#46](https://github.com/DataSentics/p360-export/pull/46) by [@Vinsho](https://github.com/Vinsho).\n* :recycle: QueryBuilder and ExportManager refactor. PR [#49](https://github.com/DataSentics/p360-export/pull/49) by [@Vinsho](https://github.com/Vinsho).\n* :recycle: ColumnSampleGetter turned to service. PR [#47](https://github.com/DataSentics/p360-export/pull/47) by [@Vinsho](https://github.com/Vinsho).\n* :arrow_up: Unpin the fixed feature-store-bundle version. PR [#48](https://github.com/DataSentics/p360-export/pull/48) by [@Vinsho](https://github.com/Vinsho).\n* :recycle: Google Ads Exporter Refactor. PR [#44](https://github.com/DataSentics/p360-export/pull/44) by [@Vinsho](https://github.com/Vinsho).\n* ♻️ TypeGuesser component refactor. PR [#35](https://github.com/DataSentics/p360-export/pull/35) by [@Vinsho](https://github.com/Vinsho).\n* :recycle: Facebook Exporter refactor. PR [#43](https://github.com/DataSentics/p360-export/pull/43) by [@Vinsho](https://github.com/Vinsho).\n* :recycle: Data Picker components refactor. PR [#40](https://github.com/DataSentics/p360-export/pull/40) by [@Vinsho](https://github.com/Vinsho).\n* :green_heart: Fixed failing pylint tests. PR [#42](https://github.com/DataSentics/p360-export/pull/42) by [@Vinsho](https://github.com/Vinsho).\n* :technologist: Alter pylint to pyfony coding style. PR [#41](https://github.com/DataSentics/p360-export/pull/41) by [@Vinsho](https://github.com/Vinsho).\n\n#### 1.0.2\n* :arrow_up: Feature store bundle update to 2.5.1. PR [#36](https://github.com/DataSentics/p360-export/pull/36) by [@matejoravec](https://github.com/matejoravec).\n* :construction_worker: Release pipeline customized. PR [#34](https://github.com/DataSentics/p360-export/pull/34) by [@matejoravec](https://github.com/matejoravec).\n\n#### 1.0.1\n* :memo: Missing emojis added to README. PR [#31](https://github.com/DataSentics/p360-export/pull/31) by [@matejoravec](https://github.com/matejoravec).\n* :arrow_up: feature-store-bundle 2.5.0b2 -> 2.5.0b3. PR [#30](https://github.com/DataSentics/p360-export/pull/30) by [@Vinsho](https://github.com/Vinsho).\n* :sparkles: Make created Data Extension sendable. PR [#29](https://github.com/DataSentics/p360-export/pull/29) by [@Vinsho](https://github.com/Vinsho).\n* :bug: Fixed Type Guesser bugs. PR [#28](https://github.com/DataSentics/p360-export/pull/28) by [@Vinsho](https://github.com/Vinsho).\n* :sparkles: Added Type Guesser. PR [#27](https://github.com/DataSentics/p360-export/pull/27) by [@Vinsho](https://github.com/Vinsho).\n* :building_construction: Retrieval of redundant attributes removed. PR [#26](https://github.com/DataSentics/p360-export/pull/26) by [@matejoravec](https://github.com/matejoravec).\n* :sparkles: SFMC Exporter: Enable field updating. PR [#23](https://github.com/DataSentics/p360-export/pull/23) by [@Vinsho](https://github.com/Vinsho).\n* :construction_worker: Build & Release Pipeline outsourced. PR [#25](https://github.com/DataSentics/p360-export/pull/25) by [@matejoravec](https://github.com/matejoravec).\n* :construction_worker: Latest changes action added. PR [#24](https://github.com/DataSentics/p360-export/pull/24) by [@matejoravec](https://github.com/matejoravec).\n",
    'author': 'Datasentics',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.10,<4.0.0',
}


setup(**setup_kwargs)
