from duct import Workspace

from IPython.core.magic import register_cell_magic
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import pandas as pd

if 'display' not in dir():
    from IPython.display import display

class WS_sqlalchemy(Workspace):
    """
    Workspace class from the pyodbc library

    Similar for other DSWS classes, the following class properties and methods are
    provided:
      - connection_url (property): a sqlalchemy URL based on pyodbc connection string
      - engine (property): a sqlalchemy engine based on pyodbc connection string
      - connection (property): a sqlalchemy connection based on pyodbc connection string
      - qry(run_cmd): executes a run command
      - table(): returns the entire table as a pandas dataframe
      - qry: precesses a proc sql query, the return type is dependent upon r_type requested:
        - df (default): pandas dataframe
        - disp: pretty html form of pandas dataframe
        - log: text output of query
        - df_log: tuple of df and text log

    Configuring a Saspy class is typically done through `dsws.duct`, but can also be
        evaluated as:
        ```python
        from dsws.ws_pyodbc import Pyodbc
        kwargs = {'odbc_connect':  spark.conf.get("spark.sas_url")}
        sas = Saspy(kwargs)
        ```
        SAS Sessions can time out, be aware that this happens, you will get a notice in terminal when
        it does happen and variables set in previous sessions will no longer be set."""

    _connection_url = None
    _engine = None
    _connection = None

    @property
    def connection_url(self):
        """SQL Alchemy connection URL"""
        # TODO: argument create protocol
        if not self._connection_url:
            self._connection_url = URL.create(**self._kwargs)
        return self._connection_url

    @property
    def engine(self):
        """SQL Alchemy engine"""
        if not self._connection_url:
            self._connection_url = URL.create(**self._kwargs)
        if not self._engine:
            self._engine = create_engine(self._connection_url)
        return self._engine

    @property
    def connection(self):
        """SQL Alchemy connection"""
        if not self._connection_url:
            self._connection_url = URL.create(**self._kwargs)
        if not self._engine:
            self._engine = create_engine(self._connection_url)
        if not self._connection:
            self._connection = self._engine.connect()
        return self._connection

    def qry(self, sql):
        # Create Pandas Dataframe from SAS SQL Statement
        return pd.read_sql(sql=text(sql), con=self.connection)

    def _register_magic(self):
        @register_cell_magic(self._handle)
        def qry_magic(line=None, cell=''):
            if not line:
                print ('Line commands are not evaluated.')
            display(self.qry(sql=cell))

        del qry_magic
