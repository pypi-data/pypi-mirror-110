[![Build Status](https://travis-ci.com/ant358/oanda-base.svg?branch=main)](https://travis-ci.com/ant358/oanda-base)
[![codecov](https://codecov.io/gh/ant358/oanda-base/branch/main/graph/badge.svg?token=AYQZW7TNAN)](https://codecov.io/gh/ant358/oanda-base)
# Oanda Base Package
Uses the REST v20 API to access your Oanda account, send orders and receive data.

## Installation 
Create a virtual environment and activate it.  
for ref: https://docs.python.org/3/tutorial/venv.html  

```pip install oandabase```  

Create a ```.env``` file in the root folder and add your account number and token. You can add multiple accounts here e.g. live, practice, different accounts for different strategies etc. The classes in the ```oanda.py``` module are setup to default to ```account=PRACTICE_ACCOUNT``` and ```token=PRACTICE_TOKEN```, when writing strategies to use different accounts simply pass these as keyword arguments to replace the default ones.  
Add ```.env``` to your .gitignore to keep your account details local.  

```
PRACTICE_ACCOUNT=XXX-XXX-XXXXXXXX-XXX
PRACTICE_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  
```  
## Usage:  
Built to be a component of other systems. 
Read through the classes and they should explain themselves.  