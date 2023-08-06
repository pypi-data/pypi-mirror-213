# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datastation',
 'datastation.common',
 'datastation.dans_bag',
 'datastation.dataverse',
 'datastation.ingestflow',
 'datastation.scripts',
 'datastation.verifydataset']

package_data = \
{'': ['*']}

install_requires = \
['dicttoxml>=1.7.4,<2.0.0',
 'lxml>=4.8.0,<5.0.0',
 'psycopg>=3.1.8,<4.0.0',
 'pyYAML>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'rich>=13.3.4,<14.0.0']

entry_points = \
{'console_scripts': ['dans-bag-validate = datastation.dans_bag_validate:main',
                     'dv-banner = datastation.dv_banner:main',
                     'dv-dataset-delete-draft = '
                     'datastation.dv_dataset_delete_draft:main',
                     'dv-dataset-destroy = datastation.dv_dataset_destroy:main',
                     'dv-dataset-destroy-migration-placeholder = '
                     'datastation.dv_dataset_destroy_migration_placeholder:main',
                     'dv-dataset-find-by-role-assignment = '
                     'datastation.dv_dataset_find_by_role_assignment:main',
                     'dv-dataset-get-metadata = '
                     'datastation.dv_dataset_get_metadata:main',
                     'dv-dataset-get-metadata-export = '
                     'datastation.dv_dataset_get_metadata_export:main',
                     'dv-dataset-lock = datastation.dv_dataset_lock:main',
                     'dv-dataset-publish = datastation.dv_dataset_publish:main',
                     'dv-dataset-reindex = datastation.dv_dataset_reindex:main',
                     'dv-dataset-reingest-tabular = '
                     'datastation.dv_dataset_reingest_tabular:main',
                     'dv-dataset-role-assignment = '
                     'datastation.dv_dataset_role_assignment:main',
                     'dv-dataset-update-datacite = '
                     'datastation.dv_dataset_update_datacite:main',
                     'dv-dataset-verify = datastation.dv_dataset_verify:main',
                     'dv-notifications-cleanup = '
                     'datastation.dv_notifications_cleanup:main',
                     'dv-user-import = datastation.dv_user_import:main',
                     'ingest-flow = datastation.ingest_flow:main']}

setup_kwargs = {
    'name': 'dans-datastation-tools',
    'version': '0.27.0',
    'description': 'Command line utilities for Data Station application management',
    'long_description': 'None',
    'author': 'DANS-KNAW',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
