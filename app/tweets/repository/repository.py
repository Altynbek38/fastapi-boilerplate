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
            "user_id": ObjectId(input["user_id"]),
            "created_at": datetime.utcnow(),
            "type": input["type"],
            "price": input["price"],
            "address": input["address"],
            "area": input["area"],
            "rooms_count": input["rooms_count"],
            "description": input["description"],
            "media": [],
            "comments": [],
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
        response = self.database["tweets"].find_one(
            {"_id": ObjectId(tweet_id), "user_id": ObjectId(user_id)}
        )
        if response:
            return response
        else:
            raise HTTPException(status_code=404, detail="Element not found")

    def update_tweet(self, tweet_id: str, user_id: str, input_data: dict):
        update_data = {
            "$set": {
                "created_at": datetime.utcnow(),
                "type": input_data["type"],
                "price": input_data["price"],
                "address": input_data["address"],
                "area": input_data["area"],
                "rooms_count": input_data["rooms_count"],
                "description": input_data["description"],
            }
        }

        self.database["tweets"].update_one(
            filter={"_id": ObjectId(tweet_id), "user_id": ObjectId(user_id)},
            update=update_data,
        )

    def delete_tweets_by_id(self, id, user_id):
        tweet = self.database["tweets"].find_one(
            {"_id": ObjectId(id), "user_id": ObjectId(user_id)}
        )
        if tweet:
            self.database["tweets"].delete_one({"_id": ObjectId(id)})
        else:
            raise HTTPException(status_code=404, detail="No permission")

    def upload_media(self, tweet_id, user_id, media):
        tweet = self.database["tweets"].find_one(
            {"_id": ObjectId(tweet_id), "user_id": ObjectId(user_id)}
        )

        if tweet:
            # new_media = tweet.get("media", [])
            # new_media.extend(media)

            update_data = {"$set": {"media": media}}

            self.database["tweets"].update_one(
                filter={"_id": ObjectId(tweet_id), "user_id": ObjectId(user_id)},
                update=update_data,
            )

        else:
            raise HTTPException(status_code=404, detail="No permission")

    def delete_media(self, tweet_id, user_id, media):
        tweet = self.database["tweets"].find_one(
            {"_id": ObjectId(id), "user_id": ObjectId(user_id)}
        )
        if tweet:
            new_media = []
            for file in tweet["media"]:
                if file != media:
                    new_media.push(file)

            update_data = {"$set": {"media": new_media}}

            self.database["tweets"].update_one(
                filter={"_id": ObjectId(tweet_id), "user_id": ObjectId(user_id)},
                update=update_data,
            )

        else:
            raise HTTPException(status_code=404, detail="No permission")

    # def create_comment_by_id(self, tweet_id, user_id, content){

    # }
