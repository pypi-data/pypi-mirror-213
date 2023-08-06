# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_join_unrelated']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-join-unrelated',
    'version': '0.1.0',
    'description': 'Join Django ORM models having no relations.',
    'long_description': '# django-join-unrelated\n![Python version](https://img.shields.io/badge/Python-3.8%2B-blue)\n[![Tests](https://github.com/KazakovDenis/django-join-unrelated/actions/workflows/cicd.yml/badge.svg)](https://github.com/KazakovDenis/django-join-unrelated/actions/workflows/cicd.yml)\n\n### Use SQL Join with Django ORM models having no relations.\n\nIf you have models in your project that share the same data but have no relations, \nyou might face a situation when you need to join them. But Django does not provide \nthis functionality yet.\n  \nWith `django-join-unrelated` you can do the following \n(models defined [here](https://github.com/KazakovDenis/django-join-unrelated/blob/main/app/core/models.py)):\n```python\nfrom app.core.models import Jedi, Person\n\nPerson.objects.create(first_name=\'Padme\', last_name=\'Amidala\', birth_place=\'Naboo\')\nPerson.objects.create(first_name=\'Obi-Wan\', last_name=\'Kenobi\', birth_place=\'Stewjon\')\nJedi.objects.create(first_name=\'Obi-Wan\', last_name=\'Kenobi\', force=100)\nJedi.objects.create(first_name=\'Mace\', last_name=\'Windu\', force=80)\n\nJedi.objects.join(first_name=Person.first_name).values_list(\'first_name\')\n# <UnrelatedJoinQuerySet [(\'Obi-Wan\',)]>\n\nprint(Jedi.objects.join(first_name=Person.first_name).values_list(\'first_name\').query)\n# SELECT "core_jedi"."first_name" FROM "core_jedi" INNER JOIN core_person ON ("core_jedi"."first_name" = core_person."first_name")\n```\n\n`django-join-unrelated` tries to keep all QuerySet power where it is possible:\n```python\nJedi.objects.join(first_name=Person.first_name).filter(last_name=\'Kenobi\')\n# <UnrelatedJoinQuerySet [<Jedi: Jedi object (1)>]>\n\nJedi.objects.join(first_name=Person.first_name).filter(last_name=\'Windu\')\n# <UnrelatedJoinQuerySet []>\n```\n\n## Installation\nYou can install `django-join-unrelated` using pip:\n\n```\npip install django-join-unrelated\n```\n\n## Usage\nJust import `UnrelatedJoinManager` and set it as an attribute to your models:\n\n```python\nfrom django.db import models\nfrom django_join_unrelated import UnrelatedJoinManager\n\nclass Jedi(models.Model):\n    first_name = models.CharField(\'First name\', max_length=128)\n    last_name = models.CharField(\'Last name\', max_length=128)\n    force = models.IntegerField(\'Force\')\n\n    objects = UnrelatedJoinManager()\n\n    class Meta:\n        verbose_name = \'Jedi\'\n```',
    'author': 'Denis Kazakov',
    'author_email': 'denis@kazakov.ru.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/django-join-unrelated',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
