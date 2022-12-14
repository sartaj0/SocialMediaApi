
from typing import Union
import time
import sqlite3


class MyPostDataBase(object):
	def __init__(self):
		
		self.databasename = "./fastapi.db"
		while True:
			try:
				self.connection = sqlite3.connect(self.databasename, check_same_thread=False)
				self.cursor = self.connection.cursor()
				print("Database Connection Successfully")
				break

			except Exception as e:
				print("Connecting Databse Failed")
				print("Error:", e)
			time.sleep(2)


		command = """
			DROP TABLE IF EXISTS posts;

			CREATE TABLE IF NOT EXISTS posts(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			title VARCHAR NOT NULL,
			content VARCHAR NOT NULL,
			published BOOLEAN NOT NULL DEFAULT TRUE,
			created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);

			INSERT INTO posts(title, content) VALUES ('1st title', '1st content'), ('2nd title', '2nd content');
			"""
		self.cursor.executescript(command)
		self.insert_command = "INSERT INTO posts (title, content, published) VALUES (?, ?, ?);"
		self.find_command = "SELECT * FROM posts where id=%s"
		self.connection.commit()


	def store(self, data: dict):
		self.posts.append(data)
		self.cursor.execute(self.insert_command, (data['title'], data['content'], data['published']))
		new_post = self.cursor.fetchone()
		return {"data": new_post}

	def __call__(self) -> dict:
		return self.posts

	def get_posts(self):
		response = self.cursor.execute("SELECT * FROM posts").fetchall()
		data = [dict(zip([c[0] for c in self.cursor.description], response[i])) for i in range(len(response))]
		
		return data


	def find_post(self, idx: int) -> Union[dict, None]:
		# a = next((x for x in self.posts if x["id"] == idx), None)
		try:
			self.cursor.execute("SELECT * FROM posts where id=?", str(idx))
			response = self.cursor.fetchone()
			data = dict(zip([c[0] for c in self.cursor.description], response))
		except Exception as e:
			return None

	def delete_post(self, idx:int) -> bool:
		result = self.cursor.execute("""DELETE FROM posts WHERE id=?""", (str(idx), )).fetchone()
		print(result, "result")
		self.connection.commit()
		return True

	def update_post(self, idx:int, post: dict) -> bool:
		self.cursor.execute("""UPDATE posts SET title=?, content=?, published=? WHERE id=?""", 
		(post['title'], post['content'], post['published'], str(idx)))
		updated_post = self.cursor.fetchone()
		self.connection.commit()
		print(updated_post)
		return True


"""CREATE TABLE IF NOT EXISTS products(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name VARCHAR NOT NULL,
			price INT NOT NULL,
			is_sale BOOL DEFAULT 0,
			inverntory INTEGER NOT NULL DEFAULT 0,
			created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);"""