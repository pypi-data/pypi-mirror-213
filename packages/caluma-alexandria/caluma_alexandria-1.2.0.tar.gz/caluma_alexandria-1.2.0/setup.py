# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alexandria',
 'alexandria.core',
 'alexandria.core.migrations',
 'alexandria.oidc_auth',
 'alexandria.settings']

package_data = \
{'': ['*']}

install_requires = \
['django-environ>=0.9.0,<0.11.0',
 'django-filter>=22.1,<24.0',
 'django-localized-fields>=6.6,<7.0',
 'django>=3.2,<3.3',
 'djangorestframework-jsonapi>=5.0.0,<7.0.0',
 'djangorestframework>=3.13.0,<4.0.0',
 'minio>=7.1.14,<8.0.0',
 'mozilla-django-oidc>=2.0.0,<3.0.0',
 'preview-generator>=0.29,<0.30',
 'psycopg2-binary>=2.9,<2.10',
 'requests>=2.28.0,<3.0.0',
 'uwsgi>=2.0.20,<3.0.0',
 'vtk>=9.2.6,<10.0.0']

setup_kwargs = {
    'name': 'caluma-alexandria',
    'version': '1.2.0',
    'description': 'Document management service',
    'long_description': '# alexandria\n\n[![Build Status](https://github.com/projectcaluma/emeis/workflows/Tests/badge.svg)](https://github.com/projectcaluma/emeis/actions?query=workflow%3ATests)\n[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/projectcaluma/emeis/blob/master/setup.cfg#L50)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/projectcaluma/alexandria)\n[![License: GPL-3.0-or-later](https://img.shields.io/github/license/projectcaluma/emeis)](https://spdx.org/licenses/GPL-3.0-or-later.html)\n\nOur goal is to implement an external document management service to hold and provide uploaded documents.\nDocuments can be uploaded and, depending on user access, managed by internal as well as external users.\n\nThe goal is NOT to re implement a complex [DMS](https://en.wikipedia.org/wiki/Document_management_system) but rather to have a simple and user-friendly way of managing documents with different permissions.\n\nAll User Interface interactions should be as simple as possible and easily understandable.\n\n[Original RFC that led to alexandria](docs/original_alexandria_rfc.md)\n\n## Getting started\n\n### Installation\n\n**Requirements**\n* docker\n* docker-compose\n\nAfter installing and configuring those, download [docker-compose.yml](https://raw.githubusercontent.com/projectcaluma/alexandria/master/docker-compose.yml) and run the following commands:\n\n```bash\n# only needs to be run once\necho UID=$UID > .env\n\ndocker-compose up -d\n```\n\nYou can now access the api at [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/).\n\n### Example data\n\nTo load a set of categories run the following command:\n```bash\nmake load_example_data\n```\n\n### Configuration\n\nDocument Merge Service is a [12factor app](https://12factor.net/) which means that configuration is stored in environment variables.\nDifferent environment variable types are explained at [django-environ](https://github.com/joke2k/django-environ#supported-types).\n\n#### Common\n\nA list of configuration options which you need\n\n* Django configuration\n  * `SECRET_KEY`: A secret key used for cryptography. This needs to be a random string of a certain length. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY).\n  * `ALLOWED_HOSTS`: A list of hosts/domains your service will be served from. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts).\n  * `DATABASE_ENGINE`: Database backend to use. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DATABASE-ENGINE). (default: django.db.backends.postgresql)\n  * `DATABASE_HOST`: Host to use when connecting to database (default: localhost)\n  * `DATABASE_PORT`: Port to use when connecting to database (default: 5432)\n  * `DATABASE_NAME`: Name of database to use (default: alexandria)\n  * `DATABASE_USER`: Username to use when connecting to the database (default: alexandria)\n  * `DATABASE_PASSWORD`: Password to use when connecting to database\n* Authentication configuration\n  * `OIDC_OP_USER_ENDPOINT`: Userinfo endpoint for OIDC\n  * `OIDC_VERIFY_SSL`: Set to `false` if you want to disable verifying SSL certs. Useful for development\n  * `OIDC_DRF_AUTH_BACKEND`: Overwrite the default authentication backend with your own\n  * `ALEXANDRIA_OIDC_USER_FACTORY`: Overwrite the default user with your own\n  * `ALEXANDRIA_CREATED_BY_USER_PROPERTY`: Overwrite the default user property which is used for `..._by_user` (default: username)\n  * `ALEXANDRIA_CREATED_BY_GROUP_PROPERTY`: Overwrite the default group property which is used for `..._by_group` (default: group)\n* Authorization configurations\n  * `ALEXANDRIA_VISIBILITY_CLASSES`: Comma-separated list of classes that define visibility for all models\n  * `ALEXANDRIA_PERMISSION_CLASSES`: Comma-separated list of classes that define permissions for all models\n* Data validation configuration\n  * `ALEXANDRIA_VALIDATION_CLASSES`: Comma-separated list of classes that define [custom validations](docs/validation.md)\n\nFor development, you can also set the following environemnt variables to help\nyou:\n\n  * `DEV_AUTH_BACKEND`: Set this to "true" to enable a fake auth backend that simulates an authenticated user. Requires `DEBUG` to be set to `True` as well.\n  * `DEBUG`: Set this to true for debugging during development. Never enable this in production, as it **will** leak information to the public if you do.\n\n## Contributing\n\nLook at our [contributing guidelines](CONTRIBUTING.md) to start with your first contribution.\n\n## Maintainer\'s Handbook\n\nSome notes for maintaining this project can be found in [the maintainer\'s handbook](MAINTAINING.md).',
    'author': 'Caluma',
    'author_email': 'info@caluma.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/projectcaluma/alexandria',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
