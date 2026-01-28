import sys
import os

# プロジェクトルートを sys.path に追加
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from app.models import Payment, Business, Station


def main():
    app = create_app()

    with app.app_context():
        print("Seeding initial data...")

        # 既存データ削除（開発中は便利）
        Payment.query.delete()
        Business.query.delete()
        Station.query.delete()

        # Payment
        payments = [
            Payment(name="現金"),
            Payment(name="クレジット"),
        ]

        # Business
        businesses = [
            Business(name="新規購入"),
            Business(name="変更"),
            Business(name="払戻"),
        ]

        # Station
        stations = [
            Station(name="越前たけふ", prefix=1, last_number=0),
            Station(name="福井", prefix=2, last_number=0),
            Station(name="芦原温泉", prefix=3, last_number=0),
        ]

        db.session.add_all(payments)
        db.session.add_all(businesses)
        db.session.add_all(stations)
        db.session.commit()

        print("Seed data inserted successfully.")


if __name__ == "__main__":
    main()
