#!/usr/bin/env -S Rscript --vanilla

if (! require(epiparameter, quietly = TRUE)) {
  install.packages(
    "epiparameter",
    repos = c(
      "https://epiverse-trace.r-universe.dev",
      "https://cloud.r-project.org"
    )
  )
}

library(epiparameter)

#
# Extract the distribution name and shape parameters from an epiparameter
# distribution, so that they can be saved and then read from Python.
#
summarise_epidist_for_python <- function(epidist) {
  name <- family(epidist$prob_dist)
  params <- distributional::parameters(epidist$prob_dist)
  list(name = name, params = as.list(params))
}

influenza_incubation <- epidist_db(
  disease = "influenza",
  epi_dist = "incubation period",
  single_epidist = TRUE
)

saveRDS(
  summarise_epidist_for_python(influenza_incubation),
  "influenza_incubation.rds"
)

#
# Also save an invalid distribution, for testing purposes.
#

saveRDS(
  list(name = "invalid", unexpected = "should raise an exception"),
  "invalid_distribution.rds"
)
