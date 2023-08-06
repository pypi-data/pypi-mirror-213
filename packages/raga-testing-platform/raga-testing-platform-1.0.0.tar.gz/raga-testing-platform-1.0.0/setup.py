from setuptools import setup, find_packages

setup(
    name='raga-testing-platform',
    version='1.0.0',
    author='Raga AI',
    author_email='support@ragaai.com',
    description='Short description or overview of the raga package.',
    long_description='Longer description or documentation of the package.',
    url='https://github.com/whoosh-labs/testing-platform-python-client',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'pandas',
        'requests',
        'urllib3==1.26.7'
    ],
)
