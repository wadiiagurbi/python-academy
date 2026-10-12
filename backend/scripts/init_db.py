#!/usr/bin/env python
"""Initialize database with tables."""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.config import settings
from app.core.database import init_db

async def main():
    print(f"Initializing database at: {settings.DATABASE_URL}")
    await init_db()
    print("Database initialized successfully!")

if __name__ == "__main__":
    asyncio.run(main())