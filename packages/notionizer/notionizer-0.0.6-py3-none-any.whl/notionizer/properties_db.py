from notionizer.properties_basic import DbPropertyObject
from notionizer.properties_basic import TitleProperty
from notionizer.object_adt import DictionaryObject
from notionizer.functions import from_plain_text_to_rich_text_array
from typing import Any
from typing import Dict


class DbPropertyCreatedBy(DbPropertyObject):
    """
    'DbPropertyCreatedBy'
    """
    _type_defined = 'created_by'
    _mutable = False


class DbPropertyPhoneNumber(DbPropertyObject):
    """
    'DbPropertyPhoneNumber'
    """
    _type_defined = 'phone_number'
    _mutable = True
    _input_validation = (str, )


class DbPropertyEmail(DbPropertyObject):
    """
    'DbPropertyEmail'
    """
    _type_defined = 'email'
    _mutable = True
    _input_validation = (str, )


class DbPropertyPeople(DbPropertyObject):
    """
    'DbPropertyPeople'
    """
    _type_defined = 'people'
    _mutable = True
    _input_validation = (list, )


class DbPropertyTitle(DbPropertyObject):
    """
    'DbPropertyTitle'
    """
    _type_defined = 'title'
    _mutable = True
    _input_validation = (str, list)
    title = TitleProperty()

    def _convert_to_update(self, value: str) -> Dict[str, Any]:
        """
        convert value to 'title' update from.

        :param value: str
        :return: dictionary
        """
        return {'title': from_plain_text_to_rich_text_array(value)}


class DbPropertyText(DbPropertyObject):
    """
    'DbPropertyText'
    """
    _type_defined = 'text'
    _mutable = True
    _input_validation = (str, list)

    def _convert_to_update(self, value: Any) -> Any:
        """
        convert value to 'text' update from.

        :param value: str or list
        :return: dictionary
        """
        if type(value) is str:
            return {'rich_text': from_plain_text_to_rich_text_array(value)}
        elif type(value) is list:
            return value


class DbPropertyFiles(DbPropertyObject):
    """
    'DbPropertyFiles'
    """
    _type_defined = 'files'
    _mutable = True
    _input_validation = (list, )


class DbPropertyCreatedTime(DbPropertyObject):
    """
    'DbPropertyCreatedTime'
    """
    _type_defined = 'created_time'
    _mutable = False


class DbPropertyNumber(DbPropertyObject):
    """
    'DbPropertyNumber'
    """
    _type_defined = 'number'
    _mutable = True
    _input_validation = (int, float)


class DbPropertyRollup(DbPropertyObject):
    """
    'DbPropertyRollup'
    """
    _type_defined = 'rollup'
    _mutable = False


class DbPropertyRelation(DbPropertyObject):
    """
    'DbPropertyRelation'
    """
    _type_defined = 'relation'
    _mutable = False
    relation: DictionaryObject


class DbPropertyCheckbox(DbPropertyObject):
    """
    'DbPropertyCheckbox'
    """
    _type_defined = 'checkbox'
    _mutable = True
    _input_validation = (bool, )


class DbPropertyUrl(DbPropertyObject):
    """
    'DbPropertyUrl'
    """
    _type_defined = 'url'
    _mutable = True
    _input_validation = (str, )


class DbPropertySelect(DbPropertyObject):
    """
    'DbPropertySelect'
    """
    _type_defined = 'select'
    _mutable = True
    _input_validation = (dict, )

    def set_select_list(self, select_list):
        payload = {"options": []}
        for s in select_list:
            payload["options"].append({'name': s})
        self._update('select', payload)


class DbPropertyFormula(DbPropertyObject):
    """
    'DbPropertyFormula'
    """
    _type_defined = 'formula'
    _mutable = False


class DbPropertyLastEditedTime(DbPropertyObject):
    """
    'DbPropertyLastEditedTime'
    """
    _type_defined = 'last_edited_time'
    _mutable = False


class DbPropertyDate(DbPropertyObject):
    """
    'DbPropertyDate'
    """
    _type_defined = 'date'
    _mutable = True
    _input_validation = (dict, )


class DbPropertyMultiSelect(DbPropertyObject):
    """
    'DbPropertyMultiSelect'
    """
    _type_defined = 'multi_select'
    _mutable = True
    _input_validation = (list, )


class DbPropertyLastEditedBy(DbPropertyObject):
    """
    'DbPropertyLastEditedBy'
    """
    _type_defined = 'last_edited_by'
    _mutable = False


