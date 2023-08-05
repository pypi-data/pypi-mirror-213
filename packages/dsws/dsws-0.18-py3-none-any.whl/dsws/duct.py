"""
Data Science Work Space - Duct

Duct provides a single class object that is intended to consolidate
all analytical source data connection patterns.
'duct' was deliberately chosen to consolidate the collection of connection
components, but avoid names like pipe, connection, stream to avoid naming
confusion as well as to not limit the types of work space components included

"""

from IPython.core.magic import register_cell_magic
from abc import ABC, abstractmethod
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.readwriter import DataFrameReader, DataFrameWriter
import pathlib
import re
import subprocess


if 'display' not in dir():
    from IPython.display import display

if 'displayHTML' not in dir():
    from IPython.core.display import HTML
    from IPython.display import display
    def displayHTML(html):
        display(HTML(html))

class Alias:
    """Class used within CommandLineInterface to handle dynamic alias"""

    def __init__(self, alias, command, url, picker):
        self.alias = alias
        self._command = command
        self._url = url
        self._picker = picker

    def set_default(self):
        with open(self._picker, "w") as f:
            f.write("clear\n")
            f.write(self.alias + "\n")

    def launch(self):
        if not self._url:
            print('url is not set')
            return
        """NOTE: running launch will also set default"""
        self.set_default()
        script = '''<script type="text/Javascript">const sleep = async (milliseconds) => {
                  await new Promise(resolve => {return setTimeout(resolve, milliseconds)});};
                  if (0 <1) {window.open("%s");};sleep(5000);</script>''' % self._url
        displayHTML(script)

class CommandLineInterface:
    """Optional Class to create one or more aliases for workspace connector"""

    def __init__(self, startup_file: str, *aliases: {}):
        """Init will add aliases terminal startup
        startup_file is where all aliases will be set.
        Each alias will be a dict:
        startup_file
        [{"alias": <name of the alias to be used in terminal>,
          "command": <string of command to be used in alias>,}, ...]
        """
        self._startup_file = pathlib.Path(startup_file)
        self._picker = self._startup_file.parent.joinpath('.picker')
        with open(self._startup_file, 'r') as f:
            startup_txt = f.read()
        for a in list(aliases):
            if len(re.findall(f"alias {a['alias']}=", startup_txt)) == 0:
                with open(self._startup_file, "a") as f:
                    f.write(f"alias {a['alias']}='{a['command']}'\n")
            setattr(self, str(a['alias']).replace('-', '_'),
                    Alias(alias=a['alias'],
                          command=a['command'],
                          url=None,
                          picker=self._picker))

        # add startup command to run picker
        subprocess.run(["touch", self._picker])
        with open(self._startup_file, "a") as f:
            f.write(f"source {self._picker}\n")

    def unset_default(self):
        with open(self._picker, "w") as f:
            f.write('')


class SparkJDBC:
    """Optional Class addition to Workspace that provides methods to interface with Spark via JDBC
    There are three methods and one property:
        jdbc_reader (property):
        jdbc_table (method):
        jdbc_qry (method):
        jdbc_writer (method):
    """

    _reader: DataFrameReader = None

    def __init__(self, kwargs: dict, handle=None):
        self._kwargs = kwargs
        self._handle = handle
        self._register_magic()

    @property
    def reader(self) -> DataFrameReader:
        if not self._reader:
            self._reader = SparkSession.builder.getOrCreate().read.format("jdbc").options(**self._kwargs)
        return self._reader

    def table(self, table: str) -> DataFrame:
        return self.reader.option("dbtable", table).load()

    def qry(self, sql: str) -> DataFrame:
        return self.reader.option("query", sql).load()

    def writer(self, src: DataFrame, tgt: str) -> DataFrameWriter:
        return src.write.format('jdbc') \
            .options(**self._kwargs) \
            .option("dbtable", tgt)

    def _register_magic(self):
        @register_cell_magic(self._handle + '_spark')
        def spark_jdbc_qry_magic(line=None, cell=''):
            if not line:
                print ('Line commands are not evaluated.')
            display(self.qry(sql=cell))

        del spark_jdbc_qry_magic


class Workspace(ABC):
    """
    Workspace - base class for all three workspace types:
       - client (remote client session)
       - session (locally instantiated session)
       - connection (open connection to a long-lived service)
    """
    _kwargs: dict = {}
    _handle = None
    _commandLineInterface: CommandLineInterface = None
    _sparkJDBC: SparkJDBC = None

    def __init__(self, kwargs, handle=None, spark_jdbc=None, cli_aliases=None):
        """
        kwargs are a dict of all necessary configurations for
        command, if provided, is the commandline used for terminal sessions
        """
        if spark_jdbc: self.spark_jdbc = SparkJDBC(spark_jdbc, handle)
        if cli_aliases: self.cli = CommandLineInterface(cli_aliases['startup_file'], *cli_aliases['aliases'])
        self._kwargs = kwargs
        self._handle = handle
        self._register_magic()

    @abstractmethod
    def _register_magic(self):
        """ Base code to register cell magics"""
        pass

class Duct:
    """
    Duct - A single entry class for all workspaces to be configured within.

    In addition to just being a container class, duct provides a way to display all configured functionality
    via the show_workspaces() method. This is important because it will not only list all available magics
    and aliases, but it provides a hyperlink to a web-terminal which will a common interactive pattern for users.

    During instantiation the workspaces are defined as well as
    magics are created according to dsws conventions:
     - An un-argumented magic launches a cli session
     - An argumented magic accepts sql and returns
     a display of results. Intended for very concise
     iterations or summary results.
    """
    def __init__(self, duct_ws:{str: Workspace}=None):
        self.ws = duct_ws
        for k, v in self.ws.items():
            setattr(self, k, v)
