# Load epiparameter distributions in Python

1. Save the distribution name and shape parameters to a `RDS` file:

   ```R
   summarise_epidist_for_python <- function(epidist) {
     name <- family(epidist$prob_dist)
     params <- distributional::parameters(epidist$prob_dist)
     list(name = name, params = as.list(params))
   }

   my_dist <- load_my_distribution()

   saveRDS(summarise_epidist_for_python(my_dist), "my_dist.rds")
   ```

2. Load the distribution in Python:

   ```py
   import pydist

   dist = pydist.load_distribution("my_dist.rds")
   samples = dist.rvs(size=1000)
   ```

Note that this relies on mapping R distribution names and shape parameter names to their SciPy equivalents.
Currently, this package only defines these mappings for a very few distributions.
The user can override these mappings as necessary:

```py
import pydist

# Map the R "beta" distribution (key) to ``scipy.stats.beta`` (value).
dist_map = {"beta": "beta"}
# Map R shape parameters ("shape1", "shape2") to SciPy parameters ("a", "b").
param_map = {"shape1": "a", "shape2": "b"}
dist = pydist.load_distribution("my_beta_dist.rds", dist_map, param_map)
```
