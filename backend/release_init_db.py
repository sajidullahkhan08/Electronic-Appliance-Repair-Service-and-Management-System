"""
release_init_db.py
==================
Railway runs this script during the RELEASE PHASE (before the app starts).
It creates the database, tables, and default admin if they don't already exist.

Railway runs: python release_init_db.py
"""

import sys
from dotenv import load_dotenv

load_dotenv()

from config import Config
from init_db import init


def main():
    print("=" * 50)
    print("  ElectroFix — Release Phase DB Init")
    print(f"  Host : {Config.MYSQL_HOST}:{Config.MYSQL_PORT}")
    print(f"  DB   : {Config.MYSQL_DB}")
    print("=" * 50)
    try:
        init()
        print("[OK] Release init complete.")
    except Exception as e:
        print(f"[ERROR] Release init failed: {e}")
        sys.exit(1)   # Non-zero exit tells Railway the release failed


if __name__ == "__main__":
    main()
