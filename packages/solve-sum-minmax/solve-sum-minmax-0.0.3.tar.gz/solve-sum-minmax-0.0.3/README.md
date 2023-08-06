**What is this module?**:  
`solve-sum-minmax` is used to solve a sum of min/max equations in python by 
taking advantage of the powerful sympy library. For instance, say you want to solve this equation: 
min(400, 500x) + min(200, 500x) + min(0, 500x) = 700 
with the assumption that
x is within range (0, 1).  
In Math, the rigorous way would 
require you to set up all possible conditions, which 
might result in huge computation. 
Currently, there isn't any available packages in Python
that allows you to solve this kind of equation fastly with minimum codes. Thus,
this package is developed to fill the void and hopefully be of use to the broad population.  
****
**Quick Start**:  
Let's say you want to find the solution for the equation 
min(500, 600a) + max(400, 500a) = 500. Solving it in Math makes you feel 
annoyed, and you ask yourself, "What if there is a library that lets me 
solve it like a piece of cake?" Yes, there is a library now, 
although not perfect. You can use it like below:  
```
from solve-sum-minmax import solver
>>> eq = "min(500, 600*a) + max(400, 500*a) = 500"
>>> solver.solve_sum_minmax(eq, "a")
1/6
```
Yayyyy😆😆! You solved this complex-looking equation with 3 lines of code, 
but what does it mean? Let's break it down: here the core function 
`solve_sum_minmax` takes in two required parameters 
`equation` and `var_name`. `equation` takes in a string of the equation you want to solve 
and `var_name` lets you define your variable with flexibility, such as `"a"`
or `"x"`. Optionally, you can also pass in `"low"`, `"high"`, and `"decimal"`, 
with details left out in the docstring if you are interested.  
****
**Features in 0.0.3**: 
* Now the module is able to return exact values as fractions, such as 1/6.
* When there isn't a solution, the function would return `None`. 
* you can put the variable either in the first place inside the parenthesis 
or in the second place. 
* you can use any characters in the alphabet except `"m"` for the variable.
* you can use min and max together in one equation.
* you can use + or -. 
* you can have constants in front of min or max, such as 2*min(400, 400a).
****
**Limitations**:  
* One of the biggest limitations now is when there are infinitely many solutions, 
the module cannot handle it well and would only return a single real number.
* Because the module is written in a way that it heavily depends on regular 
expressions, it currently doesn't support `"m"` as user-defined variable name.
* With the reason same as above, the user needs to follow the format of the 
equation carefully, or the module might break. 
****
**Contact**:  
* **Email**: yz4175@columbia.edu
* **Collaboration**: collaborations are welcomed, please send me an email if you 
are interested.
