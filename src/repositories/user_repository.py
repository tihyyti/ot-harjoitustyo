# Refactoroitu, aiemmin generoitu koodi alkaa
# expanded user-record of repositories/user_repository.py
# SQLite: UserRepository: create, find_by_username, authenticate

import sqlite3
import uuid
import hashlib
import os
from typing import Optional

# Import the User dataclass from the package
from repositories.models import User


def _hash_password(password: str, salt: bytes, iterations: int = 100_000) -> str:
    # pbkdf2_hmac tuottaa bytes; palautetaan hex
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return dk.hex()


class UserRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path
        # Varmista, että DB on olemassa ja taulut luotu (create_db.py huolehtii, mutta lisätään varmistus)
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database not found: {db_path}")

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create_user(self, username: str, password: str, **kwargs) -> User:
        # generoi uuid ja salt
        user_id = str(uuid.uuid4())
        salt = os.urandom(16)
        password_hash = _hash_password(password, salt)

        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO "user" (
                    user_id, username, password_hash, salt, weight, length, age,
                    activity_level, allergies, kcal_min, kcal_max, weight_loss_target
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    user_id,
                    username,
                    password_hash,
                    salt.hex(),
                    kwargs.get("weight"),
                    kwargs.get("length"),
                    kwargs.get("age"),
                    kwargs.get("activity_level"),
                    kwargs.get("allergies"),
                    kwargs.get("kcal_min"),
                    kwargs.get("kcal_max"),
                    kwargs.get("weight_loss_target"),
                ),
            )
            conn.commit()

        return User(
            user_id=user_id,
            username=username,
            password_hash=password_hash,
            salt=salt.hex(),
            weight=kwargs.get("weight"),
            length=kwargs.get("length"),
            age=kwargs.get("age"),
            activity_level=kwargs.get("activity_level"),
            allergies=kwargs.get("allergies"),
            kcal_min=kwargs.get("kcal_min"),
            kcal_max=kwargs.get("kcal_max"),
            weight_loss_target=kwargs.get("weight_loss_target"),
        )

    def find_by_username(self, username: str) -> Optional[User]:
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM "user" WHERE username = ?', (username,))
            row = cur.fetchone()
            if not row:
                return None
            return User(
                user_id=row["user_id"],
                username=row["username"],
                password_hash=row["password_hash"],
                salt=row["salt"],
                weight=row["weight"],
                length=row["length"],
                age=row["age"],
                activity_level=row["activity_level"],
                allergies=row["allergies"],
                kcal_min=row["kcal_min"],
                kcal_max=row["kcal_max"],
                weight_loss_target=row["weight_loss_target"],
            )

    def authenticate(self, username: str, password: str) -> bool:
        user = self.find_by_username(username)
        if not user:
            return False
        salt = bytes.fromhex(user.salt)
        expected = _hash_password(password, salt)
        return expected == user.password_hash


# Refactoroitu, aiemmin generoitu koodi päättyy
