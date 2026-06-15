"""Render PDF pages to base64 PNG images for vision-model analysis."""
import base64

import fitz  # PyMuPDF


def pdf_to_images_b64(file_bytes, dpi=150, max_pages=20):
    """Return a list of base64-encoded PNG strings, one per page (capped)."""
    images = []
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)
    for page_index in range(min(len(doc), max_pages)):
        page = doc.load_page(page_index)
        pix = page.get_pixmap(matrix=matrix)
        png_bytes = pix.tobytes("png")
        images.append(base64.b64encode(png_bytes).decode("utf-8"))
    doc.close()
    return images


def pdf_page_count(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    n = len(doc)
    doc.close()
    return n
