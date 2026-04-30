# QR Code Generator
# This program generates a QR Code for a given URL of a photo album. 
# It uses the segno library to create the QR code 
# and uses io to save the image as bytes.
# Author: Stephen Kerr

import segno
import io

def generate_qr(url: str, scale: int = 10) -> bytes:
    """Generate a QR code for the given URL and return PNG bytes."""
    qr = segno.make(url, error="h")
    
    buffer = io.BytesIO()
    qr.save(buffer, kind="png", scale=scale, dark="black", light="white")
    buffer.seek(0)
    return buffer.read()

if __name__ == "__main__":
    test_url = "http://google.com"
    qr_bytes = generate_qr(test_url)
    
    with open("test_qr.png", "wb") as f:
        f.write(qr_bytes)
    
    print("QR code generated and saved as test_qr.png")