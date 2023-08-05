# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hydrolib',
 'hydrolib.dhydamo',
 'hydrolib.dhydamo.converters',
 'hydrolib.dhydamo.core',
 'hydrolib.dhydamo.geometry',
 'hydrolib.dhydamo.io',
 'hydrolib.dhydamo.modeldata',
 'hydrolib.post',
 'hydrolib.profile_optimizer',
 'hydrolib.profile_optimizer.profile_optimizer']

package_data = \
{'': ['*'],
 'hydrolib': ['arcadis/*',
              'arcadis/docs/*',
              'case_management_tools/*',
              'case_management_tools/docs/*',
              'hydromt_delft3dfm/*',
              'hydromt_delft3dfm/docs/*',
              'hydromt_delft3dfm/docs/developments/*',
              'hydromt_delft3dfm/docs/getting_started/*',
              'hydromt_delft3dfm/docs/reference/*',
              'hydromt_delft3dfm/docs/user_guide/*',
              'hydromt_delft3dfm/docs/user_guide/working_with_the_delft3dfm_model/*',
              'inundation_toolbox/*',
              'inundation_toolbox/docs/*',
              'notebooks/*',
              'tests/data/*',
              'tests/data/complex_controllers/*',
              'tests/data/rasters/*',
              'tests/data/rasters/evaporation/*',
              'tests/data/rasters/precipitation/*',
              'tests/data/rasters/seepage/*'],
 'hydrolib.dhydamo': ['docs/*',
                      'docs/developments/*',
                      'docs/getting_started/*',
                      'docs/reference/*',
                      'resources/RR/*',
                      'resources/RTC/*'],
 'hydrolib.profile_optimizer': ['docs/*',
                                'figures/*',
                                'src/*',
                                'src/moergestels_broek/*',
                                'src/moergestels_broek/roughness/*']}

install_requires = \
['contextily>=1.0.1,<2.0.0',
 'fiona>=1.8,<2.0',
 'fire>=0.5.0,<0.6.0',
 'geopandas>=0.10,<0.11',
 'hkvsobekpy>=1.5,<2.0',
 'hydrolib-core==0.4.1',
 'imod==0.10.1',
 'jupyter>=1.0.0,<2.0.0',
 'llvmlite>=0.39.1,<0.40.0',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy==1.21',
 'openpyxl>=3,<4',
 'pandas>=1.2,<2.0',
 'rasterio>=1.3.4,<2.0.0',
 'rasterstats>=0.17.0,<0.18.0',
 'scipy>=1.9,<2.0',
 'shapely>=1.8,<2.0',
 'tqdm>=4.64.1,<5.0.0',
 'xarray>=0.17,<0.18']

setup_kwargs = {
    'name': 'hydrolib',
    'version': '0.2.0',
    'description': 'HYDROLIB tools for hydrodynamic and hydrological modelling workflows',
    'long_description': 'None',
    'author': 'Deltares',
    'author_email': 'None',
    'maintainer': 'Arthur van Dam',
    'maintainer_email': 'arthur.vandam@deltares.nl',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
