import os
import sys
import subprocess
import tempfile
import sqlalchemy as sa
import pandas as pd


class YbConnector:
    """ A pytezza-esque connector to Yellowbrick. """
    def __init__(self,host,db,user,pw="",psql_compatible_version='13.7'):
        """ """
        self.host=host
        self.db=db
        self.user=user
        
        self.pw=pw
        if not pw:
          self.pw=os.environ.get('YBPASSWORD')
        
        self.psql_compatible_version=psql_compatible_version
        self.dry_run_mode=False
        self.engine=None
        self.connection=self.getConnection()
    
    def __del__(self):
        if hasattr(self,"connection"):
            try:
                self.disconnect()
            except:
                pass
        return
    
    def __repr__(self):
        """ """
        stat="CONNECTED"
        try:
            self.connection.execute("select 1")
        except:
            stat="DISCONNECTED"
            
        return(f"Yellowbrick connector for user {self.user} on host {self.host}.\n{stat}")
    
    def _checkConnection(self,reconnect=False):
        """ When using psycopg2 interactively, it's not unusual for the db
            connection to become invalid due to idle timeout.  Before issuing
            a query, check the connection and optionally reconnect if needed.
        """
        try:
            self.connection.execute("select 1")
        except Exception as e:
            if reconnect:
                self.disconnect()
                self.connection=self.getConnection()
            else:
                raise Exception("Connection problem: %s"%e, sys.exc_info()[2])
        
    def getEngine(self):
        """ """
        self._checkConnection()
        return self.engine
    
    def getConnection(self):
        """ """
        from sqlalchemy.dialects.postgresql.base import PGDialect
        psql_vinfo=tuple([int(x) for x in self.psql_compatible_version.split(".")])
        PGDialect._get_server_version_info = lambda *args:psql_vinfo
        
        connection_url = sa.engine.URL.create(
            drivername="postgresql+psycopg2",
            username=self.user,
            password=self.pw,
            host=self.host,
            database=self.db,
        )
        
        try:
            self.engine=sa.create_engine(connection_url,pool_pre_ping=True)
            conn=self.engine.connect().execution_options(isolation_level="AUTOCOMMIT")
            return conn
        except Exception as details:
            print("Error connecting using:",(self.host,self.db,self.user,self.pw))
            print(">>> ",details)
            sys.exit()
    
    def disconnect(self):
        """ """
        if self.connection:
            self.connection.close()
        return
    
    def query(self,query_to_run,dryRun=False,dumpTo=None,dumpAppend=False,printQuery=False):
        """ Query implies fetch data. """
        return self._query(query_to_run,withData=True,dryRun=dryRun,dumpTo=dumpTo,dumpAppend=dumpAppend,printQuery=printQuery)
        
    def execute(self,query_to_run,dryRun=False,dumpTo=None,dumpAppend=False,printQuery=False):
        """ Execute implies don't fetch data. """
        return self._query(query_to_run,withData=False,dryRun=dryRun,dumpTo=dumpTo,dumpAppend=dumpAppend,printQuery=printQuery)
    
    def _query(self,query_to_run,withResults=False,withData=False,dryRun=False,dumpTo=None,dumpAppend=False,printQuery=False):
        """ Query Yellowbrick, optionally returning a dataframe of results. """
        self._checkConnection(reconnect=True)
        
        df=None
        if dumpTo:
            mode="a+" if dumpAppend else "w+"
            open(os.path.join(".",dumpTo),mode).write(query_to_run)
        
        if dryRun:
            print("This is a dry run.  Not submitting:\n")
            print(query_to_run)
            return
        
        if printQuery:
            print(query_to_run)
        
        #withResults and withData are identical; phasing out the withResults.
        #In case of a conflict, err on the side of returning data.
        withData=max(withResults,withData)
        
        #Connect and execute, with or without returning results.  If there's a problem
        #print the details, and always close the connection.
        try:
            if withData:
                df=pd.read_sql(query_to_run,self.getEngine())
            else:
                self.connection.execute(query_to_run)
        except Exception as d:
            print("There was an error while executing the SQL:\n",d)
            sys.exit()
        
        return df
    
    def tableExists(self,table):
        """ """
        (db,tbl)=table.split(".")
        q=f"""
            select count(*) as rc
            from information_schema.tables
            where upper(table_schema)=upper('{db}')
              and upper(table_name)=upper('{tbl}')
        """
        d=self.query(q)
        return d.rc[0]>0
    
    def tableRowCount(self,table):
        """ """
        q=f"""
            select count(*) as rc
            from {table}
        """
        d=self.query(q)
        return d.rc[0]
    
    def sample(self,table,fields=None,limit=10,orderby=None):
       """ """
       h="Sample of "+table
       print(h+"\n"+("-"*len(h)))
       return self.query(f"select {fields if fields else '*'} from {table} order by {orderby if orderby else 'random()'} limit {limit}")
    
    
    def getDfDDL(self,src,ybTypes=None):
        """ """
        if not ybTypes:
            #If were weren't supplied types, guess them ourselves.
            ybTypes=self.getYbTypesFromDf(src)
            
        ddl = ""
        for i in range(len(src.columns)):
            #New DDL line for each element.  Trickiness to handle no-comma for last element.
            ddl+='    "%s" %s%s\n'%(src.columns[i],ybTypes[i],(i<len(src.columns)-1)*",")
            
        return ddl

    def dfToYb(self,src,target,distribute_on="random",clobber=False,ybTypes=None,verbose=False,ignoreLoadErrors=False):
        """ Given a pandas df, push that table to yellowbrick, optionally replace the existing table in yellowbrick.
            If ybTypes immutable is provided, use those types and to hell with the consequences.
            Otherwise, infer the types.
        """
        
        def vprint(s):
            if verbose:
                print(s)
        
        print(f"Loading {src.shape[0]} rows and {src.shape[1]} columns into {target}.")
        vprint(f"Here is a sample of the source data:\n{src.head(5)}")
        
        if not ybTypes:
            #If were weren't supplied types, guess them ourselves.
            ybTypes=self.getYbTypesFromDf(src)
        
        if clobber:
            vprint(f"Dropping {target}.")
            self.execute(f"drop table if exists {target};")
        
        maxbad="0"
        if ignoreLoadErrors:
            maxbad="-1"
        
        ddl = self.getDfDDL(src,ybTypes)
        
        dump=tempfile.mkstemp(".csv")[1]
        vprint(f"Dumping local data to {dump}")
        src.to_csv(dump,index=False,header=True,lineterminator="\n")
        vprint(f"Dumped {os.path.getsize(dump)/1024/1024:0.2f}MB.")
        
        if not self.tableExists(target):
            self.execute(f"""
                create table {target} (
                    {ddl}
                )
                ;
            """,printQuery=verbose)
        
        os.environ["YBPASSWORD"]=self.pw
        cmd=rf'"C:\Program Files\Yellowbrick Data\Client Tools\bin\ybload.exe" --host {self.host} --username {self.user} --dbname {self.db} --max-bad-rows {maxbad} --csv-skip-header-line true --table {target} {dump}'
        vprint(f"Running this now ===> {cmd}")
        
        try:
            _=subprocess.call(cmd)
        except Exception as details:
            print(f"There was a problem running ybload.  Make sure it's installed, is on your PATH, and that Java is installed:\n{details}\n")
            sys.exit(1)
        
        lrows = self.tableRowCount(target)
        if len(src)==lrows or clobber==False:
            print("YBload successful")
            vprint(f"Dumped {len(src)} rows, and then loaded {lrows} rows.")
        else:
            print("THERE MIGHT HAVE BEEN A PROBLEM LOADING!  The number of rows loaded doesn't match the input length.  Check the output.")
        
        return
    
    #Alias
    df2Yb=dfToYb
    
    def getYbTypesFromDf(self,df):
        """ Try to map.  This is almost vulgar.
            Return a tuple the same size as dftypes."""
        default_yb = "varchar(255)"
        df2yb = {'int64':'bigint',
                 'int32':'bigint',
                 'float64':'float',
                 'float32':'float',
                 'object':'varchar(1024)'}
        ybtypes = []
        for t in df.dtypes:
            ybtypes.append(df2yb.get(t.name,default_yb))
        return(tuple(ybtypes))



def test(timeouttest=False):
    """ """
    YB = YbConnector("ybr-01.eyc.com","dbo","clevis")
    tt = "geatstanl.cjl_test"
    if YB.tableExists(tt):
        print(f"{tt} already exists.  Dropping.")
        YB.query(f"drop table {tt}")
    
    YB.query(f"create table {tt} as select 1 one,current_timestamp as ts")
    d=YB.query("select * from %s"%tt,withData=True)
    print(type(d))
    print(d)
    
    data=pd.read_csv(r"C:\temp\ptest.csv")
    YB.dfToYb(data,"geatstanl.cjltest",clobber=True)
    d=YB.query("select * from geatstanl.cjltest",withData=True)
    d.head()
    print(len(d))
    
    if timeouttest:
        import time
        mins=12
        print(f"Make some tea.  This will run for {mins} minutes.")
        time.sleep(mins*60)
        print(YB.query("select current_timestamp",withData=True))
    

if __name__=="__main__":
    pass

