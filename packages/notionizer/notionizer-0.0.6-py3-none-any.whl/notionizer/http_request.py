"""
HTTP REQUEST

managing request

"""
import time

import requests  # type: ignore
import json
import logging

from notionizer import settings

from typing import Dict, Any, Tuple, TypeVar

_logger = logging.getLogger(__name__)


class HttpRequestError(Exception):
    def __init__(self, status, code, message, header, payload, request_url):
        self.status = status
        self.code = code
        self.message = message
        self.header = header
        self.payload = payload
        self.request_url = request_url
        super().__init__(f'[{status}] {code}: {message}, header: {header} body: {payload} from: {request_url}')


T_HttpRequest = TypeVar('T_HttpRequest', bound='HttpRequest')


class HttpRequest:

    def __init__(self, secret_key: str, timeout: int = 15, time_out_try=3, time_out_wait=30):
        self.base_url = settings.BASE_URL
        self.__headers = {
            'Authorization': 'Bearer ' + secret_key,
            'Content-Type': 'application/json',
            'Notion-Version': settings.NOTION_VERSION
        }
        self.timeout = timeout
        self.time_out_try = time_out_try
        self.time_out_wait = time_out_wait


    def post(self: T_HttpRequest, url: str, payload: Dict[str, Any]) -> Tuple[T_HttpRequest, Dict[str, Any]]:
        return self._request('POST', url, payload)

    def get(self: T_HttpRequest, url: str) -> Tuple[T_HttpRequest, Dict[str, Any]]:
        return self._request('GET', url, {})

    def patch(self: T_HttpRequest, url: str, payload: Dict[str, Any]) -> Tuple[T_HttpRequest, Dict[str, Any]]:
        return self._request('PATCH', url, payload)

    def delete(self: T_HttpRequest, url: str):
        return self._request('DELETE', url, {})

    def _request(self: T_HttpRequest, request_type: str, url: str, payload: Dict[str, Any]) -> Tuple[T_HttpRequest,
                                                                                                     Dict[str, Any]]:
        """

        :param request_type: 'POST' or 'GET'
        :param url: fully assembled url
        :param payload:
        :return: python data type object(dictionay and list)
        """
        _logger.debug(f'[{request_type}] url[{self.base_url + url}] payload: {payload}')
        # _logger.debug('payload:' + str(payload))
        payload_json = ''
        if payload:
            payload_json = json.dumps(payload)
        request_url: str = self.base_url + url
        for i in range(self.time_out_try):
            try:
                result_json: str = requests.request(request_type, request_url, headers=self.__headers,
                                            data=payload_json, timeout=self.timeout).text

                result: Dict[str, Any] = json.loads(result_json)
                _logger.debug(f"result: {result}")
                if result['object'] == 'error':
                    status = result['status']
                    code = result['code']
                    message = result['message']
                    raise HttpRequestError(status, code, message, self.__headers, payload, request_url)
                break
            except requests.exceptions.ReadTimeout as e:
                if i + 1 == self.time_out_try:
                    raise e
                _logger.info(f'time out:{i}')
                time.sleep(self.time_out_wait)
            except json.decoder.JSONDecodeError as e:
                if i + 1 == self.time_out_try:
                    raise e
                _logger.info(f'time out:{i}')
                time.sleep(self.time_out_wait)
            except HttpRequestError as e:
                if e.status == 500:
                    if i + 1 == self.time_out_try:
                        raise e
                    _logger.info(f':{e.code}:{i}')
                    time.sleep(self.time_out_wait)
                else:
                    raise e

        return self, result
