from setuptools import setup, find_packages

setup(
    name='image_crypt',
    version='2.0.1',
    packages=find_packages(),
    install_requires=['pillow', 'pyqt5', 'pycryptodomex'],
)
