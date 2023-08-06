import re
from setuptools import setup, find_packages

with open('memento/__init__.py', encoding='utf-8') as f:
    version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read()).group(1)

setup(
    name='memento-scorecard',
    version=version,
    url='https://github.com/Guilliu/Memento',
    author='Guillermo Lizcano Villafáñez',
    author_email='guille.lv.97@gmail.com',
    description='Scorecard development with Python',
    license='Apache License 2.0',
    packages=find_packages(),
    keywords=['python', 'scoring', 'rating', 'logistic', 'regression',
    'scorecard', 'woe', 'credit-risk', 'autogrouping'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable'
    ],
    long_description_content_type='text/markdown',
    long_description='''
# Memento - Scorecard development with Python

**Memento** is a Python package with the aim of providing the necessary tools for:

- Grouping variables (both numerical and categorical) in an automatic and interactive way.
- Development of customizable scorecards adaptable to the requirements of each user.

## Source code
Check out the [GitHub](https://github.com/Guilliu/Memento) repository.

## Documentation
You can find useful documentation [here](https://guilliu.github.io/).
'''
)

