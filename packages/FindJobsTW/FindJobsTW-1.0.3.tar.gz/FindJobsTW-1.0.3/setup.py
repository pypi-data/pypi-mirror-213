import setuptools
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    
setup(
    name='FindJobsTW',    
    version='1.0.3',      
    packages=find_packages(),    
    install_requires=requirements,
    package_data={
        'findJobs': ['templates/*', 'static/*']
    },  
    author="Danny Fin",
    author_email="dannyfinselect@outlook.com",
    description="A Python package to find jobs on 104.com.tw based on specific keywords.",
    long_description=open('README.md', 'r', encoding='utf-8').read(),# 若Discription.md中有中文 須加上 encoding="utf-8"
    long_description_content_type="text/markdown",
    url="https://github.com/DannyFin/FindJobsTW",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)