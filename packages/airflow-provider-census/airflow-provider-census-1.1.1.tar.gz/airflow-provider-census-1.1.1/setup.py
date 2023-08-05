# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airflow_provider_census',
 'airflow_provider_census.example_dags',
 'airflow_provider_census.hooks',
 'airflow_provider_census.operators',
 'airflow_provider_census.sensors']

package_data = \
{'': ['*']}

install_requires = \
['apache-airflow-providers-http>=1.1.1,<2.0.0', 'apache-airflow>=1.10']

entry_points = \
{'apache_airflow_provider': ['provider_info = '
                             'airflow_provider_census.__init__:get_provider_info']}

setup_kwargs = {
    'name': 'airflow-provider-census',
    'version': '1.1.1',
    'description': 'A Census provider for Apache Airflow.',
    'long_description': '# Census Provider for Apache Airflow\n\nThis package allows you to trigger syncs for [Census](https://www.getcensus.com/).\n\n## Installation\n\nInstall the [airflow-provider-census](https://pypi.org/project/airflow-provider-census/) package from PyPI using your preferred way of installing python packages.\n\n## Configuration\n\nThere are 2 ways to configure a Census connection depending on whether you are using Airflow 1.10 or Airflow 2.\n\nThe `CensusHook` and `CensusOperator` use the `census_default` connection id as a default, although this is configurable if you would like to use your own connection id.\n\n### Finding the secret-token\n\n1. Go to any sync at https://app.getcensus.com/syncs\n2. Click on the Sync Configuration tab.\n3. Next to API TRIGGER, click "Click to show"\n4. The url will be of the format https://bearer:secret-token:arandomstring@app.getcensus.com/api/v1/syncs/0/trigger\n5. the secret token will be of the format "secret-token:arandomstring" in the url above, including the "secret-token:" part. Do not include the "@".\n\n### Configuration in Airflow 1.10\n\nIn the Airflow Connections UI, create a new connection:\n\n* Conn ID: census_default\n* Conn Type: HTTP\n* Password: secret-token\n\n### Configuration in Airflow 2\n\nIn the Airflow Connections UI, create a new connection:\n\n* Conn Id: census_default\n* Conn Type: Census\n* Census Secret Token: secret-token\n\n## Hooks\n\n### CensusHook\n\n`CensusHook` is a class that inherits from `HttpHook` and can be used to run http requests for Census.\nYou will most likely interact with the operator rather than the hook.\n\nThe hook can be imported by the following code:\n\n```python\nfrom airflow_provider_census.hooks.census import CensusHook\n```\n\n## Operators\n\n### CensusOperator\n\n`CensusOperator` triggers a sync job in Census. The operator takes the following parameters:\n\n1. sync_id : Navigate to the sync and check the url for the sync id. For example https://app.getcensus.com/syncs/0/overview here, the sync_id would be 0.\n2. census_conn_id : The connection id to use. This is optional and defaults to \'census_default\'.\n\nThe operator can be imported by the following code:\n\n```python\nfrom airflow_provider_census.operators.census import CensusOperator\n```\n\n## Sensors\n\n### CensusSensor\n\n`CensusSensor` polls a sync run in Census. The sensor takes the following parameters:\n\n1. sync_run_id : The sync run id you get back from the CensusOperator which triggers a new sync.\n2. census_conn_id : The connection id to use. This is optional and defaults to \'census_default\'.\n\nThe sensor can be imported by the following code:\n\n```python\nfrom airflow_provider_census.sensors.census import CensusSensor\n```\n\n## Example\n\nThe following example will run a Census sync once a day:\n\n```python\nfrom airflow_provider_census.operators.census import CensusOperator\n\nfrom airflow import DAG\nfrom airflow.utils.dates import days_ago\nfrom datetime import timedelta\n\ndefault_args = {\n    "owner": "airflow",\n    "start_date": days_ago(1)\n}\n\ndag = DAG(\'census\', default_args = default_args)\n\nsync = CensusOperator(sync_id = 27, dag = dag, task_id = \'sync\')\n\nsensor = CensusSensor(sync_run_id = "{{ ti.xcom_pull(task_ids = \'sync\') }}", dag = dag, task_id = \'sensor\')\n\nsync >> sensor\n```\n\n# Feedback\n\n[Source code available on Github](https://github.com/sutrolabs/airflow-provider-census). Feedback and pull requests are greatly appreciated. Let us know if we can improve this.\n\n\n# From\n\n:wave: The folks at [Census](http://getcensus.com) originally put this together. Have data? We\'ll sync your data warehouse with your CRM and the customer success apps critical to your team.\n\n# Need help setting this up?\n\nYou can always contact us via support@getcensus.com or [in-app](https://app.getcensus.com/) via the live chat in the bottom right corner.\n',
    'author': 'Census',
    'author_email': 'dev@getcensus.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.getcensus.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
