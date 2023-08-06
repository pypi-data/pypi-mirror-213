from unittest import TestCase
from notionizer import notion
from notionizer import Property as Prop
from notionizer import NumberFormat as NumForm
from notionizer import OptionColor as OptColor

#import notionizer
from setting import setting
from notionizer import functions

notion_api_key = setting.notion_api_key
pdir = functions.pdir


class TestPage(TestCase):
    def test_get_properties(self):
        import notionizer.notion

        notion = notionizer.notion.Notion(notion_api_key)

        test_page = notion.get_page('b5e1db8808ad47d19ed826873f144c43')
        print(pdir(test_page))

        print("archived         :", type(test_page.archived))
        print("cover            :", type(test_page.cover))
        print("create_database  :", type(test_page.create_database))
        print("created_by       :", type(test_page.created_by))
        print("created_time     :", type(test_page.created_time))
        print("get_properties   :", type(test_page.get_properties))
        print("icon             :", type(test_page.icon))
        print("id               :", type(test_page.id))
        print("last_edited_by   :", type(test_page.last_edited_by))
        print("last_edited_time :", type(test_page.last_edited_time))
        print("object           :", type(test_page.object))
        print("parent           :", type(test_page.parent))
        print("properties       :", type(test_page.properties))
        print("url              :", type(test_page.url))

        assert isinstance(test_page.created_by, notionizer.object_user.User)
        assert isinstance(test_page.last_edited_by, notionizer.object_user.User)
        assert isinstance(test_page.parent, notionizer.object_adt.DictionaryObject)
        assert isinstance(test_page.properties, notionizer.properties_property.PropertiesProperty)


class TestPage(TestCase):
    def test_create_database(self):
        import notionizer.notion

        notion = notionizer.notion.Notion(notion_api_key)

        test_page = notion.get_page('b5e1db8808ad47d19ed826873f144c43')

        db = test_page.create_database(
            title='test_create_database',
            emoji='🎉',
            cover='https://web.image.path/image.jpg',
            properties=

                [
                Prop.RichText("text filed"),
                Prop.Number("number", format= NumForm.dollar),
                Prop.Select("select", options= {'opt1': OptColor.blue, 'opt2': OptColor.red}),
                Prop.MultiSelect("multi select", options= {'opt1': OptColor.blue, 'opt2': OptColor.red}),
                ]


        )

