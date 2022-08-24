from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schema, database, oauth2, models
from sqlalchemy.orm import Session
router = APIRouter(
	tags=['Vote'],
	prefix="/votes"
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
	post = db.query(models.Post).filter(models.Post.idx == vote.post_id).first()
	if post is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} was not found")

	vote_querry = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, 
	models.Vote.user_id == current_user.idx) 
	found_vote = vote_querry.first()
	print(vote.post_id)

	if vote.dir == 1:
		if found_vote != None:
			raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.idx} has already voted on post: {vote.post_id}")
		new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.idx)
		db.add(new_vote)
		db.commit()
		return {"message": "successfully added vote"}
	else:
		if found_vote is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote doesn't exist")
		vote_querry.delete(synchronize_session=False)
		db.commit()

		return {"message": "successfully deleted vote"}

