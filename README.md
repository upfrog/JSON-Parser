A recursive descent JSON parser which extends standard JSON with sets and complex numbers.

This has several further deviations from the official JSON standard. The deviations I have found include:
  1. My parser can handle fractional numbers without a leading zero (eg .2)
  2. My parser can handle floating-point numbers with a (redundant) leading "+"

I am aware the "JSON parsing is a minefield" (https://seriot.ch/projects/parsing_json.html), and am confident there are many, many additional deviations. I am also aware that being able to parse non-standard elements is not always an advantage. 

The biggest challenges of implementing this was wrapping my head around the recursive descent technique I used.
