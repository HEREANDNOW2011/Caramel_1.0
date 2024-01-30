# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


from pymongo import MongoClient

class SaveConversations(Action):
    def name(self) -> Text:
        return "action_save_conversations"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get user and bot responses from tracker
        user_response = tracker.latest_message.get("text")
        bot_response = dispatcher.messages[-1]["text"]

        # Save conversation to MongoDB
        self.save_to_mongodb(user_response, bot_response)

        # Save conversation to text file
        self.save_to_text_file(user_response, bot_response)

        return []

    def save_to_mongodb(self, user_response: Text, bot_response: Text):
        # MongoDB connection details
        MONGODB_URL = "mongodb+srv://Nick11703:HEREANDNOWTheFrenchInstitute@chatbot.73ablqv.mongodb.net/?retryWrites=true&w=majority"
        DATABASE_NAME = "chatbot"
        COLLECTION_NAME = "conversations"

        # Connect to MongoDB
        client = MongoClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        # Save conversation to MongoDB
        collection.insert_one({"user_response": user_response, "bot_response": bot_response})

        # Close MongoDB connection
        client.close()

    def save_to_text_file(self, user_response: Text, bot_response: Text):
        # Output text file path
        OUTPUT_FILE = "N:\Documents\conversations.txt"

        # Write conversation to text file
        with open(OUTPUT_FILE, "a", encoding="utf-8") as file:
            file.write(f"User: {user_response}\nBot: {bot_response}\n\n")#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
