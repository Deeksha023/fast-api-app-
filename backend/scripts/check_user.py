import os
import sys
from sqlalchemy import text

# ensure backend package is importable
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import engine
from utils.security import verify_password

email = 'swagger@example.com'
plain = 'Test1234!'

with engine.connect() as conn:
    result = conn.execute(text("SELECT id,email,username,hashed_password,role FROM users WHERE email=:email"), {"email": email}).fetchall()
    if not result:
        print('NO_USER')
    else:
        for row in result:
            print(row)
            hashed = row[3]
            ok = verify_password(plain, hashed)
            print('PASSWORD_MATCH' if ok else 'PASSWORD_MISMATCH')
