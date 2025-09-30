import qrcode
import io
from fastapi.responses import StreamingResponse

def generate_qr(batch_id: str):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(f"https://demo.com/provenance/{batch_id}")  # Replace with real portal later
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
