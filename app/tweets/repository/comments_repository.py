from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from fastapi import HTTPException
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult


class CommentRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_comment(self, tweet_id: str, user_id: str, payload: dict):
        payload["tweet_id"] = ObjectId(tweet_id)
        payload["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload["author_id"] = user_id
        tweet = self.database["tweets"].find_one({"_id": ObjectId(tweet_id)})
        if not tweet:
            raise HTTPException(
                status_code=404, detail=f"Could find tweet with id {tweet_id}"
            )
        payload["user_id"] = ObjectId(user_id)
        comment = self.database["comments"].insert_one(payload)
        return comment.acknowledged

    def get_comments_by_tweet_id(self, tweet_id: str) -> List[dict]:
        comments = self.database["comments"].find({"tweet_id": ObjectId(tweet_id)})
        return list(comments)

    def update_comment_by_id(
        self, comment_id: str, user_id: str, data: dict
    ) -> UpdateResult:
        return self.database["comments"].update_one(
            filter={"_id": ObjectId(comment_id), "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            },
        )

    def delete_comment_by_id(self, comment_id: str, user_id: str) -> DeleteResult:
        return self.database["comments"].delete_one(
            {"_id": ObjectId(comment_id), "user_id": ObjectId(user_id)}
        )
