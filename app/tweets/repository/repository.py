from datetime import datetime
from typing import List
from fastapi import HTTPException

from bson.objectid import ObjectId
from pymongo.database import Database


class TweetRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_tweet(self, input: dict):
        payload = {
            "content": input["content"],
            "user_id": ObjectId(input["user_id"]),
            "created_at": datetime.utcnow(),
            "type": input["type"],
            "price": input["price"],
            "address": input["address"],
            "area": input["area"],
            "rooms_count": input["rooms_count"],
            "description": input["description"]
        }

        self.database["tweets"].insert_one(payload)

    def get_tweet_by_user_id(self, user_id: str) -> List[dict]:
        tweets = self.database["tweets"].find(
            {
                "user_id": ObjectId(user_id),
            }
        )
        result = []
        for tweet in tweets:
            result.append(tweet)

        return result
    
    def get_tweet_by_id(self, tweet_id: str, user_id: str):
        response = self.database["tweets"].find_one({'_id': ObjectId(tweet_id), 'user_id': ObjectId(user_id)})
        if response:
            return response
        else:
            raise HTTPException(status_code=404, detail="Element not found")
        
    def update_tweet(self, tweet_id: str, user_id: str, input_data: dict):
        update_data = {
            "$set": {
                "content": input_data["content"],
                "created_at": datetime.utcnow(),
                "type": input_data["type"],
                "price": input_data["price"],
                "address": input_data["address"],
                "area": input_data["area"],
                "rooms_count": input_data["rooms_count"],
                "description": input_data["description"]
            }
        }

        self.database["tweets"].update_one(
            filter={"_id": ObjectId(tweet_id), "user_id": ObjectId(user_id)},
            update=update_data
        )

    def delete_tweets_by_id(self, id, user_id):
        tweet = self.database["tweets"].find_one({'_id': ObjectId(id), "user_id": ObjectId(user_id)})
        if tweet:
            self.database["tweets"].delete_one({"_id": ObjectId(id)})
        else:
            raise HTTPException(status_code=404, detail="No permission")