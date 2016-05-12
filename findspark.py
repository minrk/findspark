"""Find spark home, and initialize by adding pyspark to sys.path.

If SPARK_HOME is defined, it will be used to put pyspark on sys.path.
Otherwise, common locations for spark (currently only Homebrew's default) will be searched.
"""

from glob import glob
import os
import sys

__version__ = '1.0.0'


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


def change_rc(spark_home, spark_python, py4j):
    """Persists changes to environment by changing shell config.

    Adds lines to .bashrc to set environment variables 
    including the adding of dependencies to the system path. Will only
    edit this file if they already exist. Currently only works for bash.

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

    if os.path.isfile(bashrc_location):
        with open(bashrc_location, 'a') as bashrc:
            bashrc.write("\n# Added by findspark\n")
            bashrc.write("export SPARK_HOME=" + spark_home + "\n")
            bashrc.write("export PYTHONPATH=" + spark_python + ":" + 
                         py4j + ":$PYTHONPATH\n\n")
    

def edit_ipython_profile(spark_home, spark_python, py4j):
    """Adds a startup file to the current IPython profile to import pyspark.
    
    The startup file sets the required environment variables and imports pyspark.

    Parameters
    ----------
    spark_home : str
        Path to Spark installation.
    spark_python : str
        Path to python subdirectory of Spark installation.
    py4j : str
        Path to py4j library.
    """
    from IPython import get_ipython
    ip = get_ipython()

    if ip:
        profile_dir = ip.profile_dir.location
    else:
        from IPython.utils.path import locate_profile
        profile_dir = locate_profile()

    startup_file_loc = os.path.join(profile_dir, "startup", "findspark.py")
        
    with open(startup_file_loc, 'w') as startup_file:
        #Lines of code to be run when IPython starts
        startup_file.write("import sys, os\n")
        startup_file.write("os.environ['SPARK_HOME'] = '" + spark_home + "'\n")
        startup_file.write("sys.path[:0] = " + str([spark_python, py4j]) + "\n")
        startup_file.write("import pyspark\n")       
        

def init(spark_home=None, python_path=None, edit_rc=False, edit_profile=False):
    """Make pyspark importable.

    Sets environment variables and adds dependencies to sys.path.
    If no Spark location is provided, will try to find an installation.

    Parameters
    ----------
    spark_home : str, optional, default = None
        Path to Spark installation, will try to find automatically
        if not provided.
    python_path : str, optional, default = None
        Path to Python for Spark workers (PYSPARK_PYTHON),
        will use the currently running Python if not provided.
    edit_rc : bool, optional, default = False
        Whether to attempt to persist changes by appending to shell
        config.
    edit_profile : bool, optional, default = False
        Whether to create an IPython startup file to automatically
        configure and import pyspark.
    """

    if not spark_home:
        spark_home = find()

    if not python_path:
        python_path = sys.executable

    # ensure SPARK_HOME is defined
    os.environ['SPARK_HOME'] = spark_home

    # ensure PYSPARK_PYTHON is defined
    os.environ['PYSPARK_PYTHON'] = python_path

    # add pyspark to sys.path
    spark_python = os.path.join(spark_home, 'python')
    py4j = glob(os.path.join(spark_python, 'lib', 'py4j-*.zip'))[0]
    sys.path[:0] = [spark_python, py4j]
    
    if edit_rc:
        change_rc(spark_home, spark_python, py4j) 
    
    if edit_profile:
        edit_ipython_profile(spark_home, spark_python, py4j)
