import psycopg2
DATABASE = DATABASE = {'dbname':"dfmirrdfr3rn0s",
			'user':"yvjqxthpshyvnq",
			'password':"48bdc442512a8e66b104e33701aec72627f883fa43fa6573c02a1fe29d492e1b",
			'host':"ec2-54-247-78-30.eu-west-1.compute.amazonaws.com",
			'port':"5432" 
}

class Sqlopen:
	def __init__(self):
		self.connection = psycopg2.connect(
				dbname=DATABASE["dbname"],
				user=DATABASE["user"],
				password=DATABASE["password"],
				host=DATABASE["host"],
				port=DATABASE["port"])
		self.cursor = self.connection.cursor()

	
	def create_table(self, table):
		self.cursor.execute(f'CREATE TABLE "{str(table)}" (Subject Text, Numbers Text)')

		self.connection.commit()
	def add_data(self, table, text):
		self.cursor.execute(f'INSERT INTO {str(table)} VALUES ({str(text)})')
		self.connection.commit()	
	def add_chanell(self, table, chanell):
		self.cursor.execute(f'INSERT INTO {str(table)} VALUES ({str(chanell)})')
	
		self.connection.commit()
	def returner(self, data):
		self.cursor.execute(f'SELECT * FROM "{str(data)}"')
		return self.cursor.fetchall()

	def deleter(self, data, category, info):
		self.cursor.execute(f"DELETE FROM '{str(data)}' WHERE {str(category)} = '{str(info)}'")
		self.connection.commit()


		