from Config import Settings
from pymongo import MongoClient
from bson.objectid import ObjectId

settings = Settings()


class MongoDB:
    def __init__(self):
        # Initialize the MongoDB client
        self.client = MongoClient(settings.mongodb_url)
        self.db = self.client["university_assignment"]  # Database name

    def set_collection(self, collection_name: str):
        """
        Set the active collection for CRUD operations dynamically.
        """
        self.collection = self.db[collection_name]
        return self.collection

    def get_connection(self) -> dict:
        """
        Get MongoDB client and database connections.
        """
        return {
            'client': self.client,
            'db': self.db
        }

    def create(self, data: dict) -> str:
        """
        Create a new document in the current collection.
        :param data: Dictionary representing the document to insert.
        :return: Inserted document ID.
        """
        result = self.collection.insert_one(data)
        return result

    def read(self, query: dict = None) -> list:
        """
        Read documents from the current collection.
        :param query: Dictionary for filtering documents. Default is {} (all documents).
        :return: List of matching documents.
        """
        query = query or {}
        print(query)
        return list(self.collection.find(query))

    def update(self, document_id: str, update_data: dict) -> bool:
        """
        Update a document by its ID.
        :param document_id: The ID of the document to update.
        :param update_data: Dictionary representing the fields to update.
        :return: True if the update was successful, False otherwise.
        """
        result = self.collection.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete(self, document_id: str) -> bool:
        """
        Delete a document by its ID.
        :param document_id: The ID of the document to delete.
        :return: True if the delete was successful, False otherwise.
        """
        result = self.collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count > 0

    def get_by_id(self, document_id: str) -> dict:
        """
        Find a document by its ID.
        :param document_id: The ID of the document to retrieve.
        :return: The matching document as a dictionary, or None if not found.
        """
        try:
            document = self.collection.find_one({"_id": ObjectId(document_id)})
            return document
        except Exception as e:
            print(f"Error fetching document by ID: {e}")
            return None
