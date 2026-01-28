

import sys
import os # プロジェクトルートを sys.path に追加
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import create_app, db

def main():
    app = create_app()

    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()

        print("Creating new tables...")
        db.create_all()

        print("Database initialized successfully.")

if __name__ == "__main__":
    main()
