
class MyPostDataBase(object):
	def __init__(self):
		self.posts = [
		{"title": "Title 1", "content": "Content 1", "id": 1},
		{"title": "Title 2", "content": "Content 2", "id": 2}
		]

	def store(self, data: dict):
		self.posts.append(data)
		return self

	def __call__(self) -> dict:
		return self.posts