# CMH
Implementation of the Cochran-Mantel-Haenzsel Chi2 Test, based on/ported from
"Categorical Data Analysis", page 295 by Agresti (2002) and `R` implementation
of the function `mantelhaen.test()`.


# Usage
````python
import pandas as pd
from cmh import CMH

df = pd.DataFrame(
    [
        ['S1', 'no', 'yes'],
        ['S1', 'no', 'yes'],
        ['S1', 'no', 'yes'],
        ['S1', 'no', 'yes'],
        ['S1', 'no', 'yes'],
        ['S1', 'no', 'yes'],
        ['S1', 'yes', 'yes'],
        ['S1', 'yes', 'yes'],
        ['S1', 'yes', 'yes'],
        ['S1', 'yes', 'yes'],
        ['S1', 'yes', 'yes'],
        ['S1', 'yes', 'yes'],

        ['S2', 'yes', 'yes'],
        ['S2', 'yes', 'yes'],
        ['S2', 'yes', 'yes'],
        ['S2', 'yes', 'yes'],
        ['S2', 'yes', 'yes'],
        ['S2', 'no', 'yes'],
        ['S2', 'no', 'yes'],
        ['S2', 'no', 'yes'],
        ['S2', 'no', 'yes'],
        ['S2', 'no', 'no'],
        ['S2', 'no', 'no'],
        ['S2', 'no', 'no'],
        ['S2', 'no', 'no'],

    ],
    columns=['stratum', 'A', 'B']
)

# CMH() will automatically count frequencies of the columns in the dataframe.
result = CMH(df, 'A', 'B', stratifier='stratum')
print(result)

# Will print:
#
#         Cochran-Mantel-Haenszel Chi2 test
#
# "A" x "B", stratified by "stratum"
#
# Cochran-Mantel-Haenszel M^2 = 3.33333, dof = 1, p-value = 0.0679

# Individual components of the result can be accessed via attributes:
print(result.dof)
print(result.p)

# If you're working in a Jupyter Notebook, you can also use `display()` for
# a nicely formatted result.
display(result)

```
