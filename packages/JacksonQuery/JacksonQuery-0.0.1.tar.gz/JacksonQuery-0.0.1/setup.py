from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='JacksonQuery',
    version='0.0.1',
    description='Automated interaction and data extraction tool for Jackson National Life Insurance website',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Nathan Ramos, CFA®',
    author_email='info@nrcapitalmanagement.com',
    url='https://github.com/nathanramoscfa/JacksonQuery',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4>=4.12.2',
        'bt>=0.2.9',
        'ffn>=0.3.6',
        'fuzzywuzzy>=0.18.0',
        'keyring>=23.13.1',
        'matplotlib>=3.7.1',
        'numpy>=1.23.5',
        'pandas>=1.5.3',
        'patsy>=0.5.3',
        'seaborn>=0.12.2',
        'selenium>=4.9.0',
        'setuptools>=66.0.0',
        'statsmodels>=0.13.5',
        'tika>=2.6.0',
        'tiafork>=1.2.0',
        'tqdm>=4.65.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='automation, jackson, scraping, selenium',
    python_requires='>=3.11',
)
