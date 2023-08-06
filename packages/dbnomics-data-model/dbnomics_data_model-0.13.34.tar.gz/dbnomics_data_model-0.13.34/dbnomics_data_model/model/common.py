"""Common types for model."""


__all__ = [
    "CategoryCode",
    "DatasetCode",
    "ProviderCode",
    "SeriesCode",
    "AttributeCode",
    "AttributeValueCode",
    "DimensionCode",
    "DimensionValueCode",
]

dataset_code_re = "^[-0-9A-Za-z._:]+$"
series_code_re = "^[^/ ]+$"

CategoryCode = str
DatasetCode = str
ProviderCode = str
SeriesCode = str

AttributeCode = str
AttributeValueCode = str

DimensionCode = str
DimensionValueCode = str
