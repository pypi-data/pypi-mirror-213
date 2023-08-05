import glob
import pathlib
from distutils.util import convert_path

import pkg_resources
from setuptools import setup

with pathlib.Path('requirements.txt').open() as r:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(r)
    ]
install_requires.append('setuptools')

main_ns = {}
version = convert_path('hub/version.py')
with open(version) as f:
  exec(f.read(), main_ns)




setup(
  name='cerc-hub',
  version=main_ns['__version__'],
  description="CERC Hub consist in a set of classes (Central data model), importers and exporters to help researchers "
              "to create better and sustainable cities",
  long_description="CERC Hub consist in a set of classes (Central data model), importers and exporters to help "
                   "researchers to create better and sustainable cities.\n\nDevelop at Concordia university in canada "
                   "as part of the research group from the next generation cities institute our aim among others it's "
                   "to provide a comprehensive set of tools to help researchers and urban developers to make decisions "
                   "to improve the livability and efficiency of our cities",
  classifiers=[
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
  ],
  include_package_data=True,
  packages=['hub',
            'hub.catalog_factories',
            'hub.catalog_factories.construction',
            'hub.catalog_factories.cost',
            'hub.catalog_factories.data_models',
            'hub.catalog_factories.data_models.construction',
            'hub.catalog_factories.data_models.cost',
            'hub.catalog_factories.data_models.energy_systems',
            'hub.catalog_factories.data_models.greenery',
            'hub.catalog_factories.data_models.usages',
            'hub.catalog_factories.energy_systems',
            'hub.catalog_factories.greenery',
            'hub.catalog_factories.greenery.ecore_greenery',
            'hub.catalog_factories.usage',
            'hub.city_model_structure',
            'hub.city_model_structure.attributes',
            'hub.city_model_structure.building_demand',
            'hub.city_model_structure.energy_systems',
            'hub.city_model_structure.greenery',
            'hub.city_model_structure.iot',
            'hub.city_model_structure.transport',
            'hub.config',
            'hub.data',
            'hub.exports',
            'hub.exports.building_energy',
            'hub.exports.building_energy.idf_files',
            'hub.exports.building_energy.insel',
            'hub.exports.energy_systems',
            'hub.exports.formats',
            'hub.helpers',
            'hub.helpers.peak_calculation',
            'hub.helpers.data',
            'hub.imports',
            'hub.imports.construction',
            'hub.imports.construction.helpers',
            'hub.imports.energy_systems',
            'hub.imports.geometry',
            'hub.imports.geometry.citygml_classes',
            'hub.imports.geometry.helpers',
            'hub.imports.results',
            'hub.imports.usage',
            'hub.imports.weather',
            'hub.imports.weather.helpers',
            'hub.persistence',
            'hub.persistence.models',
            'hub.persistence.repositories',
            'hub.imports'
            ],
  setup_requires=install_requires,
  install_requires=install_requires,
  data_files=[
    ('hub', glob.glob('requirements.txt')),
    ('hub/config', glob.glob('hub/config/*.ini')),
    ('hub/catalog_factories/greenery/ecore_greenery', glob.glob('hub/catalog_factories/greenery/ecore_greenery/*.ecore')),
    ('hub/data/construction', glob.glob('hub/data/construction/*')),
    ('hub/data/costs', glob.glob('hub/data/costs/montreal_costs.xml')),
    ('hub/data/customized_imports', glob.glob('hub/data/customized_imports/ashrae_archetypes.xml')),
    ('hub/data/energy_systems', glob.glob('hub/data/energy_systems/*.xml')),
    ('hub/data/energy_systems/heat_pumps', glob.glob('hub/data/energy_systems/heat_pumps/*.xml')),
    ('hub/data/energy_systems/heat_pumps', glob.glob('hub/data/energy_systems/heat_pumps/*.insel')),
    ('hub/data/energy_systems/heat_pumps', glob.glob('hub/data/energy_systems/heat_pumps/*.xlsx')),
    ('hub/data/energy_systems/heat_pumps', glob.glob('hub/data/energy_systems/heat_pumps/*.txt')),
    ('hub/data/energy_systems/heat_pumps', glob.glob('hub/data/energy_systems/heat_pumps/*.yaml')),
    ('hub/data/geolocation', glob.glob('hub/data/geolocation/*.txt')),
    ('hub/data/greenery', glob.glob('hub/data/greenery/*.xml')),
    ('hub/data/usage', glob.glob('hub/data/usage/*.xml')),
    ('hub/data/usage', glob.glob('hub/data/usage/*.xlsx')),
    ('hub/data/weather', glob.glob('hub/data/weather/*.dat')),
    ('hub/data/weather/epw', glob.glob('hub/data/weather/epw/*.epw')),
    ('hub/data/weather', glob.glob('hub/data/weather/*.dat')),
    ('hub/exports/building_energy/idf_files', glob.glob('hub/exports/building_energy/idf_files/*.idf')),
    ('hub/exports/building_energy/idf_files', glob.glob('hub/exports/building_energy/idf_files/*.idd'))
  ],

)
