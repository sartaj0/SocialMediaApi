
class MyPostDataBase(object):
	def __init__(self):
		self.posts = [
		{"title": "Title 1", "content": "Content 1"},
		{"title": "Title 2", "content": "Content 2"}
		]

	def store(self, data):
		pass

	def __call__(self):
		return self.posts