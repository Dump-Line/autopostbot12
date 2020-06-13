import sqlite3


class Sqlopen:
	def __init__(self, base):
		self.connection = sqlite3.connect(base)
		self.cursor = self.connection.cursor()
	
	def create_table(self, table):
		self.cursor.execute(f'CREATE TABLE "{str(table)}" (Subject Text, Numbers Text)')

		self.connection.commit()
	def add_data(self, table, text):
		self.cursor.execute(f'INSERT INTO "{str(table)}" VALUES ("{str(text)}")')
		self.connection.commit()	
#def add_data_text(self, table, text):
#		self.cursor.execute(f'INSERT INTO "{str(table)}" VALUES ("{str(text)}")')

	def add_chanell(self, table, chanell):
		self.cursor.execute(f'INSERT INTO "{str(table)}" VALUES ("{str(chanell)}")')
	
		self.connection.commit()
	def returner(self, data):
		self.cursor.execute(f'SELECT * FROM "{str(data)}"')
		return self.cursor.fetchall()

	def deleter(self, data, category, info):
		self.cursor.execute(f"DELETE FROM '{str(data)}' WHERE {str(category)} = '{str(info)}'")
		self.connection.commit()


		