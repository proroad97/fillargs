
## About

If you are tired to provide the same arguments to a function or method, this library is for you. There is no neccessity passing 'verbose' each time. 
## Key Features

* Supports every combination of arguments(keyword,positional only,etc)
* Suitable for manipulating user-given methods of a class or instance

## How To Use
How to handle an single function:

```python
from fillargs import fill_function

default_args={"a":1,"b":2,"c":3}

@fill_function(reserved_args=default_args)
def fun(a,b,c=None,/d=None):
    print(a,b,c,d)

fun(1,2)
```
you can pass also a argument environment:

```python
from fillargs.env import ArgEnv,getenv
from fillargs import fill_function
default_args={"a":1,"b":2,"c":3}

env=ArgEnv(default_args={"a":1,"b":2,"d":3},name="arg_env")
#or
env=getenv(name="arg_env")
@fill_function(arg_env=env)
def fun(a,b,c=None,/d=None):
    print(a,b,c,d)


```
In case you dont provide arguments or environment , a default environment created by the user will be used:
```python
from fillargs.env import DefaultEnv
from fillargs import fill_function
args={"a":1,"b":2}
default_env=DefaultEnv(args)

@fill_function
def fun(*args,**kwds):
    print(args,kwds)

```

It is possible to handle a instance or a class with the function 'handle_instance':
```python
from fillargs import handle_instance
from yourclass import YourClass

instance=YourClass()
args={}
filled_instance=handle_instance(instace,reserved_args=args,on_names=["method1","method2"],strict=True)

#as a decorator
@handle_instance(reserved_args=args)
class YourClass:
    pass
```
Note that if you dont provide 'on_names' argument it will filter dunder and private methods and then it will decorate the remaining methods. Setting strict to False it will match each method's name that contains some name from on_names, else they must match exactly

Also, you might use this library to provide the default arguments in each individual method of a class without write them in the method's definition( Why to do this?)






