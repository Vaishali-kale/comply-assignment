from __future__ import annotations

import re
import statistics
from pathlib import Path
from collections import Counter
from typing import Any

import fitz


# =========================
# TEXT CLEANING
# =========================

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "")
    return text.strip()


# =========================
# REPEATED HEADER / FOOTER
# =========================

def find_repeated_headers_footers(lines):
    counter = Counter()

    for line in lines:

        if line["y"] < 55 or line["y"] > 730:

            text = line["text"]

            if 3 <= len(text) <= 150:
                counter[text] += 1

    return {
        text
        for text, count in counter.items()
        if count >= 3
    }


# =========================
# BODY FONT SIZE
# =========================

def calculate_body_font_size(lines):

    sizes = []

    for line in lines:

        size = line["font_size"]

        if 8 <= size <= 13 and len(line["text"]) > 20:
            sizes.append(size)

    if sizes:
        return statistics.median(sizes)

    if lines:
        return statistics.median(
            line["font_size"]
            for line in lines
        )

    return 10


# =========================
# HEADING DETECTION
# =========================

def is_heading(line, body_font_size):

    text = line["text"]

    font_size = line["font_size"]

    bold = line["bold"]

    score = 0

    # Larger font
    if font_size >= body_font_size * 1.25:
        score += 3

    elif font_size >= body_font_size * 1.10:
        score += 1

    # Bold
    if bold:
        score += 2

    # Short text is more likely to be heading
    if len(text) <= 80:
        score += 1

    # Numbered headings
    if re.match(
        r"^\d+(\.\d+)*\s+\S+",
        text
    ):
        score += 1

    # Letter headings
    if re.match(
        r"^[A-Z][.)]\s+\S+",
        text
    ):
        score += 1

    # Don't classify metadata as headings
    metadata_patterns = [
        "SERFF Tracking",
        "State Tracking",
        "Company Tracking",
        "State:",
        "Filing Company:",
        "TOI/Sub-TOI:",
        "Product Name:",
        "Project Name/Number:",
    ]

    for pattern in metadata_patterns:

        if text.lower().startswith(
            pattern.lower()
        ):
            return False

    return score >= 3


# =========================
# CREATE SECTIONS
# =========================

def create_sections(lines):

    if not lines:
        return []

    body_font_size = calculate_body_font_size(lines)

    repeated = find_repeated_headers_footers(lines)

    sections = []

    current_section = None

    for line in lines:

        text = line["text"]

        # Skip repeated headers / footers
        if text in repeated:
            continue

        heading = is_heading(
            line,
            body_font_size
        )

        if heading:

            # Save previous section
            if current_section:

                current_section["text"] = clean_text(
                    current_section["text"]
                )

                if current_section["text"]:
                    sections.append(
                        current_section
                    )

            # Confidence
            confidence = 0.75

            if line["bold"]:
                confidence += 0.10

            if line["font_size"] >= body_font_size * 1.25:
                confidence += 0.10

            confidence = min(
                confidence,
                0.99
            )

            current_section = {
                "heading": text,
                "text": "",
                "page": line["page"],
                "level": 1,
                "confidence": round(
                    confidence,
                    2
                )
            }

        else:

            # Content before first heading
            if current_section is None:

                current_section = {
                    "heading": "Document content",
                    "text": "",
                    "page": line["page"],
                    "level": 1,
                    "confidence": 0.50
                }

            if current_section["text"]:
                current_section["text"] += " "

            current_section["text"] += text

    # Save final section
    if current_section:

        current_section["text"] = clean_text(
            current_section["text"]
        )

        if current_section["text"]:
            sections.append(
                current_section
            )

    return sections


# =========================
# PDF EXTRACTION
# =========================

def extract_pdf(path: str) -> dict[str, Any]:

    doc = fitz.open(path)

    lines = []

    # Extract text with layout information
    for page_number, page in enumerate(
        doc,
        start=1
    ):

        page_dict = page.get_text(
            "dict",
            sort=True
        )

        for block in page_dict.get(
            "blocks",
            []
        ):

            if "lines" not in block:
                continue

            for raw_line in block["lines"]:

                spans = [
                    span
                    for span in raw_line.get(
                        "spans",
                        []
                    )
                    if clean_text(
                        span.get(
                            "text",
                            ""
                        )
                    )
                ]

                if not spans:
                    continue

                text = clean_text(
                    " ".join(
                        span["text"]
                        for span in spans
                    )
                )

                sizes = [
                    float(
                        span.get(
                            "size",
                            10
                        )
                    )
                    for span in spans
                ]

                font_size = max(sizes)

                bold = any(
                    (
                        "bold"
                        in str(
                            span.get(
                                "font",
                                ""
                            )
                        ).lower()
                    )
                    or (
                        int(
                            span.get(
                                "flags",
                                0
                            )
                        )
                        & 16
                    )
                    for span in spans
                )

                bbox = raw_line.get(
                    "bbox",
                    [0, 0, 0, 0]
                )

                lines.append(
                    {
                        "text": text,
                        "page": page_number,
                        "font_size": round(
                            font_size,
                            2
                        ),
                        "bold": bool(bold),
                        "x": float(bbox[0]),
                        "y": float(bbox[1]),
                        "height": float(
                            bbox[3] - bbox[1]
                        )
                    }
                )

    # Create sections
    sections = create_sections(lines)

    characters = sum(
        len(section["heading"])
        + len(section["text"])
        for section in sections
    )

    headings = [
        section
        for section in sections
        if section["heading"]
        != "Document content"
    ]

    body_font_size = calculate_body_font_size(
        lines
    )

    return {
        "filename": Path(path).name,

        "pages": len(doc),

        "sections": sections,

        "stats": {
            "headings": len(headings),
            "sections": len(sections),
            "characters": characters,
            "body_font_size": round(
                body_font_size,
                2
            )
        }
    }


# =========================
# TEST
# =========================

if __name__ == "__main__":

    pdf_path = (
        "C:/Users/ADMIN/Desktop/"
        "comply-assignment/backend/"
        "AMGN-135003565.pdf"
    )

    result = extract_pdf(
        pdf_path
    )

    print(
        "Filename:",
        result["filename"]
    )

    print(
        "Pages:",
        result["pages"]
    )

    print(
        "Headings:",
        result["stats"]["headings"]
    )

    print(
        "Sections:",
        result["stats"]["sections"]
    )

    print("\nSections:\n")

    for section in result["sections"]:

        print(
            f"[Page {section['page']}] "
            f"{section['heading']}"
        )

        print(
            section["text"][:300]
        )

        print("-" * 60)