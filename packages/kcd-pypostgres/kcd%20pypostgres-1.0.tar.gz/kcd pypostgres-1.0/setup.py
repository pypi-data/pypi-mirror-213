from setuptools import setup

setup(
    name='kcd pypostgres',
    version='1.0',
    py_modules=['pypostgres'],
    install_requires=[
        'fire',
    ],
    entry_points={
        'console_scripts': [
            'pypostgres = pypostgres:main',
        ],
    },
)