import psycopg2

DATABASE = {'dbname':"dfmirrdfr3rn0s",
            'user':"yvjqxthpshyvnq",
            'password':"48bdc442512a8e66b104e33701aec72627f883fa43fa6573c02a1fe29d492e1b",
            'host':"ec2-54-247-78-30.eu-west-1.compute.amazonaws.com",
            'port':"5432"} 

connection = psycopg2.connect(
                dbname=DATABASE["dbname"],
                user=DATABASE["user"],
                password=DATABASE["password"],
                host=DATABASE["host"],
                port=DATABASE["port"])



cursor = connection.cursor()



sql = """CREATE TABLE "admins" (id  INTEGER);
    CREATE TABLE chanel (chanels_id  INTEGER);
    CREATE TABLE data (message  TEXT);
    """





with connection:
      cursor.execute(sql)
      connection.commit()