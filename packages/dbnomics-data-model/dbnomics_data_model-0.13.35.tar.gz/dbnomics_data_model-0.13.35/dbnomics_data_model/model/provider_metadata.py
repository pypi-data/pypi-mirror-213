"""Provider model."""

from typing import Optional

from pydantic import BaseModel, HttpUrl, constr

__all__ = ["ProviderMetadata"]


class ProviderMetadata(BaseModel):
    """Metadata about a provider."""

    code: constr(regex="^[-0-9A-Za-z._]+$")  # type:ignore # noqa: F722
    website: HttpUrl

    attribution: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    region: Optional[str] = None
    terms_of_use: Optional[HttpUrl] = None

    def merge(self, other: "ProviderMetadata") -> "ProviderMetadata":
        """Return a copy of the instance merged with `other`."""
        assert self.code == other.code, (self, other)
        return self.copy(update={**dict(other)})
