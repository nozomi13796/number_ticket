from datetime import date
from app.models import Station
from app import db


def generate_ticket_number(station_id: int) -> int:
    """指定された station の prefix と連番から Ticket.number を生成する"""

    station = Station.query.get(station_id)
    if not station:
        raise ValueError("Station not found")

    # 日付が変わっていたら連番リセット
    today = date.today()
    if station.last_date != today:
        station.last_number = 0
        station.last_date = today

    # 連番を +1
    station.last_number += 1

    # prefix × 1000 + 連番 でユニーク番号を生成
    number = station.prefix * 1000 + station.last_number

    # DB に反映
    db.session.commit()

    return number
