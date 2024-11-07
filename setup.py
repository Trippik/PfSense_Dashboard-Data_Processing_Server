from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="PfSense_Dashboard-Data_Processing_Server",
    version="1.0.1",
    author="Cameron Trippick",
    install_requires=requirements,
    packages=['data_processing_server', 'data_processing_server.lib'],
    entry_points={
        'console_scripts': [
            'PfSense_Dashboard-Data_Processing_Server = data_processing_server.app:main',
        ]
    }
)