# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['panorma']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'panorma',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Panorma\nA lightweight Python package (just over 50 lines of code) that enables you to create typed \nmodels for Pandas DataFrames using classes. \n\nYou can easily define  structured models, enforce column typing, \nenjoy autocompletion, and catch invalid column errors early in your DataFrame operations. \n\nSimplify your data modeling and enhance the reliability of your DataFrame workflows.\n\nInstallation:\n- \n```shell script\n  pip install panorma\n```\n\nExample:\n-\n- Create some models:\n```python\nfrom panorma.fields import StringDtype, Int16Dtype, Float32Dtype, Timestamp, CategoricalDtype\nfrom panorma.frames import DataFrame\n\nclass Users(DataFrame):\n    name: StringDtype\n    age: Int16Dtype\n    percentage: Float32Dtype\n    birth_date: Timestamp\n\n\nclass Cars(DataFrame):\n    car: StringDtype\n    mpg: Float32Dtype\n    cylinders: Int16Dtype\n    displacement: Float32Dtype\n    horsepower: Float32Dtype\n    weight: Float32Dtype\n    acceleration: Float32Dtype\n    model: Int16Dtype\n    origin: CategoricalDtype\n```\n\n- Instantiate your models as you instantiate a simple pandas dataframe\n\n```python\nimport pandas as pd\n\nusers = Users({\n    "name": [\'john\', \'kevin\'],\n    "age": [99, 15],\n    "percentage": [0.8, 7.3],\n    "birth_date": [pd.Timestamp(\'20180310\'), pd.Timestamp(\'20230910\')],\n})\ncars = Cars(pd.read_csv(\'CAR_DATASET.csv\'))\n```\n\n- You will get autocompletion for models columns and pandas at the same time\n![image](static/autocompletion.png)\n\n- If the columns of your data are not matching your model, you will get a NotMatchingFields exception:\n![image](static/columns_not_matching.png)\n\n- If a column cannot be cast to the type declared in the model, you will get a ParseError exception:\n![image](static/parse_impossible.png)',
    'author': 'MayasMess',
    'author_email': 'amayas.messara@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
