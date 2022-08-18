from typing import Union
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

	
