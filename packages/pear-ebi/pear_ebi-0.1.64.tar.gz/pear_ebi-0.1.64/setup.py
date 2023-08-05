from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="pear_ebi",
    version="0.1.64",
    license="MIT License",
    description="Embeds phylogenetic tree distances and produce representations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Andrea Rubbi",
    author_email="andrea.rubbi.98@gmail.com",
    url="https://github.com/AndreaRubbi/TreeEmbedding",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # "Intended Audience :: Bioinformaticians",
        # "Topic :: Phylogenetics",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib>=3.4",
        "scikit-learn",
        "plotly",
        "rich",
        "pyDRMetrics",
        "tqdm",
        "toml",
        "ipywidgets==7.7.2",
    ],
    entry_points={"console_scripts": ["pear_ebi = pear_ebi.__main__:main"]},
)
