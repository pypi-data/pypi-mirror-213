# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manim_physics',
 'manim_physics.electromagnetism',
 'manim_physics.optics',
 'manim_physics.rigid_mechanics']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.8.0,<2.0.0', 'manim>=0.17.3,<0.18.0', 'pymunk>=6.0.0,<7.0.0']

entry_points = \
{'manim.plugins': ['manim_physics = manim_physics']}

setup_kwargs = {
    'name': 'manim-physics',
    'version': '0.3.0',
    'description': 'Support physics simulation',
    'long_description': '# manim-physics \n## Introduction\nThis is a 2D physics simulation plugin that allows you to generate complicated\nscenes in various branches of Physics such as rigid mechanics,\nelectromagnetism, wave etc. **Due to some reason, I (Matheart) may not have\ntime to maintain this repo, if you want to contribute please seek help from\nother contributors.**\n\nOfficial Documentation: https://manim-physics.readthedocs.io/en/latest/\n\nContributors: \n- [**pdcxs**](https://github.com/pdcxs)\n- [**Matheart**](https://github.com/Matheart)\n- [**icedcoffeeee**](https://github.com/icedcoffeeee)\n\n# Installation\n`manim-physics` is a package on pypi, and can be directly installed using pip:\n```bash\npip install manim-physics\n```\n',
    'author': 'Matheart',
    'author_email': 'waautomationwong@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Matheart/manim-physics',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
