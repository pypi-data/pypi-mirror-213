# type: ignore
from fastapi_utils.enums import StrEnum


class ReportFormat(StrEnum):
    JSON = "JSON"
    CSV = "CSV"

    def __str__(self):
        return str(self.value)
