# coding: utf-8

"""
Copyright 2015 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems


class V1HTTPGetAction(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        V1HTTPGetAction - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'path': 'str',
            'port': 'str',
            'host': 'str',
            'scheme': 'str'
        }

        self.attribute_map = {
            'path': 'path',
            'port': 'port',
            'host': 'host',
            'scheme': 'scheme'
        }

        self._path = None
        self._port = None
        self._host = None
        self._scheme = None

    @property
    def path(self):
        """
        Gets the path of this V1HTTPGetAction.
        Path to access on the HTTP server.

        :return: The path of this V1HTTPGetAction.
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """
        Sets the path of this V1HTTPGetAction.
        Path to access on the HTTP server.

        :param path: The path of this V1HTTPGetAction.
        :type: str
        """
        self._path = path

    @property
    def port(self):
        """
        Gets the port of this V1HTTPGetAction.
        Name or number of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME.

        :return: The port of this V1HTTPGetAction.
        :rtype: str
        """
        return self._port

    @port.setter
    def port(self, port):
        """
        Sets the port of this V1HTTPGetAction.
        Name or number of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME.

        :param port: The port of this V1HTTPGetAction.
        :type: str
        """
        self._port = port

    @property
    def host(self):
        """
        Gets the host of this V1HTTPGetAction.
        Host name to connect to, defaults to the pod IP.

        :return: The host of this V1HTTPGetAction.
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """
        Sets the host of this V1HTTPGetAction.
        Host name to connect to, defaults to the pod IP.

        :param host: The host of this V1HTTPGetAction.
        :type: str
        """
        self._host = host

    @property
    def scheme(self):
        """
        Gets the scheme of this V1HTTPGetAction.
        Scheme to use for connecting to the host. Defaults to HTTP.

        :return: The scheme of this V1HTTPGetAction.
        :rtype: str
        """
        return self._scheme

    @scheme.setter
    def scheme(self, scheme):
        """
        Sets the scheme of this V1HTTPGetAction.
        Scheme to use for connecting to the host. Defaults to HTTP.

        :param scheme: The scheme of this V1HTTPGetAction.
        :type: str
        """
        self._scheme = scheme

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other): 
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """ 
        Returns true if both objects are not equal
        """
        return not self == other

