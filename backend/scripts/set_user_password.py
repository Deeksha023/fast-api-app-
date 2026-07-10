import asyncio
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(backend_dir / ".runtime-pkgs"))

from sqlalchemy.future import select

from database import SessionLocal
from models.Users import Users
from utils.security import hash_password


async def main(email: str, password: str) -> None:
    async with SessionLocal() as db:
        result = await db.execute(select(Users).filter(Users.email == email))
        user = result.scalars().first()

        if user is None:
            user = Users(
                username=email,
                email=email,
                hashed_password=hash_password(password),
                role="Candidate",
            )
            db.add(user)
            action = "created"
        else:
            user.hashed_password = hash_password(password)
            action = "updated"

        await db.commit()
        print(f"{action} {email}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: set_user_password.py <email> <password>")

    asyncio.run(main(sys.argv[1], sys.argv[2]))
