import uuid

import grpc

from . import errors
from .data_mappers import ApiKeyDataMapper
from .entities import ApiKey
from .proto import api_keys_objects_pb2
from .proto import api_keys_services_pb2
from .proto import api_keys_services_pb2_grpc
from ..errors import UnknownError


class UserApiKeyAuthService:
    def __init__(self, service_url: str):
        self.service_url = service_url

    def authenticate_user(self, api_key_string: str) -> uuid.UUID:
        with grpc.insecure_channel(self.service_url) as channel:
            stub = api_keys_services_pb2_grpc.UserApiKeyAuthServiceStub(channel)
            request = api_keys_services_pb2.AuthenticateUserRequest(api_key_string=api_key_string)
            response = stub.AuthenticateUser(request)
        if response.error == api_keys_objects_pb2.Error.NOT_AUTHORIZED:
            raise errors.NotAuthorizedError()
        if response.error == api_keys_objects_pb2.Error.INVALID_API_KEY:
            raise errors.InvalidApiKeyError()
        if response.error == api_keys_objects_pb2.Error.API_KEY_NOT_FOUND:
            raise errors.ApiKeyNotFoundError()
        if response.error:
            raise UnknownError()
        user_id = uuid.UUID(response.user_id)
        return user_id

    def create_user_api_key(self, user_id: uuid.UUID, name: str, description: str) -> str:
        with grpc.insecure_channel(self.service_url) as channel:
            stub = api_keys_services_pb2_grpc.UserApiKeyAuthServiceStub(channel)
            request = api_keys_services_pb2.CreateUserApiKeyRequest(
                user_id=str(user_id), name=name, description=description
            )
            response = stub.CreateUserApiKey(request)
        if response.error:
            raise UnknownError()
        api_key_string = response.api_key_string
        return api_key_string

    def delete_user_api_key(self, key_id: str) -> ApiKey:
        with grpc.insecure_channel(self.service_url) as channel:
            stub = api_keys_services_pb2_grpc.UserApiKeyAuthServiceStub(channel)
            request = api_keys_services_pb2.DeleteUserApiKeyRequest(key_id=key_id)
            response = stub.DeleteUserApiKey(request)
        if response.error == api_keys_objects_pb2.Error.API_KEY_NOT_FOUND:
            raise errors.ApiKeyNotFoundError()
        if response.error:
            raise UnknownError()
        api_key = ApiKeyDataMapper.proto_model_to_entity(response.api_key)
        return api_key

    def get_user_api_key(self, key_id: str) -> ApiKey:
        with grpc.insecure_channel(self.service_url) as channel:
            stub = api_keys_services_pb2_grpc.UserApiKeyAuthServiceStub(channel)
            request = api_keys_services_pb2.GetUserApiKeyRequest(key_id=key_id)
            response = stub.GetUserApiKey(request)
        if response.error == api_keys_objects_pb2.Error.API_KEY_NOT_FOUND:
            raise errors.ApiKeyNotFoundError()
        if response.error:
            raise UnknownError()
        api_key = ApiKeyDataMapper.proto_model_to_entity(response.api_key)
        return api_key

    def get_user_api_keys(self, user_id: uuid.UUID) -> list[ApiKey]:
        with grpc.insecure_channel(self.service_url) as channel:
            stub = api_keys_services_pb2_grpc.UserApiKeyAuthServiceStub(channel)
            request = api_keys_services_pb2.GetUserApiKeysListRequest(user_id=str(user_id))
            response = stub.GetUserApiKeysList(request)
        if response.error:
            raise UnknownError()
        api_keys = [ApiKeyDataMapper.proto_model_to_entity(api_key) for api_key in response.api_keys]
        return api_keys
