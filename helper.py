from inspect import signature
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

def get_signature_from_hash(hash: SHA256.SHA256Hash, private_key: RSA.RsaKey) -> bytes:
    return pkcs1_15.new(private_key).sign(hash)

def save_image_with_metadata(image: Image.Image, signature_bytes: bytes, filename: str):
    if image.format == 'PNG':
        signature_b64 = base64.b64encode(signature_bytes).decode('utf-8')
        meta = PngImagePlugin.PngInfo()
        meta.add_text('signature', signature_b64)
        image.save(f"uploads/signed_{filename}", pnginfo=meta)
    
    elif image.format == 'JPEG' or image.format == 'JPG':
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
        exif_dict['0th'][piexif.ImageIFD.ImageDescription] = base64.b64encode(signature_bytes)
        exif_bytes = piexif.dump(exif_dict)
        image.save(f"uploads/signed_{filename}", exif=exif_bytes)
    
    else:
        raise ValueError(f'Unsupported image format: {image.format}')

def retrieve_signature_from_image(image: Image.Image) -> bytes:
    if image.format == 'PNG':
        signature_b64 = image.info['signature']
        return base64.b64decode(signature_b64)
    elif image.format == 'JPEG' or image.format == 'JPG':
        exif_dict = piexif.load(image.info.get('exif', b""))
        signature_b64 = exif_dict['0th'][piexif.ImageIFD.ImageDescription]
        print(signature_b64)
        return base64.b64decode(signature_b64)
    else:
        raise ValueError(f'Unsupported image format: {image.format}')

def verify_image_signature(image: Image.Image, public_key: RSA.RsaKey):
    signature_bytes = retrieve_signature_from_image(image)
    hash = get_hash_from_image(image)
    verifier = pkcs1_15.new(public_key)
    try:
        verifier.verify(hash, signature_bytes)
        return True
    except Exception as e:
        return False