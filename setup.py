import versioneer
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    # package requirements go here
]

setup(
    name='conda-project',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Tool for encapsulating, running, and reproducing projects with Conda environments",
    license="BSD",
    author="Albert DeFusco",
    author_email='adefusco@anaconda.com',
    url='https://github.com/AlbertDeFusco/conda-project',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'conda_project=conda_project.cli:cli'
        ]
    },
    python_requires=">=3.7",
    install_requires=requirements,
    keywords='conda-project',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
