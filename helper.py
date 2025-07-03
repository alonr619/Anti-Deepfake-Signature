from PIL import Image, PngImagePlugin

import base64
import piexif


def add_text_as_metadata(image: Image.Image, signature_bytes: bytes, filename: str):
    if image.format == 'PNG':
        signature_b64 = base64.b64encode(signature_bytes).decode('utf-8')
        print(signature_b64)
        meta = PngImagePlugin.PngInfo()
        meta.add_text('signature', signature_b64)
        print(meta)
        image.save(f"uploads/signed_{filename}", pnginfo=meta)
        print(image.info)
    
    elif image.format == 'JPEG' or image.format == 'JPG':
        exif_dict = piexif.load(image.info.get('exif', b""))
        exif_dict['0th'][piexif.ImageIFD.ImageDescription] = base64.b64encode(signature_bytes).decode('utf-8')
        exif_bytes = piexif.dump(exif_dict)
        image.save(f"uploads/signed_{filename}", 'JPEG', exif=exif_bytes)
    
    else:
        raise ValueError(f'Unsupported image format: {image.format}')