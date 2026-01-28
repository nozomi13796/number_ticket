import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from app.models import Payment, Business, Station


def main():
    app = create_app()

    with app.app_context():
        print("Seeding initial data...")

        # Payment
        if Payment.query.count() == 0:
            payments = [
                Payment(name="現金"),
                Payment(name="クレジット"),
            ]
            db.session.add_all(payments)
            print("Payment seeded.")

        # Business
        if Business.query.count() == 0:
            businesses = [
                Business(name="新規購入"),
                Business(name="変更"),
                Business(name="払戻"),
            ]
            db.session.add_all(businesses)
            print("Business seeded.")

        # Station
        if Station.query.count() == 0:
            stations = [
                Station(name="越前たけふ", prefix=1, last_number=0),
                Station(name="福井", prefix=2, last_number=0),
                Station(name="芦原温泉", prefix=3, last_number=0),
            ]
            db.session.add_all(stations)
            print("Station seeded.")

        db.session.commit()
        print("Seed completed safely.")


if __name__ == "__main__":
    main()
