# Find spark

PySpark isn't on sys.path by default, but that doesn't mean it can't be used as a regular library.
You can address this by either symlinking pyspark into your site-packages,
or adding pyspark to sys.path at runtime. `findspark` does the latter.

To initialize PySpark, just call

```python
import findspark
findspark.init()

import pyspark
sc = pyspark.SparkContext(appName="myAppName")
```

Without any arguments, the SPARK_HOME environmental variable will be used,
and if that isn't set, other possible install locations will be checked. If
you've installed spark with

    brew install apache-spark

on OS X, the location `/usr/local/opt/apache-spark/libexec` will be searched.

Alternatively, you can specify a location with the `spark_home` argument.

```python
findspark.init('/path/to/spark_home')
```

To verify the automatically detected location, call

```python
findspark.find()
```