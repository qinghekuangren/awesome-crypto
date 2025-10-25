"""Example script demonstrating how to locate a target serial number or QR code in an image."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

import cv2
import numpy as np
import pytesseract


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path, help="Path to the image to analyze")
    parser.add_argument(
        "--serial",
        type=str,
        default=None,
        help="Target serial number to locate via OCR (e.g. SB-00192)",
    )
    parser.add_argument(
        "--qr",
        action="store_true",
        help="Attempt to locate a QR code and display its contents",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display a preview window with any matches highlighted",
    )
    return parser.parse_args()


def load_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Unable to read image: {path}")
    return image


def preprocess_for_ocr(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def locate_serial_numbers(image: np.ndarray, target: str) -> List[Tuple[str, Tuple[int, int, int, int]]]:
    if not target:
        return []

    processed = preprocess_for_ocr(image)
    ocr_data = pytesseract.image_to_data(
        processed,
        output_type=pytesseract.Output.DICT,
        config="--psm 6",
    )

    matches: List[Tuple[str, Tuple[int, int, int, int]]] = []
    n_boxes = len(ocr_data["text"])
    for i in range(n_boxes):
        text = ocr_data["text"][i].strip()
        if not text:
            continue
        if target.lower() in text.lower():
            x, y, w, h = (
                ocr_data["left"][i],
                ocr_data["top"][i],
                ocr_data["width"][i],
                ocr_data["height"][i],
            )
            matches.append((text, (x, y, w, h)))
    return matches


def locate_qr_code(image: np.ndarray) -> Optional[Tuple[str, np.ndarray]]:
    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(image)
    if points is None or not data:
        return None
    return data, points


def draw_serial_matches(image: np.ndarray, matches: Iterable[Tuple[str, Tuple[int, int, int, int]]]) -> None:
    for text, (x, y, w, h) in matches:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            image,
            text,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )


def draw_qr_match(image: np.ndarray, points: np.ndarray) -> None:
    pts = points.astype(int).reshape(-1, 2)
    for i in range(len(pts)):
        pt1 = tuple(pts[i])
        pt2 = tuple(pts[(i + 1) % len(pts)])
        cv2.line(image, pt1, pt2, (255, 0, 0), 3)


def main() -> None:
    args = parse_args()
    image = load_image(args.image)

    serial_matches = locate_serial_numbers(image.copy(), args.serial)
    qr_result = locate_qr_code(image) if args.qr else None

    if serial_matches:
        print(f"Found {len(serial_matches)} serial match(es):")
        for match in serial_matches:
            text, (x, y, w, h) = match
            print(f"  '{text}' at x={x}, y={y}, w={w}, h={h}")
            draw_serial_matches(image, [match])
    elif args.serial:
        print(f"No matches found for serial number '{args.serial}'.")

    if qr_result:
        data, points = qr_result
        print(f"Detected QR code with payload: {data}")
        draw_qr_match(image, points)
    elif args.qr:
        print("No QR code detected.")

    if args.show and (serial_matches or qr_result):
        cv2.imshow("Matches", image)
        cv2.waitKey(0)
    elif args.show:
        print("Nothing to show: no matches found.")


if __name__ == "__main__":
    main()
