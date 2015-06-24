"""Find spark home, and initialize by adding pyspark to sys.path.

If SPARK_HOME is defined, it will be used to put pyspark on sys.path.
Otherwise, common locations for spark (currently only Homebrew's default) will be searched.
"""

from glob import glob
import os
import sys
import subprocess

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


def change_rc(spark_home, spark_python, py4j):
    """Persists changes to enviornment by changing shell config.

    Adds lines to .bashrc to set enviornment variables including
    the adding of dependencies to the system path. Currently only 
    works for Bash and (t)csh.

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
 

def edit_ipython_profile(spark_home, spark_python, py4j, name):
    """Creates or appends to an IPython profile to automatically import pyspark.
    
    Adds lines to the ipython_config file to be run at startup of the IPython
    interpreter for a given profile, creating the profile if it does not exist.
    These lines set appropriate enviornment variables and import the pyspark 
    library upon IPython startup.

    Parameters
    ----------
    spark_home : str
        Path to Spark installation.
    spark_python : str
        Path to python subdirectory of Spark installation.
    py4j : str
        Path to py4j library.
    name : str
        Name of profile to create or append to.
    """
    subprocess.call(["ipython", "profile", "create", name])

    config_dir = subprocess.check_output(["ipython", "profile", "locate", name]).strip()
    config_filename = os.path.join(config_dir, "ipython_config.py")
        
    with open(config_filename, 'a') as config_file:
        #Lines of code to be run when IPython starts
        lines = ["import sys, os"]
        lines.append("os.environ['SPARK_HOME'] = '" + spark_home + "'")
        lines.append("sys.path[:0] = " + str([spark_python, py4j]))
        lines.append("import pyspark")       

        #Code to be placed in config file
        config_file.write("\n#pyspark configuration added by findspark\n")
        config_file.write("to_exec = " + str(lines) + "\n")
        config_file.write("try:\n")
        config_file.write("    c.InteractiveShellApp.exec_lines[:0] = to_exec\n")
        config_file.write("except TypeError:\n")
        config_file.write("    c.InteractiveShellApp.exec_lines = to_exec\n")
        

def init(spark_home=None, edit_rc=False, edit_profile=False, profile_name='spark'):
    """Make pyspark importable.

    Sets environmental variables and adds dependencies to sys.path.
    If no Spark location is provided, will try to find an installation.

    Parameters
    ----------
    spark_home : str, optional, default = None
        Path to Spark installation, will try to find automatically
        if not provided
    edit_rc : bool, optional, default = False
        Whether to attempt to persist changes by appending to shell
        config.
    edit_profile : bool, optional, default = False
        Whether to create an IPython profile that atuomatically configures
        environment variables and imports spark.
    profile_name : bool, optional, default = "spark"
        Name of the IPython profile to create or edit if edit_profile is True.
    """

    if not spark_home:
        spark_home = find()

    # ensure SPARK_HOME is defined
    os.environ['SPARK_HOME'] = spark_home

    # add pyspark to sys.path
    spark_python = os.path.join(spark_home, 'python')
    py4j = glob(os.path.join(spark_python, 'lib', 'py4j-*.zip'))[0]
    sys.path[:0] = [spark_python, py4j]
    
    if edit_rc:
        change_rc(spark_home, spark_python, py4j) 
    
    if edit_profile:
        edit_ipython_profile(spark_home, spark_python, py4j, profile_name)
