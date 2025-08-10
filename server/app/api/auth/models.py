import bcrypt
import jwt

from   datetime         import datetime, timedelta, timezone
from   typing           import Dict

from   fastapi.security import APIKeyHeader
from   fastapi          import HTTPException, status, Depends

from app.constants.constants import ALGORITHM, SECRET_KEY

api_key_header = APIKeyHeader(name="Authorization")


class Authentification:

    # хэширование пароля
    @staticmethod
    def hash_password(password: str) -> str:
        # Генерация соли
        salt   = bcrypt.gensalt()
        # Хеширование пароля с использованием соли
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

        return hashed.decode('utf-8')

    # создаем токен доступа
    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode   = data.copy()
        expire      = datetime.now(timezone.utc) + timedelta(minutes=30)
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    # обновляем токен
    @staticmethod
    def create_refresh_token(data: dict) -> str:
        to_encode   = data.copy()
        expire      = datetime.now(timezone.utc) + timedelta(days=15)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    # зависимсоть для токена
    @staticmethod
    def get_current_user(token: str = Depends(api_key_header)) -> Dict:
        try:
            if token.startswith("Bearer "):
                token = token.split(" ")[1]

            payload    = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            login      = payload.get("sub")
            token_id   = payload.get("id")
            type_token = payload.get("type")
            role       = payload.get("role")
            stat       = payload.get("status")

            if login is None or type_token != "access":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

            return {"username": login, "id": token_id, "role": role, "status": stat}

        except jwt.PyJWTError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

    @staticmethod
    def get_current_user_refresh(token: str = Depends(api_key_header)) -> Dict:
        try:
            if token.startswith("Bearer "):
                token = token.split(" ")[1]

            payload    = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            login      = payload.get("sub")
            token_id   = payload.get("id")
            type_token = payload.get("type")
            role       = payload.get("role")
            stat       = payload.get("status")

            if login is None or type_token != "refresh":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

            return {"username": login, "id": token_id, "role": role, "status": stat}

        except jwt.PyJWTError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
