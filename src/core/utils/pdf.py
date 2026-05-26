"""
PDF utilities for extracting text from uploaded resumes.

These helpers are used by the API layer to transparently convert a base64-encoded
PDF resume into plain text before passing it into agents.
"""

from __future__ import annotations

import base64
from io import BytesIO
from typing import Optional

from pypdf import PdfReader


def extract_text_from_pdf_bytes(data: bytes) -> str:
    """Extract text from raw PDF bytes."""
    reader = PdfReader(BytesIO(data))
    pages_text = []
    for page in reader.pages:
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            pages_text.append(text)
    return "\n\n".join(pages_text)


