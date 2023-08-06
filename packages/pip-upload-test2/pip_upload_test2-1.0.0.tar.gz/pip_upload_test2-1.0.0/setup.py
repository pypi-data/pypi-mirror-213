from setuptools import setup, find_packages

setup(
    name='pip_upload_test2',
    version='1.0.0',
    description='Description of your package',
    author='ghaidaa samir',
    author_email='ghaidaaelbelihy@email.com',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        'numpy'
    ],
)

