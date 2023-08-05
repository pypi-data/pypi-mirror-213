import os
from setuptools import setup, find_namespace_packages


def get_version():
    import os.path

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'src/momotor/django/version.py'), 'r') as version_file:
        loc = {}
        exec(version_file.readline(), {}, loc)
        return loc['__VERSION__']


def get_long_description():
    with open("README.md", "r") as fh:
        return fh.read()


full_version = get_version() + os.environ.get('VERSION_TAG', '')
is_dev = '.dev' in full_version

setup(
    name='momotor-django',
    version=get_version(),
    author='Erik Scheffers',
    author_email='e.t.j.scheffers@tue.nl',
    description="Momotor bindings for the Django project",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url='https://momotor.org/',
    project_urls={
        'Documentation': f'https://momotor.org/doc/engine/momotor-django/{"dev" if is_dev else "release"}/{full_version}/',
        'Source': 'https://gitlab.tue.nl/momotor/engine-py3/momotor-django/',
        'Tracker': 'https://gitlab.tue.nl/momotor/engine-py3/momotor-django/issues',
    },
    install_requires=[
        'asgiref',
        'backoff',
        'django>=3.2.0,<5',
        'protobuf',
        'momotor-engine-proto~=4.0',
        'momotor-engine-shared~=1.1'
    ],
    extras_require={
        'docs': [
            'Sphinx',
            'sphinx-autodoc-typehints',
        ]
    },
    python_requires='>=3.7',
    packages=find_namespace_packages(where='src', include=('momotor.*',)),
    package_dir={'': 'src'},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    ],
)
