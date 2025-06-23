import cv2
import numpy as np
from PIL import Image
import pytesseract
from pathlib import Path
from datetime import datetime
import argparse
import yaml
import os
import logging
from concurrent.futures import ProcessPoolExecutor

# Set up a default config dictionary to hold tweakable parameters, mostly useful if I want to tune things for different scan types

default_config = {
    'mode': 'bilevel',       # I'm sticking with bilevel for now — gives me crisp black/white output for notation
    'threshold': 'sauvola',  # Sauvola works best for sheet music since it handles contrast well in thin lines
    'median_kernel': 5,      # Keeping this small to avoid destroying staff lines
    'adaptive_block': 25,    # Slightly larger block gives smoother results in uniform areas
    'adaptive_C': 10,
    'dpi': 300,               # Output PDF resolution
    'quality': 95,           # Output image quality for JPEG
    'lang': 'eng',           # Just here in case I toggle OCR later
    'whitelist': None,
    'processes': 1,          # Can batch later if needed
    'verbose': False,
    'no_ocr': True,          # Don't rotate based on OCR — this is sheet music, not text
    'pdf': True,             # PDF output for easy storage or printing
}

# Load YAML config file if I want to override defaults later

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

# Let me toggle debug logging with a flag — super handy for debugging threshold issues

def setup_logging(verbose):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=level)

# Order points (corners) for perspective transform — just geometry sorting stuff

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0], rect[2] = pts[np.argmin(s)], pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1], rect[3] = pts[np.argmin(diff)], pts[np.argmax(diff)]
    return rect

# Try to find the biggest rectangular-ish contour — assumes page is largest shape

def find_document_contour(image, target_height=700):
    ratio = image.shape[0] / target_height
    resized = cv2.resize(image, (int(image.shape[1] / ratio), target_height))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)  # Using small blur kernel to keep staff lines from vanishing
    edged = cv2.Canny(blur, 50, 150)          # Can tweak thresholds later if needed
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in sorted(contours, key=cv2.contourArea, reverse=True):
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            return approx.reshape(4, 2) * ratio
    return None  # If nothing good found, fallback to original image later

# Take 4 corner points and do a proper perspective warp to flatten the page

def warp_perspective(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    width = int(max(np.linalg.norm(br - bl), np.linalg.norm(tr - tl)))
    height = int(max(np.linalg.norm(tr - br), np.linalg.norm(tl - bl)))
    dst = np.array([[0,0], [width-1,0], [width-1,height-1], [0,height-1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(image, M, (width, height))

# Use this to clean up lighting variations using median-blurred background subtraction

def remove_background(gray, ksize):
    bg = cv2.medianBlur(cv2.dilate(gray, np.ones((ksize,ksize), np.uint8)), ksize*3)
    diff = 255 - cv2.absdiff(gray, bg)
    return cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX)

# Helps reinforce horizontal staff lines so they don't break up during binarization

def enhance_staff_lines(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))  # Vertical dilation/erosion keeps staff lines solid
    return cv2.erode(cv2.dilate(img, kernel), kernel)

# Main thresholding logic with different methods depending on what's set in config

def threshold_image(gray, cfg):
    clean = remove_background(gray, cfg['median_kernel'])
    blur = cv2.GaussianBlur(clean, (3,3), 0)
    method = cfg['threshold']
    if method == 'adaptive':
        out = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, cfg['adaptive_block'], cfg['adaptive_C'])
    elif method == 'otsu':
        _, out = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif method == 'sauvola':
        window = cfg['adaptive_block']
        mean = cv2.blur(blur, (window, window))
        sqmean = cv2.blur(blur*blur, (window, window))
        std = np.sqrt(sqmean - mean*mean)
        R = std.max()
        k = 0.3
        thresh = mean * (1 + k * ((std / R) - 1))
        out = (blur >= thresh).astype(np.uint8)*255
    else:
        logging.warning(f"Unknown threshold {method}, using adaptive")
        return threshold_image(gray, {**cfg, 'threshold':'adaptive'})

    return enhance_staff_lines(out)  # Strengthen horizontal lines post-threshold

# Skipped OCR rotation because it's sheet music — we don't want it trying to straighten based on words

def fix_orientation(pil_img):
    return pil_img

# Process a single image from path ? enhanced + saved to output path

def process_single_image(input_path, output_path, cfg):
    img = cv2.imread(str(input_path))
    if img is None:
        logging.error(f"Failed to load {input_path}")
        return None

    pts = find_document_contour(img)
    warped = warp_perspective(img, pts) if pts is not None else img

    if cfg['mode'] == 'bilevel':
        gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        proc = threshold_image(gray, cfg)
    elif cfg['mode'] == 'grayscale':
        proc = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    else:
        proc = warped  # Color mode, skip conversion

    pil = Image.fromarray(proc)
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pil.save(str(out_path), quality=cfg['quality'])

    if cfg['pdf']:
        pdf_path = out_path.with_suffix('.pdf')
        pil.save(str(pdf_path), 'PDF', resolution=cfg['dpi'])
        logging.info(f"Saved to {out_path} and {pdf_path}")
    else:
        logging.info(f"Saved to {out_path}")

# Set up CLI entry point — this lets me use it from terminal just like:
# python scanner.py --verbose in/IMG.jpg out/IMG_fixed.png

def main():
    parser = argparse.ArgumentParser(description="Document Scanner")
    parser.add_argument('input', help="Input image path")
    parser.add_argument('output', help="Output image path")
    parser.add_argument('--verbose', action='store_true', help="Enable verbose logging")
    args = parser.parse_args()

    cfg = default_config.copy()
    setup_logging(args.verbose)
    process_single_image(args.input, args.output, cfg)

if __name__ == '__main__':
    main()

# Usage example:
# python scanner.py --verbose in/IMG_5107.jpg out/IMG_5107_enhanced.png
