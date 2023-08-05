# DotENV-Reader
A Package for PiP that will read dotenv files.

# How to use
Create a new .env file use the example one for testing and a new python file or use the test.py file
Add this code to the new python file to get and config dotenv

```python

import dotenvreader as dotenv
dotenv.config()
print(dotenv.get_value("test"))

```