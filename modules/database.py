import mysql.connector as mysql
from modules.classes import Car, DataBaseException

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
    drop_cars=('DROP TABLE IF EXISTS cars;')
    create_cars='create table cars(car_id int not null auto_increment, model varchar(100) not null, fuel varchar(100) not null, year int not null, km int not null, capacity float not null, estimated_price int not null, sale_price int not null, primary key(car_id));'
    
    cursor.execute(drop_query)

    cursor.execute(table_query)    
    
    cursor.execute(drop_cars)
    cursor.execute(create_cars)    

    # Commit the changes
    cnx.commit()
    cursor.close()
    cnx.close()
    
    print('Setup completed')



def add_new(car):
    try:
        cnx = mysql.connect(host = "db", user = "root", passwd = "root", db = "db")
        cursor = cnx.cursor()
        query = "INSERT INTO cars VALUES (%(car_id)s,%(model)s,%(fuel)s,%(year)s,%(km)s,%(capacity)s,%(estimated_price)s,%(sale_price)s);"
        re = cursor.execute(query,car)
        car['car_id']=cursor.lastrowid
        cnx.commit()
        print("\n\n result of cursor. excute: \n" , re,  '\n\n')
        cursor.close()
        cnx.close()
        car_obj=Car(car['model'],car['fuel'],car['year'],car['km'],car['capacity'],car['estimated_price'],car['sale_price'],car['car_id'])
        return car, car_obj
    except Error as e:
        raise DataBaseException("Saving the car aborted ")

