from PIL import Image, PngImagePlugin
import base64
import piexif
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def get_hash_from_image(image: Image.Image) -> SHA256.SHA256Hash:
    img_data = image.convert('RGB').tobytes()
    hash = SHA256.new(img_data)
    return hash

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

def verify_signature(image: Image.Image, public_key: RSA.RsaKey):
    if image.format == 'PNG':
        signature_b64 = image.info['signature']
        signature_bytes = base64.b64decode(signature_b64)
        hash = get_hash_from_image(image)
        verifier = pkcs1_15.new(public_key)
        try:
            verifier.verify(hash, signature_bytes)
            return True
        except Exception as e:
            return False