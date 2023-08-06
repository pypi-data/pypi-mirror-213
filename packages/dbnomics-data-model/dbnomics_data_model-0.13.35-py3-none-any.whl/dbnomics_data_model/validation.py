from pydantic import BaseModel, Field

from dbnomics_data_model.errors import DBnomicsDataModelError
from dbnomics_data_model.model.common import DatasetCode
from dbnomics_data_model.model.series import DuplicateSeriesError


class Ignore(BaseModel):
    error_code: str
    dataset_codes: list[DatasetCode] = Field(default_factory=list)


class ValidationSettings(BaseModel):
    ignore: list[Ignore]

    def is_error_ignored(self, error: DBnomicsDataModelError) -> bool:
        if isinstance(error, DuplicateSeriesError):
            for ignore_item in self.ignore:
                if ignore_item.error_code == error.error_code and (
                    not ignore_item.dataset_codes or error.dataset_code in ignore_item.dataset_codes
                ):
                    return True
        return False
