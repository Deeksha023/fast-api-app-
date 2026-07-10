import asyncio
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(backend_dir / ".runtime-pkgs"))

from sqlalchemy.future import select

from database import SessionLocal
from models.Users import Users


async def main(email: str, role: str) -> None:
    normalized_email = email.strip().lower()
    normalized_role = role.strip()

    async with SessionLocal() as db:
        result = await db.execute(select(Users).filter(Users.email == normalized_email))
        user = result.scalars().first()
        if user is None:
            raise SystemExit(f"User not found: {email}")

        user.role = normalized_role
        await db.commit()
        print(f"updated {normalized_email} role to {normalized_role}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: set_user_role.py <email> <role>")

    asyncio.run(main(sys.argv[1], sys.argv[2]))
