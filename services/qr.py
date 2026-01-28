import qrcode
import base64
from io import BytesIO

def generate_qr_base64(data: str) -> str:
    """QRコードを生成し、base64文字列として返す"""

    qr = qrcode.QRCode(
        version=1,
        box_size=8,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # base64 に変換
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_base64
