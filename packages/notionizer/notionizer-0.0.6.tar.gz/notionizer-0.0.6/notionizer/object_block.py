import notionizer.object_database
import notionizer.object_adt
from notionizer.exception import NotionBlockException
from notionizer.http_request import HttpRequest
notion_object_init_handler = notionizer.functions.notion_object_init_handler
from typing import Dict, Any


NotionUpdateObject = notionizer.object_database.NotionUpdateObject
from notionizer.exception import NotionBlockException


class ChildrenBlockList(notionizer.object_adt.ListObject):


    def __init__(self,name, owner,data: list=None, mutable=False):
        self._data = data
        super().__init__(name, owner, data, mutable=True)
        print(data)




    def __delitem__(self, block_id):
        """
        Removes the block with the block_id from the ChildrenBlockList object and deletes it.

        Args:
            block_id

        Returns:
            None
        """
        block = self._data.pop(block_id)
        block.delete()




    #     self._request.delete('v1/blocks/' + block_id)
        # raise NotImplementedError

    # def __setitem__(self, index, value):
    #     raise NotImplementedError

    # def insert(self, index, value):
    #     """
    #     Inserts the specified value at the specified index in the list.
    #     :param index: The index at which to insert the value.
    #     :type index: int
    #     :param value: The value to insert.
    #     :type value: Block
    #     :raises NotionBlockException: If the value is not a block object.
    #     """
    #     if value != Block:
    #         raise NotionBlockException("value must be block object")
    #
    #     self._data[index:index] = value
        # return self._data.append(value)

class Block(NotionUpdateObject):


    @notion_object_init_handler
    def __init__(self, request: HttpRequest, data: Dict[str, Any]):
        super().__init__(request, data)

    def delete(self):
        """
        Delete a block from block object itself.

        Raises:
            HttpRequestError: If the request fails.
        """
        self._request.delete('v1/blocks/' + self.id)

    def _set_children(self, children_list: list):
        """
        Set a ChildrenBlockList from children_list

        Args:
            children_list

        Returns:
            self.children

        """

        self.children = ChildrenBlockList("children",self, children_list)
        return self.children
