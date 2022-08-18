from typing import Union
import sqlite3
class MyPostDataBase(object):
	def __init__(self):
		self.posts = [
		{"title": "Title 1", "content": "Content 1", "id": 1},
		{"title": "Title 2", "content": "Content 2", "id": 2}
		]
		self.databasename = "./fastapi.db"
		self.connection = sqlite3.connect(self.databasename)
		cursor = self.connection.cursor()
		command2 = """CREATE TABLE IF NOT EXISTS products(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name VARCHAR NOT NULL,
			price INT NOT NULL,
			is_sale BOOL DEFAULT 0,
			inverntory INTEGER NOT NULL DEFAULT 0,
			created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
		);"""
		self.insert_command = 'INSERT INTO products(name, price, is_sale)VALUES(?, ?, ?);'
		self.fetch_all_command = 'SELECT * FROM products'
		cursor.execute(command2)
		cursor.execute(self.insert_command, ('abc', 10, True))
		output = cursor.execute(self.fetch_all_command)
		print(output.fetchall())
		self.connection.commit()


	def store(self, data: dict):
		self.posts.append(data)
		return self

	def __call__(self) -> dict:
		return self.posts


	def find_post(self, idx: int) -> Union[dict, None]:
		a = next((x for x in self.posts if x["id"] == idx), None)
		return a

	def delete_post(self, idx:int) -> bool:
		for i, p in enumerate(self.posts):
			if p['id'] == idx:
				self.posts.pop(i)
				return True
		return False

	def update_post(self, idx:int, post: dict) -> bool:
		for i, p in enumerate(self.posts):
			if p['id'] == idx:
				self.posts[i] = post
				return True
		return False
