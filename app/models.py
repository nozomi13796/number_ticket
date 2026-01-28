from datetime import datetime, date, time, timedelta
from . import db

def jst_now():
    return datetime.utcnow() + timedelta(hours=9)

class Ticket(db.Model):
    __tablename__ = "tickets"

    t_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)  # 受付番号（prefix×連番はサービス層で生成）
    created_at = db.Column(db.DateTime, default=jst_now, nullable=False)
    dep_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Boolean, default=False)  # False=未呼出, True=呼出済

    # FK
    p_id = db.Column(db.Integer, db.ForeignKey("payments.p_id"), nullable=False)
    b_id = db.Column(db.Integer, db.ForeignKey("businesses.b_id"), nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey("stations.s_id"), nullable=False)

    # Relationship
    options = db.relationship("Option", backref="ticket", lazy=True)  # 1:N
    station = db.relationship("Station", backref="tickets")
    payment = db.relationship("Payment", backref="tickets")
    business = db.relationship("Business", backref="tickets")


class Option(db.Model):
    __tablename__ = "options"

    o_id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.Date, nullable=False)
    dep_st = db.Column(db.String(50), nullable=False)
    arr_st = db.Column(db.String(50), nullable=False)
    adults = db.Column(db.Integer, default=1)
    childs = db.Column(db.Integer, default=0)
    dep_or_arr = db.Column(db.Boolean, nullable=False)  # True=出発, False=到着
    preferred_time = db.Column(db.Time)
    preference = db.Column(db.String(200))

    # FK
    t_id = db.Column(db.Integer, db.ForeignKey("tickets.t_id"), nullable=False)


class Station(db.Model):
    __tablename__ = "stations"

    s_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    prefix = db.Column(db.Integer, nullable=False)  # A=1, B=2 のように管理
    last_number = db.Column(db.Integer, default=0)
    last_date = db.Column(db.Date, default=date.today)


class Payment(db.Model):
    __tablename__ = "payments"

    p_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Business(db.Model):
    __tablename__ = "businesses"

    b_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
