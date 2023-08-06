
Change System Environment Variable permanently
[github page](https://github.com/blueboy-tm/python-envariable/)

## Install
```shell
pip install envariable
```

## Example
```python
from envarible import setenv, unsetenv, getenv, getenvall
# The variable TEST is stored permanently with the VALUE value
setenv('TEST', 'VALUE') 

print(getenv('TEST'))
>>> VALUE

# The TEST variable is permanently deleted
unsetenv('TEST')


print(getenv('TEST'))
>>> None

# returned all Environment Variable
all_env = getenvall()
```

## Example 2
```python
from envariable import setenv, getenv

path = getenv('PATH')
setenv('PATH', f'{path}:/my/dir')
```
