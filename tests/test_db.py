import unittest
from src.db import DB

class TestDB(unittest.TestCase):

    def test_get_all(self):
        labels = DB().get_all_labels()
        assert len(labels) > 0
    
    def test_get_label(self):
        labels = DB().get_all_labels()
        id = labels[0]['id']
        label = DB().get_label(id)
        assert label['id'] == id

    def test_delete_label(self):
        before = DB().get_all_labels()
        id = before[0]['id']
        DB().delete_label(id)
        after = DB().get_all_labels()
        assert len(before) == len(after)+1
        
    def test_update_label(self):
        store = DB().get_all_labels()
        id = store[0]['id']
        label = DB().get_label(id)
        before = label['text']
        
        DB().put_label(id, {"text": "Querty999"})

        label_after = DB().get_label(id)
        assert before != label_after['text']
        assert "Querty999" == label_after['text']

        # Restore text value
        DB().put_label(id, {"text": before})
