wfrom unittest import TestCase
from setting import setting

notion_api_key = setting.notion_api_key


class TestNotion(TestCase):
    def test_get_user(self):
        import notionizer.notion
        notion = notionizer.notion.Notion(notion_api_key)

        test_dt = notion.get_database('6ebb6b2ec1ea442e83ca1b11f9dd329c')
        user = notion.get_user('55cb1dac-e37d-462c-a105-edaec8b68363')

        print(user)


class TestNotion(TestCase):
    def test_get_all_users(self):
        import notionizer.notion
        notion = notionizer.notion.Notion(notion_api_key)

        all_user = notion.get_all_users()
        print(all_user)
