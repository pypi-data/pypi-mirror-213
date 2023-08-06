from unittest import TestCase


import logging
from setting import setting
notion_api_key = setting.notion_api_key
log_format = '%(asctime)s [%(filename)s:%(lineno)s|%(levelname)s] %(funcName)s(): %(message)s'
# logging.basicConfig(format=log_format, level=logging.INFO)
# logging.basicConfig(format=log_format, level=logging.DEBUG)

logger = logging.getLogger('notionizer.notion')
# logger.setLevel(logging.DEBUG)

import notionizer
from notionizer import functions
import notionizer.notion
import notionizer.object_user

pdir = functions.pdir
"""[propertied_table]
https://www.notion.so/df58db74a89743b3b1a8a4a4418da561?v=c675a032856d4aedac7992d49f1c677c
: 프로퍼티 종류를 '정리'해놓은 테이블. 해당 테이블을 통해서 '테스트 케이스'를 짜면 됩니다.
"""
propertied_table_id = "df58db74a89743b3b1a8a4a4418da561"

"""[Test Database]
https://www.notion.so/5c3b340a5fd24161888f08642403b0ad?v=76c21800ffe4495389bb7412d2139129

"""
test_database_id = "5c3b340a5fd24161888f08642403b0ad"

notion = notionizer.notion.Notion(notion_api_key)
properties_table = notion.get_database(propertied_table_id)


class TestDatabase(TestCase):
    def test_database_property(self):
        test_db = notion.get_database(test_database_id)

        print("archived     :", type(test_db.archived))
        print("cover        :", type(test_db.cover))
        print("created_by   :", type(test_db.created_by))
        print("created_time :", type(test_db.created_time))
        print("description  :", type(test_db.description))
        print("get_as_dictionaries:", type(test_db.get_as_dictionaries))
        print("get_as_tuples:", type(test_db.get_as_tuples))
        print("icon         :", type(test_db.icon))
        print("id           :", type(test_db.id))
        print("is_inline    :", type(test_db.is_inline))
        print("last_edited_by:", type(test_db.last_edited_by))
        print("last_edited_time:", type(test_db.last_edited_time))
        print("object       :", type(test_db.object))
        print("parent       :", type(test_db.parent))
        print("properties   :", type(test_db.properties))
        print("title        :", type(test_db.title))
        print("url          :", type(test_db.url))

        assert isinstance(test_db.created_by, notionizer.object_user.User)
        assert isinstance(test_db.description, notionizer.object_adt.ListObject)
        assert isinstance(test_db.last_edited_by, notionizer.object_user.User)
        assert isinstance(test_db.parent, notionizer.object_adt.DictionaryObject)
        assert isinstance(test_db.properties, notionizer.properties_property.PropertiesProperty)

