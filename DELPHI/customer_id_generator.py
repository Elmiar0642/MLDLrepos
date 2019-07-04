from connection import *

'''
'''

def customer_id_list(SQL_QUERY):
    cursor = make_connection().cursor()
    cursor.execute(SQL_QUERY)
    customer=[]*0
    for row in cursor:
        customer.append(row[0])
    return(customer)
if __name__=="__main__":
    print("DELPHI CUSTOMER ID GENERATOR SCRIPT")
    
