#Libraries Used.......................
from connection import *

'''
We have used the table named "coats_wba_p4i_hk.dbo.TABLE_FOR_ANALYTICS" in our server.
The table has been created from extracting data from two of the existing tables,namely,"coats_wba_p4i_hk.dbo.coats_bulk_orders" and "coats_wba_p4i_hk.dbo.coats_bulk_order_lines".
The only connection between these two tables are, "id" column from "coats_wba_p4i_hk.dbo.coats_bulk_orders",to "oder_id" column from "coats_wba_p4i_hk.dbo.coats_bulk_order_lines".
The columns/index of the table are, ['customer_id','id','order_id','ordered_quantity','article_id','brand_id','ticket_id','length_id','finish_id','shade_id'].
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
    
