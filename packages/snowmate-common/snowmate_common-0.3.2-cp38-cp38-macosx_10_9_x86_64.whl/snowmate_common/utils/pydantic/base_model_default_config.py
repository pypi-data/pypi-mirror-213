from datetime import datetime, timezone

from bson import ObjectId


class DefaultConfig:
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {
        ObjectId: str,
        datetime: lambda d: datetime.replace(d, tzinfo=timezone.utc).isoformat(),
    }
    validate_all = True
    validate_assignment = True
