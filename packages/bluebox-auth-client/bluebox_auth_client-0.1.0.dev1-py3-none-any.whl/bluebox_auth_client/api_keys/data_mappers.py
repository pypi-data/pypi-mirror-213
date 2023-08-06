from datetime import datetime

from .entities import ApiKey
from .proto import api_keys_objects_pb2


class ApiKeyDataMapper:
    @staticmethod
    def proto_model_to_entity(proto_model: api_keys_objects_pb2.ApiKey) -> ApiKey:
        created_at = proto_model.created_at
        created_at_dt = datetime.fromtimestamp(created_at.seconds + created_at.nanos / 1e9)
        return ApiKey(
            key_id=proto_model.key_id,
            name=proto_model.name,
            description=proto_model.description,
            created_at=created_at_dt,
        )
