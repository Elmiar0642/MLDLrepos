#Libraries Used.......................
import pyodbc
'''
Using Pyodbc we make connection to the MS-SSMS to get access to the database in our server.
'''
def make_connection():
    conn = pyodbc.connect('Driver={SQL Server};'
                                      'Server=ASINMDLB6P5T72;'
                                      'Database=coats_wba_p4i_hk;'
                                      'Trusted_Connection=yes;')
    return(conn)
if __name__=="__main__":
    print("DELPHI CONNECTION SCRIPT")
