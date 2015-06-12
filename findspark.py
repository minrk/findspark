"""Find spark home, and add pyspark to sys.path.

If SPARK_HOME is defined, it will be used to put pyspark on sys.path.
Otherwise, common locations for spark (currently only Homebrew's default) will be searched.
"""

import glob
import os
import sys

__version__ = '0.0.1'

def find_spark(spark_home=None):
    """Find spark and make pyspark importable.
    
    Ensures SPARK_HOME is set and adds pyspark's location inside SPARK_HOME to sys.path.
    
    Common
    """
    if not spark_home:
        spark_home = os.environ.get('SPARK_HOME', None)
    if not spark_home:
        for path in [
            '/usr/local/opt/apache-spark/libexec', # OS X Homebrew
            # Any other common places to look?
        ]:
            if os.path.exists(path):
                spark_home = path
                break
    
    if not spark_home:
        raise ValueError("Couldn't find spark, please specify spark_home arg or SPARK_HOME env.")
    
    # ensure SPARK_HOME is defined
    os.environ['SPARK_HOME'] = spark_home
    # add pyspark to sys.path
    spark_python = os.path.join(spark_home, 'python')
    py4j = glob(os.path.join(spark_python, 'lib', 'py4j-*.zip'))[0]
    sys.path[:0] = [spark_python, py4j]
    
    return spark_home
        