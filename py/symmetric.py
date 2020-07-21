from cryptography.fernet import Fernet


def encrypt(
        key: bytes,
        body: bytes
) -> bytes:
    f = Fernet(key)
    encrypted = f.encrypt(body)
    return encrypted


def encrypt_file(
        key: bytes,
        file_name: bytes
) -> bytes:
    with open(file_name.decode("utf-8"), "rb") as f:
        contents = f.read()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(contents)
        return encrypted


def decrypt(
        key: bytes,
        body: bytes
) -> bytes:
    f = Fernet(key)
    decrypted = f.decrypt(body)
    return decrypted


def decrypt_file(
        key: bytes,
        file_name: bytes
) -> bytes:
    with open(file_name.decode("utf-8"), "rb") as f:
        contents = f.read()
        fernet = Fernet(key)
        decrypted = fernet.decrypt(contents)
        return decrypted


def generate_key() -> bytes:
    return Fernet.generate_key()
