import mysql.connector as mysql


def commit_req(estimate_req):
    cnx = mysql.connect(host = "db", user = "root", passwd = "root", db = "db")
    cursor = cnx.cursor()



    estimate_req['model_id']=None
    print(estimate_req)
    
    
    insert_query='INSERT INTO estimate_req VALUES(%(model_id)s,%(Model)s,%(Coefficient)s,%(Intercept)s,%(Estimated_Price)s)'
    
    cursor.execute(insert_query,estimate_req)
    cnx.commit()
    cursor.close()
    cnx.close()

def setup_db():
    cnx = mysql.connect(host = "db", user = "root", passwd = "root", db = "db")


    cursor = cnx.cursor()
    drop_query=('DROP TABLE IF EXISTS estimate_req;')
    table_query='create table estimate_req(model_id int not null auto_increment, Model varchar(100) not null, Coefficient varchar(100), Intercept varchar(100), Estimated_Price varchar(100), primary key(model_id));'

    cursor.execute(drop_query)

    cursor.execute(table_query)    

    # Commit the changes
    cnx.commit()
    cursor.close()
    cnx.close()
    
    print('Setup completed')
