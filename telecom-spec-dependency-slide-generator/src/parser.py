from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable, List, Mapping, Optional

from .models import Document


SECTION_SPLIT_PATTERN = re.compile(r"\n(?=(?:\d+(?:\.\d+)*)\s+.+|[A-Z][A-Z\s\-/]{4,})")
WHITESPACE_PATTERN = re.compile(r"\s+")


class DocumentParser:
    """Parse raw telecom specification text into normalized document objects."""

    def parse_text(
        self,
        text: str,
        *,
        document_id: str,
        title: str,
        domain: str,
        version: Optional[str] = None,
        organization: Optional[str] = None,
        summary: Optional[str] = None,
    ) -> Document:
        normalized_text = self.normalize_text(text)
        sections = self.split_sections(normalized_text)
        return Document(
            id=document_id,
            title=title,
            domain=domain,
            version=version,
            organization=organization,
            summary=summary,
            sections=sections,
            raw_text=normalized_text,
        )

    def parse_file(
        self,
        path: str | Path,
        *,
        document_id: str,
        title: str,
        domain: str,
        version: Optional[str] = None,
        organization: Optional[str] = None,
        summary: Optional[str] = None,
        encoding: str = "utf-8",
    ) -> Document:
        file_path = Path(path)
        text = file_path.read_text(encoding=encoding)
        return self.parse_text(
            text,
            document_id=document_id,
            title=title,
            domain=domain,
            version=version,
            organization=organization,
            summary=summary,
        )

    def parse_many(self, documents: Iterable[Mapping[str, Any]]) -> List[Document]:
        parsed: List[Document] = []
        for item in documents:
            parsed.append(
                self.parse_text(
                    str(item["text"]),
                    document_id=str(item["id"]),
                    title=str(item["title"]),
                    domain=str(item["domain"]),
                    version=self._optional_str(item.get("version")),
                    organization=self._optional_str(item.get("organization")),
                    summary=self._optional_str(item.get("summary")),
                )
            )
        return parsed

    @staticmethod
    def normalize_text(text: str) -> str:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        lines = [WHITESPACE_PATTERN.sub(" ", line).strip() for line in text.split("\n")]
        cleaned = "\n".join(lines)
        return cleaned.strip()

    @staticmethod
    def split_sections(text: str) -> List[str]:
        if not text:
            return []
        sections = [section.strip() for section in SECTION_SPLIT_PATTERN.split(text) if section.strip()]
        return sections or [text]

    @staticmethod
    def _optional_str(value: object) -> Optional[str]:
        if value is None:
            return None
        return str(value)
