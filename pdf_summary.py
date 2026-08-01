# ============================================================
# pdf_summary.py — PDF Summary CLI Tool
# ============================================================
# Usage:  python pdf_summary.py <path-to-pdf>
#
# Extracts text from a PDF, sends it to DeepSeek, and prints a
# structured summary with three sections:
#   Overview  |  Key Points (with [Page X] citations)  |  Limitations
# ============================================================

import argparse
import os
import sys

import pdfplumber
from dotenv import load_dotenv
from openai import OpenAI

# ---- Load environment variables ----
load_dotenv()

# DeepSeek model to use (matching the project convention from cli_qa.py)
MODEL = "deepseek-v4-flash"

# Hard character cap: documents exceeding this limit are truncated before
# the LLM call.  DeepSeek v4 supports a large context; this is a conservative
# guardrail that leaves headroom for the system prompt and response tokens.
MAX_CHARS = 60_000


# ---------------------------------------------------------------------------
# Step 1 — Extract text from the PDF
# ---------------------------------------------------------------------------
def extract_text(pdf_path: str) -> list[tuple[int, str]]:
    """
    Open a PDF and return a list of (page_number, text) for every page that
    contains extractable text.  Pages with no text (e.g. scanned images) are
    silently skipped.
    """
    pages: list[tuple[int, str]] = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text and text.strip():
                    pages.append((page.page_number, text.strip()))
    except FileNotFoundError:
        print(f"Error: file not found — '{pdf_path}'")
        print("Usage:  python pdf_summary.py <path-to-pdf>")
        sys.exit(1)

    return pages


# ---------------------------------------------------------------------------
# Step 2 — Build the LLM prompt from extracted pages
# ---------------------------------------------------------------------------
def build_prompt(pages: list[tuple[int, str]]) -> str:
    """
    Format the extracted pages into a single string with [Page N] markers
    so the LLM can cite sources.
    """
    parts: list[str] = []
    for page_num, text in pages:
        parts.append(f"[Page {page_num}]\n{text}")
    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Step 3 — Truncate pages to fit within the LLM context window
# ---------------------------------------------------------------------------
def truncate_pages(
    pages: list[tuple[int, str]], max_chars: int
) -> tuple[list[tuple[int, str]], int, int]:
    """
    Keep only as many pages as fit within *max_chars* (page-level truncation —
    a page is either kept in full or dropped entirely).

    Returns (kept_pages, kept_chars, dropped_chars).
    """
    kept: list[tuple[int, str]] = []
    used = 0
    for page_num, text in pages:
        # Account for the "[Page N]\n" marker plus the two-newline separator
        overhead = len(f"[Page {page_num}]\n") + (2 if kept else 0)
        if used + overhead + len(text) > max_chars:
            break
        kept.append((page_num, text))
        used += overhead + len(text)

    total = sum(len(t) for _, t in pages)
    return kept, used, total - used


# ---------------------------------------------------------------------------
# Step 4 — Call the DeepSeek LLM
# ---------------------------------------------------------------------------
def call_llm(document_text: str) -> str:
    """
    Send the document text to DeepSeek and return the three-section summary.
    The API key is read from the DEEPSEEK_API_KEY environment variable
    (loaded from .env by load_dotenv).
    """
    client = OpenAI(
        base_url="https://api.deepseek.com",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )

    system_prompt = (
        "You are a precise academic summariser. "
        "Read the document provided by the user and produce a structured summary.\n\n"
        "Output EXACTLY three sections with these Markdown headings:\n\n"
        "## Overview\n"
        "A 2-4 sentence paragraph describing what the document covers.\n\n"
        "## Key Points\n"
        "A bulleted list of the most important facts, claims, or findings.\n"
        "- Each bullet MUST end with a [Page X] citation.\n"
        "- Include 5-10 points depending on document length.\n\n"
        "## Limitations\n"
        "Note gaps, missing context, assumptions, or topics the document "
        "only briefly mentions.\n\n"
        "Rules:\n"
        "1. Use ONLY information present in the document.\n"
        "2. Every factual claim in Key Points MUST carry a [Page X] citation.\n"
        "3. Do not add external knowledge, opinions, or commentary.\n"
        "4. Write in clear, professional English."
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": document_text},
        ],
    )

    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# Step 5 — Main entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF and print a structured LLM summary."
    )
    parser.add_argument(
        "pdf_path",
        help="Path to the PDF file to summarise",
    )
    args = parser.parse_args()

    # ---- Extract ----
    pages = extract_text(args.pdf_path)

    if not pages:
        print(
            "No extractable text found in this PDF. "
            "It may be a scanned document or contain only images."
        )
        sys.exit(0)

    # ---- Guard: large documents → truncate ----
    total_chars = sum(len(text) for _, text in pages)
    if total_chars > MAX_CHARS:
        pages, kept_chars, dropped_chars = truncate_pages(pages, MAX_CHARS)
        print(
            f"Document is {total_chars:,} characters across {len(pages)} pages — "
            f"exceeds the limit of {MAX_CHARS:,} characters.\n"
            f"Only the first {kept_chars:,} characters "
            f"({len(pages)} page(s)) will be summarised. "
            f"The remaining {dropped_chars:,} characters are skipped.\n"
        )

    # ---- Build prompt & call LLM ----
    prompt = build_prompt(pages)
    summary = call_llm(prompt)

    # ---- Print result (only the summary; never the raw text or API key) ----
    print(summary)


if __name__ == "__main__":
    main()
