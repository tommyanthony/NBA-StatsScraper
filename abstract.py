import requests
import json


def parse_json_request(result):
    json = result.json()
    if 'resultSets' not in json:
        raise Exception('JSON does not fit expected format')
    else:
        return Data(json)


class Data():
    def __init__(self, json):
        self.json = json

    def out(self, file_path):
        with open(file_path) as output:
            json.dump(output, self.json)

    @property
    def data(self):
        return self.json['resultSets']


class API:
    def __init__(self, url):
        self.url = url

    def endpoint_url(self, endpoint):
        return "%s%s" % (self.url, endpoint)

    def make_request(self, endpoint, params):
        return requests.get(self.endpoint_url(endpoint), params=params)

    def endpoint(self):
        def wrapper(clz):
            instance = clz()
            setattr(instance, "api", self)
            setattr(self, clz.__endpoint__, instance)
            return clz
        return wrapper

new_api = API


class Endpoint(object):
    __optional_params__ = {}
    __required_params__ = []
    __endpoint__ = ""
    api = None

    def __init__(self, **kwargs):
        for param in kwargs.keys():
            if not self._valid_param(param):
                raise InvalidParameterException(param, self.__endpoint__)
        self.default_params = dict(self.__optional_params__)
        self.default_params.update(kwargs)

    def _valid_param(self, param):
        return (param in self.__required_params__ or
                param in self.__optional_params__)

    def get(self, **kwargs):
        params = dict(self.default_params)
        for param in self.__required_params__:
            if param not in kwargs:
                raise RequiredParameterException(param, self.__endpoint__)
        for param in kwargs:
            if not self._valid_param(param):
                raise InvalidParameterException(param, self.__endpoint__)
        params.update(kwargs)
        result = self.api.make_request(self.__endpoint__, params)
        return parse_json_request(result)
    __call__ = get

class ParameterException(Exception):
    pass

class InvalidParameterException(ParameterException):
    def __init__(self, param, endpoint, **kwargs):
        return super().__init__(
            "%s is not a valid parameter for service %s" % (param, endpoint),
            **kwargs
        )

class RequiredParameterException(ParameterException):
    def __init__(self, param, endpoint, **kwargs):
        return super().__init__(
            "%s is a required parameter for service %s" % (param, endpoint),
            **kwargs
        )
