'''
Created on 2022-06-11
@author: wf
'''
import time
from functional_dependencies.BCNF import FunctionalDependencySet
from lodstorage.sql import SQLDB

class FDCheck:
    '''
    check functional dependencies for a tabular dataset in list of dicts form
    '''
    
    def __init__(self,lod:list,debug:bool=False):
        '''
        construct me with the given list of dicts
        
        Args:
            lod(list): the list of dicts (table) to check
            debug(bool): if true switch on debugging
        '''
        self.lod=lod
        self.debug=debug
        self.entityInfo=None
        
    def createDatabase(self,entityName,primaryKey=None,executeMany=True,fixNone=False,fixDates=False,debug=False,doClose=True):
        '''
        create a database for my list of Records
        
        Args:     
           entityName(string): the name of the entity type to be used as a table name
           primaryKey(string): the name of the key / column to be used as a primary key
           executeMany(boolean): True if executeMany mode of sqlite3 should be used
           fixNone(boolean): fix dict entries that are undefined to have a "None" entry
           debug(boolean): True if debug information e.g. CREATE TABLE and INSERT INTO commands should be shown
           doClose(boolean): True if the connection should be closed
      
        '''     
        size=len(self.lod)
        if self.debug:
            print("%s size is %d fixNone is %r fixDates is: %r" % (entityName,size,fixNone,fixDates))
        self.sqlDB=SQLDB(debug=debug,errorDebug=True)
        entityInfo=self.sqlDB.createTable(self.lod,entityName,primaryKey)
        startTime=time.time()
        self.sqlDB.store(self.lod,entityInfo,executeMany=executeMany,fixNone=fixNone)
        elapsed=0.000000000001 if time.time()-startTime == 0 else time.time()-startTime
        if self.debug:
            print ("adding %d %s records took %5.3f s => %5.f records/s" % (size,entityName,elapsed,size/elapsed)) 
        if self.debug:
            resultList=self.sqlDB.queryAll(entityInfo,fixDates=fixDates)    
            print ("selecting %d %s records took %5.3f s => %5.f records/s" % (len(resultList),entityName,elapsed,len(resultList)/elapsed)) 
        if doClose:
            self.sqlDB.close()
        self.entityInfo=entityInfo
        return entityInfo    
    
    def findFDs(self):
        '''
          find functional dependencies 
          
          https://github.com/gustavclausen/functional-dependency-finder/blob/master/main.py
          Return:
              FunctionalDependencySet: the set of functional dependencies
        '''
        if self.entityInfo is None:
            raise Exception("createDataBase needed to supply entityInfo")
        fields = list(self.entityInfo.typeMap.keys())
        table_name=self.entityInfo.name
        fds=FunctionalDependencySet()
        for i,field in enumerate(fields) :
            attr1_var=chr(ord('A')+i)
            fds.add_attribute(attr1_var, field)
        for i,field in enumerate(fields) :
            attr1_var=chr(ord('A')+i)      
            for j in range(0, len(fields)):
                if (i == j):
                    continue
    
                field_1 = fields[i]
                field_2 = fields[j]
                attr2_var=chr(ord('A')+j)
                sql=f'SELECT {field_1}, COUNT(DISTINCT {field_2}) c FROM {table_name} GROUP BY {field_1} HAVING c > 1'
                hits=self.sqlDB.query(sql)
                if self.debug:
                    print (f"{sql}\n{hits}")
                
                if len(hits)==0:
                    # Functional dependency found: it's not the case that there's more than one value (field_2)
                    # associated with field_1
                    fds.add_dependency(attr1_var,attr2_var)
        self.fds=fds
        return fds
        
        
        
        