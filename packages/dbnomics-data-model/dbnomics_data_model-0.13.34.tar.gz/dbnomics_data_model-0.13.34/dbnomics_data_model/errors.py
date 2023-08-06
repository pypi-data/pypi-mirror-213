"""DBnomics data model errors."""


__all__ = ["DBnomicsDataModelError", "DBnomicsValidationError"]


class DBnomicsDataModelError(Exception):
    """Error about DBnomics data model."""


class DBnomicsValidationError(DBnomicsDataModelError):
    """Validation error for a DBnomics data model instance."""
