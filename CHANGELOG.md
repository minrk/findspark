# Changes in findspark

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
