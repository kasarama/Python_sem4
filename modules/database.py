import mysql.connector as mysql
from modules.classes import Car, User, DataBaseException

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
    
    drop_users=('DROP TABLE IF EXISTS users;')
    create_users='create table users(user_name varchar(100) not null, password varchar(100) not null, primary key(user_name));'
    
    drop_cars=('DROP TABLE IF EXISTS cars;')
    create_cars='create table cars(car_id int not null auto_increment, model varchar(100) not null, fuel varchar(100) not null, year int not null, km int not null, capacity float not null, estimated_price int not null, sale_price int not null, owner varchar(100) not null REFERENCES users(user_name), primary key(car_id));'
    
    cursor.execute(drop_query)

    cursor.execute(table_query)    
    
    cursor.execute(drop_users)
    cursor.execute(create_users)    
    
    cursor.execute(drop_cars)
    cursor.execute(create_cars)    

    # Commit the changes
    cnx.commit()
    cursor.close()
    cnx.close()
    
    print('Setup completed')




def add_new(car,user_name):
    try:
        cnx = mysql.connect(host = "db", user = "root", passwd = "root", db = "db")
        car['owner']=user_name
        cursor = cnx.cursor()
        query = "INSERT INTO cars VALUES (%(car_id)s,%(model)s,%(fuel)s,%(year)s,%(km)s,%(capacity)s,%(estimated_price)s,%(sale_price)s,%(owner)s);"
        cursor.execute(query,car)
        car['car_id']=cursor.lastrowid

        cnx.commit()
        
        cursor.close()
        cnx.close()
        car_obj=Car(car['model'],car['fuel'],car['year'],car['km'],car['capacity'],car['estimated_price'],car['sale_price'],car['car_id'])
        return car, car_obj
    except Exception as e:
        print(e)
        raise DataBaseException("Saving the car aborted ")

def register_user(user_name, password):
    try:
        cnx = mysql.connect(host = "db", user = "root", passwd = "root", db = "db")
        
        cursor = cnx.cursor()
        query = "INSERT INTO users VALUES (%(user_name)s,%(password)s);"
        cursor.execute(query,{'user_name':user_name,'password':password})
        

        cnx.commit()
        
        cursor.close()
        cnx.close()
        user_obj=User(user_name,password)
        return {"user_name":user_name,"added":True}, user_obj
    except Exception as e:
        print(e)
        raise DataBaseException("Saving the user aborted ")
