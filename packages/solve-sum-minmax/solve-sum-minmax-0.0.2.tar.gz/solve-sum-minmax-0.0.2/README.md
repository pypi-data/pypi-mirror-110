**solve-sum-minmax** is used to solve a sum of min/max equations in python by 
using numerical methods. For instance, say you want to solve this equation: 
min(400, 500x) + min(200, 500x) + min(0, 500x) = 700 
with the assumption that
x is within range (0, 1).  
In Math, the rigorous way would 
require you to set up all possible conditions, which 
might result in huge computation. 
Currently, there isn't any available packages in Python
that allows you to solve this kind of equation fastly with minimum codes. Thus,
this package is developed to fill the void and hopefully be of use to the 
broad population.  
**example**: say you want to find the solution for the equation 
min(500, 600a) + max(400, 500a) = 500
```
from solve-sum-minmax import solve
>>> eq = "min(500, 600*a) + max(400, 500*a)"
>>> value = 500
>>> solve.solve_sum_minmax(eq, value)
0.16666
```
**What's new in 0.0.2**: 
1. you can put the variable either in the first place inside the parenthesis 
or in the second place.
   
2. you can use [a-z] for the variable.
3. you can use min and max together in one equation.
4. you can use + or -. 
5. you can have constants in front of min or max, such as 2min(400, 400a).
6. you can specify the magnitude of accuracy for your result (precision to 
   how many decimal places).
   

**current version**: 0.0.2  
**email**: yz4175@columbia.edu  
**disclaimer**: this package is still under development, the current version
only has very limited functionality  
**collaboration**: collaborations are welcomed, please send me an email if you 
are interested.