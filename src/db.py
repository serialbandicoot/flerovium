import os
from pysondb import db


class DB:
    def __init__(self):
        self.db_name = "data_store"

    def _get_or_create(self):
        db_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..",
            "data",
            f"{self.db_name}.json",
        )
        return db.getDb(db_path)

    def save_data(self, label: str, element):
        store = self._get_or_create()
        data = {
            "label": label,
            "image_label_name": f"{label}.png",
            "tag_name": element.tag_name,
            "accessible_name": element.accessible_name,
            "text": element.text,
            "e_id": element.get_attribute("id"),
            "name": element.get_attribute("name"),
            "placeholder": element.get_attribute("placeholder"),
        }
        if self.get_by_label(label) is None:
            store.add(data)

    def get_by_label(self, label: str):
        store = self._get_or_create()
        labels = store.getByQuery({"label": label})
        if len(labels) == 0:
            return None
        return labels[0]
