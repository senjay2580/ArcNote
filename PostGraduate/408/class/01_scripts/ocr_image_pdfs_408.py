from __future__ import annotations

from pathlib import Path

import easyocr
import fitz
import numpy as np
from PIL import Image


ROOT = Path(r"D:\Desktop\ArcNote\PostGraduate\408\class")
PDFS = [
    Path(r"D:\Desktop\ArcNote\PostGraduate\答题卡\计算机408历年真题\2024计算机408真题+解析\25王道408历年真题.pdf"),
    Path(r"D:\Desktop\ArcNote\PostGraduate\答题卡\计算机408历年真题\2025计算机408真题+解析\2025年计算机408统考真题及答案.pdf"),
]


def safe_stem(path: Path) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in path.stem)


def main() -> None:
    out_dir = ROOT / "ocr_cache"
    out_dir.mkdir(parents=True, exist_ok=True)

    reader = easyocr.Reader(["ch_sim", "en"], gpu=False, verbose=False)
    for pdf in PDFS:
        out = out_dir / f"{safe_stem(pdf)}.txt"
        if out.exists() and out.stat().st_size > 1000:
            print(f"skip cached: {out}")
            continue

        print(f"OCR: {pdf.name}", flush=True)
        parts: list[str] = []
        with fitz.open(pdf) as doc:
            for i, page in enumerate(doc, 1):
                pix = page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0), alpha=False)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                lines = reader.readtext(np.array(img), detail=0, paragraph=True)
                text = "\n".join(lines)
                parts.append(f"\n\n===== PAGE {i} =====\n{text}")
                out.write_text("\n".join(parts), encoding="utf-8")
                print(f"  page {i}/{len(doc)} chars={len(text)}", flush=True)

        print(f"saved: {out}", flush=True)


if __name__ == "__main__":
    main()
