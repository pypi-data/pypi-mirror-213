import json
from typing import Dict, Union

from netorca_sdk.auth import AbstractNetorcaAuth
from netorca_sdk.config import API_VERSION, URL_PREFIX
from netorca_sdk.exceptions import NetorcaException
from netorca_sdk.validations import ContextIn, InvalidContextError


class Netorca:
    """
    Netorca

    A class to manage API calls to various endpoints in the Netorca API using the provided authentication method.

    Attributes:
    - auth (AbstractNetorcaAuth): The authentication object used for making API requests.
    - endpoints (Dict): A dictionary containing the supported API endpoints and their corresponding methods.

    Methods:

    __init__(self, auth: AbstractNetorcaAuth)
    Initializes the NetorcaEndpointCaller with the provided authentication object.

    caller(self, endpoint: str, operation: str, id: Union[str, int] = None, filters: Dict = None, data: Dict = None, context: ContextIn = None) -> Dict
    Performs the specified operation on the specified endpoint using the provided arguments.

    _get(self, endpoint: str, id: Union[str, int] = None, filters: Dict = None, context: ContextIn = None) -> Dict
    Performs a GET request on the specified endpoint using the provided arguments.

    _create(self, endpoint: str, data: Dict, context: ContextIn = None) -> Dict
    Performs a CREATE request on the specified endpoint using the provided arguments.

    _update(self, endpoint: str, id: Union[str, int], data: Dict, context: ContextIn = None) -> Dict
    Performs an UPDATE request on the specified endpoint using the provided arguments.

    _delete(self, endpoint: str, id: Union[str, int], context: ContextIn = None) -> Dict
    Performs a DELETE request on the specified endpoint using the provided arguments.

    create_url(self, endpoint: str, context: ContextIn = ContextIn.SERVICEOWNER.value, id: Union[str, int] = None)
    Creates the appropriate URL for the specified endpoint, context, and optional ID.
    """

    def __init__(self, auth: AbstractNetorcaAuth):
        self.auth = auth
        self.endpoints = {
            "service_items": {
                "get": self._get,
            },
            "deployed_items": {
                "get": self._get,
                "create": self._create,
                "update": self._update,
                "patch": self._update,
                "delete": self._delete,
            },
            "deployed_items_dependent": {
                "get": self._get,
                "url": "deployed_items/dependant",
            },
            "change_instances": {
                "get": self._get,
                "create": self._create,
                "update": self._update,
                "patch": self._update,
            },
            "change_instances_dependent": {
                "get": self._get,
                "url": "change_instances/dependant",
            },
            "change_instances_referenced": {
                "get": self._get,
                "url": "change_instances/referenced",
            },
            "service_configs": {
                "get": self._get,
                "create": self._create,
            },
        }

    def caller(
        self,
        endpoint: str,
        operation: str,
        id: Union[str, int] = None,
        filters: Dict = None,
        data: Dict = None,
        context: ContextIn = None,
    ) -> Dict:
        if endpoint not in self.endpoints:
            raise ValueError(f"Invalid endpoint: {endpoint}")

        if operation not in self.endpoints[endpoint]:
            raise ValueError(f"Invalid operation: {operation}")

        if operation == "create":
            return self.endpoints[endpoint][operation](endpoint, data=data, context=context)
        elif operation in {"update", "patch"}:
            return self.endpoints[endpoint][operation](endpoint, id=id, data=data, context=context)
        elif operation == "delete":
            return self.endpoints[endpoint][operation](endpoint, id=id, context=context)
        else:
            return self.endpoints[endpoint][operation](endpoint, id=id, filters=filters, context=context)

    def _get(self, endpoint: str, id: Union[str, int] = None, filters: Dict = None, context: ContextIn = None) -> Dict:
        url = self.create_url(endpoint=endpoint, context=context, id=id)
        response = self.auth.get(url=url, authentication_required=True, filters=filters)
        if response.status_code == 200:
            return response.json()

        raise NetorcaException(f"Could not fetch data from {endpoint} due to: {response.json()}")

    def _create(self, endpoint: str, data: Dict, context: ContextIn = None) -> Dict:
        url = self.create_url(endpoint=endpoint, context=context)
        response = self.auth.post(url=url, data=json.dumps(data), authentication_required=True)
        if response.status_code == 201:
            return response.json()

        raise NetorcaException(f"Could not create data in {endpoint} due to: {response.json()}")

    def _update(self, endpoint: str, id: Union[str, int], data: Dict, context: ContextIn = None) -> Dict:
        url = self.create_url(endpoint=endpoint, context=context, id=id)
        response = self.auth.patch(url=url, data=json.dumps(data), authentication_required=True)
        if response.status_code == 200:
            return response.json()

        raise NetorcaException(f"Could not update data in {endpoint} due to: {response.json()}")

    def _delete(self, endpoint: str, id: Union[str, int], context: ContextIn = None) -> Dict:
        url = self.create_url(endpoint=endpoint, context=context, id=id)
        response = self.auth.delete(url=url, authentication_required=True)
        if response.status_code == 204:
            return {"status": "deleted"}

        raise NetorcaException(f"Could not delete data from {endpoint} due to: {response.json()}")

    def create_url(self, endpoint: str, context: ContextIn = ContextIn.SERVICEOWNER.value, id: Union[str, int] = None):
        id_str = f"{str(id).replace('/', '')}/" if id else ""

        context = ContextIn.SERVICEOWNER.value if context is None else context
        if context not in (ContextIn.SERVICEOWNER.value, ContextIn.CONSUMER.value):
            raise InvalidContextError(
                f"{context} is not a valid ContextIn value. Options are {ContextIn.SERVICEOWNER.value} and {ContextIn.CONSUMER.value}"
            )
        custom_url = self.endpoints.get(endpoint, {}).get("url")
        if custom_url:
            url = f"{self.auth.fqdn}{API_VERSION}{URL_PREFIX}/{context}/{custom_url}/{id_str}"
        else:
            url = f"{self.auth.fqdn}{API_VERSION}{URL_PREFIX}/{context}/{endpoint}/{id_str}"

        return url

    def create_deployed_item(self, change_instance_uuid: str, description: dict) -> dict:
        data = {"deployed_item": description}
        return self.caller("change_instances", "patch", id=change_instance_uuid, data=data)

    def get_deployed_item(self, change_instance_uuid: str) -> dict:
        return self.caller("deployed_items", "get", id=change_instance_uuid)

    def get_deployed_items(self) -> dict:
        return self.caller("deployed_items", "get")

    def get_service_items(self) -> dict:
        return self.caller("service_items", "get")

    def get_service_item(self, service_item_uuid: str) -> dict:
        return self.caller("service_items", "get", id=service_item_uuid)

    def get_change_instance(self, change_instance_uuid: str) -> dict:
        return self.caller("change_instances", "get", id=change_instance_uuid)

    def get_change_instances(self) -> dict:
        return self.caller("change_instances", "get")

    def update_change_instance(self, change_instance_uuid: str, data: dict) -> dict:
        return self.caller("change_instances", "update", id=change_instance_uuid, data=data)

    def get_service_config(self, service_config_uuid: str) -> dict:
        return self.caller("service_configs", "get", id=service_config_uuid)

    def get_service_configs(self) -> dict:
        return self.caller("service_configs", "get")

    def create_service_config(self, data: dict) -> dict:
        return self.caller("service_configs", "create", data=data)
