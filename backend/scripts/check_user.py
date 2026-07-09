import os
import sys
import asyncio
from sqlalchemy import text

# ensure backend package is importable
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import engine
from utils.security import verify_password

email = 'swagger@example.com'
plain = 'Test1234!'


async def main():
    async with engine.connect() as conn:
        result = await conn.execute(
            text("SELECT id,email,username,hashed_password,role FROM users WHERE email=:email"),
            {"email": email},
        )
        rows = result.fetchall()

    if not rows:
        print('NO_USER')
        return

    for row in rows:
        print(row)
        hashed = row[3]
        ok = verify_password(plain, hashed)
        print('PASSWORD_MATCH' if ok else 'PASSWORD_MISMATCH')


if __name__ == "__main__":
    asyncio.run(main())
