import hashlib
import secrets


def hash_password(password: str) -> str:
    """
    パスワードをハッシュ化する（簡易版）

    注意: これはインターンシップ課題用の簡易実装です。
    実際のプロダクションではbcryptやArgon2などの専用ライブラリを使用すべきです。
    """
    # ソルトを生成
    salt = secrets.token_hex(16)
    # パスワードとソルトを結合してハッシュ化
    password_hash = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    # ソルトとハッシュを結合して保存
    return f"{salt}${password_hash}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    パスワードを検証する（簡易版）
    """
    try:
        # ソルトとハッシュを分離
        salt, stored_hash = hashed_password.split("$")
        # 同じソルトでハッシュ化
        password_hash = hashlib.sha256(f"{plain_password}{salt}".encode()).hexdigest()
        # ハッシュを比較
        return secrets.compare_digest(password_hash, stored_hash)
    except ValueError:
        # 旧形式（ハッシュ化されていない）の場合は直接比較
        # インターンシップ課題用の後方互換性
        return secrets.compare_digest(plain_password, hashed_password)
