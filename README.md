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

Findspark can add a startup file to the current IPython profile so that the enviornment vaiables will be properly set and pyspark will be imported upon IPython startup. This file is created when `edit_profile` is set to true. A profile other than the current one can be modified using the `profile_name` option.

```ipython --profile=myprofile
findspark.init('/path/to/spark_home', edit_profile=True)
findspark.init('/path/to/spark_home', edit_profile=True, profile_name='otherprofile')
```

Findspark can also add to .bashrc and .cshrc configuration files so that the enviornment variables will be properly set whenever a new shell is opened. This is enabled by setting the optional argument `persist_changes` to true.

```python
findspark.init('/path/to/spark_home, 'edit_rc=True)
```

If changes are persisted, findspark will not need to be called again unless the spark installation is moved.
