from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoManager:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="todo_db", collection_name="tasks"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_task(self, title, description):
        task = {"title": title, "description": description}
        result = self.collection.insert_one(task)
        return str(result.inserted_id)

    def get_all_tasks(self):
        tasks = list(self.collection.find())
        for task in tasks:
            task['_id'] = str(task['_id'])
        return tasks

    def get_task_by_id(self, task_id):
        task = self.collection.find_one({"_id": ObjectId(task_id)})
        if task:
            task['_id'] = str(task['_id'])
        return task

    def update_task(self, task_id, title=None, description=None):
        update_fields = {}
        if title:
            update_fields['title'] = title
        if description:
            update_fields['description'] = description
        if not update_fields:
            return None  # چیزی برای آپدیت فرستاده نشده
        
        result = self.collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_fields}
        )
        return result.modified_count > 0  # اگر چیزی آپدیت شد True برمیگردونه

    def delete_task(self, task_id):
        result = self.collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0  # اگر حذف شد True برمیگردونه

