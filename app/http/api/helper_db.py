import os
from pysondb import db

from app.http.api.helper import strip, image_path, database_path


class HelperDB:
    def __init__(self):
        self.db_name = "data_store"

    def _get_or_create(self):
        db_path = os.path.join(
            database_path(),
            f"{self.db_name}.json",
        )
        return db.getDb(db_path)

    def post_label(self, data):
        store = self._get_or_create()

        if self.get_by_label(data["label"]) is None:
            img_label = data["label"].replace(" ", "_")
            data = {
                "label": data["label"],
                "image_name": f"{img_label}.png",
                "tag_name": data["tag_name"],
                "accessible_name": data["accessible_name"],
                "text": data["text"],
                "e_id": data["e_id"],
                "name": data["name"],
                "placeholder": data["placeholder"],
                "class": data["class"],
            }
            store.add(data)

    def get_by_label(self, label: str):
        store = self._get_or_create()
        labels = store.getByQuery({"label": label})
        if len(labels) == 0:
            return None
        return labels[0]

    def get_all_labels(self):
        store = self._get_or_create()
        return store.getAll()

    def get_label(self, id: int):
        store = self._get_or_create()
        return store.getById(id)

    def delete_label(self, id: int):
        store = self._get_or_create()
        label = store.getById(id)
        img_path = os.path.join(
            image_path(),
            label["image_name"],
        )
        if os.path.exists(img_path):
            os.remove(img_path)

        return store.deleteById(id)

    def put_label(self, id, update={}):
        store = self._get_or_create()
        return store.updateById(id, update)
