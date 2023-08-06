[![PyPI version](https://badge.fury.io/py/proptables.svg)](https://badge.fury.io/py/proptables)
[![pypi supported versions](https://img.shields.io/pypi/pyversions/proptables.svg)](https://pypi.python.org/pypi/proptables)
# Python proptables
#### proptables is a Python library designed to provide easy access to comprehensive property tables for R134a 
##### (water-steam tables will be implemented soon). 

# To Install
```bash
pip install proptables
```
## How to use
```python
from proptables import R134a
```

## To find data in saturated liquid vapour region

Use either one of followings
```python
R134a(Pressure=VALUE_IN_KPA)
R134a(Temperature=VALUE_IN_C)
```    
![image](https://github.com/Buddhi19/PropertyTables_Python/assets/119914594/93dc1dd8-5267-4a0b-9c6f-f22196a409c3)

![image](https://github.com/Buddhi19/PropertyTables_Python/assets/119914594/e3fa0006-7f3f-4e03-a568-433b606ec995)

## To find composition of states

```python
R134a(Pressure=VALUE_IN_KPA,Enthalpy=VALUE_IN_KJ/Kg)
R134a(Temperature=VALUE_IN_C,Enthalpy=VALUE_IN_KJ/Kg)
```
![image](https://github.com/Buddhi19/PropertyTables_Python/assets/119914594/b3bad57e-440c-444a-91e1-baa589d78c7a)

## To vishualize superheated vapour table at a given pressure

```python
R134a(Pressure=VALUE_IN_KPA,Superheated=True)
```
![image](https://github.com/Buddhi19/PropertyTables_Python/assets/119914594/f4661274-5347-4b81-a45d-090725f95cfb)

## To find data in the superheated region when any parameter is known with pressure

```python
R134a(Pressure=VALUE_IN_KPA,Enthalpy=VALUE_IN_KJ/Kg,Superheated=True)
R134a(Pressure=VALUE_IN_KPA,Temperature=VALUE_IN_C,Superheated=True)
R134a(Pressure=VALUE_IN_KPA,Entropy=VALUE_IN_KJ/KgK,Superheated=True)
R134a(Pressure=VALUE_IN_KPA,Energy=VALUE_IN_KJ/Kg,Superheated=True)
```

![image](https://github.com/Buddhi19/PropertyTables_Python/assets/119914594/1bd85362-5324-492f-8a74-f58bcb8fcb8d)

