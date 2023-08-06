"""
Notion API


"""

import logging as _logging

_log = _logging.getLogger(__name__)
_logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)s|%(levelname)s] %(funcName)s(): %(message)s')

from notionizer.http_request import HttpRequest
from notionizer.object_database import Database
from notionizer.object_page import Page
from notionizer.object_user import User
from notionizer.object_block import Block
from notionizer.object_block import ChildrenBlockList


class Notion:
    f"""
    Notion

    'Notion' is basic object of 'notionizer' module.
    """

    def __init__(self, secret_key: str, timeout=15):
        """
        Initializes an instance of the HttpRequest class with the specified secret key.

        Args:
            secret_key (str): A string containing the secret key used to authenticate requests.
        """
        self.__secret_key = secret_key
        self._request: HttpRequest = HttpRequest(secret_key, timeout=timeout)

    def get_database(self, database_id: str) -> Database:
        f"""
        get 'Database' Object by 'database_id'

        https://www.notion.so/myworkspace/{{database_id}}?v=...
        
        ex) https://www.notion.so/myworkspace/a8aec43384f447ed84390e6e32c2e089?v=...
            database id -> a8aec43384f447ed84390e6e32c2e089
        
        :param database_id:
        :return: Database
        """

        result = self._request.get('v1/databases/' + database_id)
        database = Database(*result)
        db_object: Database = database
        return db_object

    def get_page(self, page_id: str) -> Page:
        """
        get 'Page' object by 'page id'
        :param page_id:
        :return: Page
        """
        page_object: Page = Page(*self._request.get('v1/pages/' + page_id))
        return page_object

    def get_user(self, user_id: str) -> User:
        """
        get 'User' object by 'user id'.
        :param user_id:
        :return: User
        """
        user_object: User = User(*self._request.get('v1/users/' + user_id))
        return user_object

    def get_all_users(self) -> list:
        """
        get a paginated list of 'Users for the workspace(user and bots)'.
        :return: List[User]
        """
        request: HttpRequest
        user_list = list()

        request, result = self._request.get('v1/users')

        for obj in result['results']:
            user_list.append(User(request, obj))
        return user_list

    def get_me(self) -> User:
        """
        get the 'bot User' itself associated with the API token
        :return: User
        """
        me: User = User(*self._request.get('v1/users/me'))

        return me

    def get_block(self, block_id: str) -> Block:
        """

        get the block object from the block id.

        :param block_id
        :return: block
        """

        block: Block = Block(*self._request.get('v1/blocks/' + block_id))
        # print(block)
        return block

    def get_block_children(self, block_id: str) -> "ChildrenBlockList":
        """

        get the ChildrenBlockList object from the block id.

        :param block_id
        :return: ChildrenBlockList
        """

        request, data = self._request.get('v1/blocks/' + block_id + "/children")
        children = list()
        results = data['results']
        for obj in results:
            children.append(Block(request, obj))

        childrenBlockList = Block._set_children(self, children)

        return childrenBlockList

    def delete_block(self, block_id: str):
        """
        Delete a block from block_id.

        Args:
            block_id (str)

        Raises:
            HttpRequestError: If the request fails.
        """

        self._request.delete('v1/blocks/' + block_id)

    def update_block(self, block_id: str, payload):

        self._request.patch('v1/blocks/' + block_id, payload)
        # pass

    def append_block_children(self, block_id: str):
        self._request.patch('v1/blocks/' + block_id + '/children')
        # pass