from setuptools import setup, find_packages

setup(
    name='NN-FAL',
    version='1.0',
    packages=find_packages(),
    package_data={
        '': ['network/**/*', 'property/**/*', 'source/**/*', 'validation/**/*']
    },
    entry_points={
        'console_scripts': [
            'NNFAL=NNFAL.source.NNFAL:main'
        ]
    },
)
