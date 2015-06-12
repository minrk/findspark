# Find spark

PySpark isn't on sys.path by default, but that doesn't mean it can't be used as a regular library.
You can address this by either symlinking pyspark into your site-packages,
or adding pyspark to sys.path at runtime. `findspark` does the latter.

This provides one function:

```python
import findspark
findspark.find_spark()

import pyspark
sc = pyspark.SparkContext(appName="myAppName")
```

If SPARK_HOME env is set, you don't need to pass any args.
You can pass a path to spark_home to find_spark,
and it will set SPARK_HOME:

```python
findspark.find_spark('/path/to/spark_home')
```

If you've installed spark with

    brew install apache-spark

on OS X, the default location of `/usr/local/opt/apache-spark/libexec` will be searched
if SPARK_HOME is not already set.