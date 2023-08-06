"""Module for parsing text files.."""
from typing import Iterator

from langplus.document_loaders.base import BaseBlobParser
from langplus.document_loaders.blob_loaders import Blob
from langplus.schema import Document


class TextParser(BaseBlobParser):
    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """Lazily parse the blob."""
        yield Document(page_content=blob.as_string(), metadata={"source": blob.source})
