# Changes in findspark

## 2.0.0

- Do nothing if `pyspark` has already been successfully imported.
- Give private methods `change_rc` and `edit_ipython_profile` private names,
  so they don't seem like public API methods.


## 1.4.2

- Fix regression in 1.4.0 when adding to existing PYSPARK_SUBMIT_ARGS.
  New args are now added to the front.

## 1.4.1

- Avoid setting empty PYSPARK_SUBMIT_ARGS

## 1.4.0

- Add /usr/local/spark, /opt/spark to common search path
- Fix add_packages, add_jar when PYSPARK_SUBMIT_ARGS is undefined or or both are called

## 1.3.0

- Add /usr/lib/spark to common search path (Amazon EMR)

## 1.2.0

- Add `findspark.add_jars`
- Preserve PYSPARK_PYTHON env, if specified

## 1.1.0

- Add `findspark.add_packages`


## 1.0.0

First release
