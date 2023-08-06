from typing import TYPE_CHECKING, Any, Dict

from pydantic import AnyUrl

if TYPE_CHECKING:
    from pydantic.config import BaseConfig
    from pydantic.fields import ModelField


class GcsPath(AnyUrl):
    allowed_schemes = {"gcs", "gs"}

    __slots__ = ()

    @classmethod
    def validate(
        cls, value: Any, field: "ModelField", config: "BaseConfig"
    ) -> "AnyUrl":
        if isinstance(value, Dict):
            _value = value.get("bucket")
            if not _value:
                raise ValueError("Received a wrong bucket definition: %s", value)
            if "://" not in _value:
                _value = "gs://{}".format(_value)
            blob = value.get("blob")
            if blob:
                _value = "{}/{}".format(_value, blob)
            value = _value
        return super(GcsPath, cls).validate(value=value, field=field, config=config)

    def to_param(self):
        return str(self)

    @property
    def structured(self):
        return dict(bucket=self.host, blob=self.path.strip("/"))
