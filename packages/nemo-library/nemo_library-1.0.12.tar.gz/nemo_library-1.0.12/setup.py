from setuptools import setup, find_packages

setup(
    name='nemo_library',
    version='1.0.12',
    packages=find_packages(),
    install_requires=[
        'requests','pandas'
    ],
    author='Gunnar Schug',
    author_email='GunnarSchug81@gmail.com',
    description='A library for uploading data to and downloading reports from NEMO cloud solution',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',    
    classifiers=[
        'Programming Language :: Python :: 3.11',
    ],
    project_urls={
        'Github': 'https://github.com/H3rm1nat0r/nemo_library',  
        'NEMO': 'https://enter.nemo-ai.com/nemo/'
    }
)
