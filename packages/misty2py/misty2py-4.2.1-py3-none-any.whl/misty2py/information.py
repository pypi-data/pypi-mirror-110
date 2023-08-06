"""This module's function is to send information requests via the information keywords matching to Misty's API endpoints, sending information requests and matching data shortcuts.
"""
import json
from os import path
from typing import Dict
from urllib.parse import urlencode

import requests

this_directory = path.abspath(path.dirname(__file__))
INFOS_JSON = str(path.join(this_directory, "allowed_infos.json"))


class Get:
    """A class representing the GET url request method.

    Attributes:
        ip (str): The IP address where the requests are sent
        allowed_infos (dict): The dictionary of information keywords matching to the Misty's API endpoints.
    """

    def __init__(self, ip: str, custom_allowed_infos: Dict = {}) -> None:
        """Initialises a Get object.

        Args:
            ip (str): The IP address where the requests are sent.
            custom_allowed_infos (Dict, optional): The dictionary of custom information keywords. Defaults to `{}`.
        """

        self.ip = ip

        allowed_infos = custom_allowed_infos
        f = open(INFOS_JSON)
        allowed_infos.update(json.loads(f.read()))
        f.close()

        self.allowed_infos = allowed_infos

    def get_info(self, endpoint: str) -> Dict:
        """Sends a GET request.

        Args:
            endpoint (str): The API endpoint to which the request is sent.

        Returns:
            Dict: The response from Misty's REST API.
        """

        r = requests.get("http://%s/%s" % (self.ip, endpoint))
        try:
            return r.json()
        except Exception as e:
            return {"status": "Success", "content": r.content, "error_msg": e}


class Info(Get):
    """A class representing an information request from Misty.
    A subclass of Get()."""

    def get_info(self, info_name: str, params: Dict = {}) -> Dict:
        """Sends an information request to Misty.

        Args:
            info_name (str): The information keyword specifying which information is requested.
            params (Dict): dict of parameter name and parameter value. Defaults to `{}`.

        Returns:
            Dict: The response from Misty's REST API.
        """

        if info_name not in self.allowed_infos.keys():
            response = {
                "status": "Failed",
                "message": "Command `%s` not supported." % info_name,
            }

        else:
            endpoint = self.allowed_infos[info_name]

            if len(params) > 0:
                endpoint += "?"
                query_string = urlencode(params)
                endpoint += query_string

            try:
                response = super().get_info(endpoint)

            except Exception as e:
                response = {
                    "status": "Failed",
                    "message": "Error occured. Error message: `%s`" % e,
                }

        return response
