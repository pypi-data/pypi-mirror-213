# JacksonQuery

JacksonQuery is a Python package designed to automate the process of downloading, parsing, and analyzing web content 
from the Jackson National Life (JNL) Insurance website located at www.jackson.com. Its main objective is to facilitate 
investment advisers in making informed decisions about variable annuity subaccount investments.

This package finds, downloads, and parses content of all the variable annuity subaccount prospectuses and Morningstar 
reports found on the JNL website. The parsed content is processed into data structures, enabling easy and efficient data 
analysis. Additionally, JacksonQuery provides a factor model and a portfolio optimization module, automating the 
investment selection and portfolio construction process.

The JNL website provides data on their variable annuity subaccounts only in the form of fund prospectuses and 
Morningstar reports, all in PDF format. There are approximately 120 JNL variable annuity subaccounts for their 
Perspective L product, and the task of going through all of this data is daunting for investment advisers. JacksonQuery 
aims to minimize heuristics and maximize statistical methods in decision-making for investment advisers, making it 
easier to choose the most appropriate subaccounts for their clients.

## Features
- Automated Web Navigation: Automatically logs into the JNL website, navigates to the necessary pages, and handles any 
pop-ups or prompts along the way.
- Data Extraction: Fetches the most recent prospectuses and Morningstar reports for all variable annuity 
subaccounts.
- Advanced Parsing: Utilizes the powerful tika library to parse PDFs and organize the data into easily analyzable 
structures.
- Factor Modeling: Implements a factor model to analyze the performance of the subaccounts.
- Portfolio Optimization: Provides a module to automate the process of creating optimal portfolios based on the parsed 
data.

## Installation
JacksonQuery is available on PyPI and can be installed via pip:
```
pip install jacksonquery
```

## Usage
See the [examples](https://github.com/nathanramoscfa/JacksonQuery/tree/master/examples) directory for usage examples.

## Disclaimer
JacksonQuery is not affiliated with Jackson National Life Insurance Company in any way. This package is not intended to
be used for any purpose other than for educational purposes. Past performance is not indicative of future results. The 
authors of this package are not responsible for any financial losses that may occur as a result of using this package. 
Use at your own risk. 

## License
[MIT](https://choosealicense.com/licenses/mit/)