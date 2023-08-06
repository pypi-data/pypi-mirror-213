from unittest import TestCase

import notionizer
from notionizer import notion
from setting import setting

notion_api_key = setting.notion_api_key

class TestNotion(TestCase):
    def test_get_database(self):
        import notionizer.notion
        notion = notionizer.notion.Notion(notion_api_key)
        test_dt = notion.get_database('6ebb6b2ec1ea442e83ca1b11f9dd329c')

        print(test_dt)