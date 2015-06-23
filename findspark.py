"""Find spark home, and initialize by adding pyspark to sys.path.

If SPARK_HOME is defined, it will be used to put pyspark on sys.path.
Otherwise, common locations for spark (currently only Homebrew's default) will be searched.
"""

from glob import glob
import os
import sys

__version__ = '0.0.4'


def find():
    """Find a local spark installation.

    Will first check the SPARK_HOME env variable, and otherwise
    search common installation locations, e.g. from homebrew
    """
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
        raise ValueError("Couldn't find Spark, make sure SPARK_HOME env is set"
                         " or Spark is in an expected location (e.g. from homebrew installation).")

    return spark_home


def persist(spark_home, spark_python, py4j):
    """Persists changes to enviornment.

    Adds lines to .bashrc to set enviornment variables including
    the adding of dependencies to the system path. Currently only 
    works for Bash.

    Parameters
    ----------
    spark_home : str
        Path to Spark installation.
    spark_python : str
        Path to python subdirectory of Spark installation.
    py4j : str
        Path to py4j library.
    """

    bashrc_location = os.path.expanduser("~/.bashrc")

    with open(bashrc_location, 'a') as bashrc:
        bashrc.write("\n# Added by findspark\n")
        bashrc.write("export SPARK_HOME=" + spark_home + "\n")
        bashrc.write("export PYTHONPATH=" + spark_python + ":" + 
                     py4j + ":$PYTHONPATH\n\n")
    
    cshrc_location = os.path.expanduser("~/.cshrc")
    
    with open(cshrc_location, 'a') as cshrc:
        cshrc.write("\n# Added by findspark\n")
        cshrc.write("setenv SPARK_HOME " + spark_home + "\n")
        cshrc.write("setenv PYTHONPATH \"" + spark_python + ":" +
                    py4j + ":\"$PYTHONPATH")
 


def init(spark_home=None, persist_changes=False):
    """Make pyspark importable.

    Sets environmental variables and adds dependencies to sys.path.
    If no Spark location is provided, will try to find an installation.

    Parameters
    ----------
    spark_home : str, optional, default = None
        Path to Spark installation, will try to find automatically
        if not provided
    persist_changes : bool, optional, default = False
        Whether to attempt to persist changes (currently only by
        appending to bashrc).
    """

    if not spark_home:
        spark_home = find()

    # ensure SPARK_HOME is defined
    os.environ['SPARK_HOME'] = spark_home

    # add pyspark to sys.path
    spark_python = os.path.join(spark_home, 'python')
    py4j = glob(os.path.join(spark_python, 'lib', 'py4j-*.zip'))[0]
    sys.path[:0] = [spark_python, py4j]
    
    if persist_changes:
        persist(spark_home, spark_python, py4j) 
