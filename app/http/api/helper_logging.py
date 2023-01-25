import os
from pysondb import db
from datetime import datetime
from helper import logging_path


class HelperLogging:
    def __init__(self):
        self.db_name = "logging_store"


    def _get_or_create(self):
        db_path = os.path.join(
            logging_path(),
            f"{self.db_name}.json",
        )
        return db.getDb(db_path)

    def post_log(self, data):
        store = self._get_or_create()

        data = {
            "date_time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "label": data["label"],
            "method": data["method"],
            "error": data["error"],
            "fl_id": data["fl_id"]
        }
        return store.add(data)

    def get_logs(self):
        store = self._get_or_create()
        return store.getAll()

    def get_log(self, id: int):
        store = self._get_or_create()
        return store.getById(id)

    def put_log(self, id, update={}):
        store = self._get_or_create()
        return store.updateById(id, update)

    def get_logs_by_fl_id(self, fl_id):
        store = self._get_or_create()
        return store.getBy({"fl_id": fl_id})