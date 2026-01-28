from datetime import date, datetime
from flask import Blueprint, render_template, url_for, redirect, request
from services.qr import generate_qr_base64
from .models import Option, Ticket, Payment, Business
from app import db
from services.numbering import generate_ticket_number

bp = Blueprint("main", __name__)

# ルートページ(test用)
@bp.route("/")
def index():
    return render_template("index.html")

# 整理券発券ページ
@bp.route("/ticket", methods=["GET", "POST"])
def ticket():
    if request.method == "POST":
        dep_date_str = request.form.get("dep_date")
        dep_date = datetime.strptime(dep_date_str, "%Y-%m-%d").date()
        p_id = request.form.get("p_id")
        b_id = request.form.get("b_id")

        station_id = 2  # 仮に station_id=2 として発券

        number = generate_ticket_number(station_id)

        ticket = Ticket(
            dep_date=dep_date,
            p_id=p_id,
            b_id=b_id,
            number = number,
            s_id = station_id
        )
        db.session.add(ticket)
        db.session.commit()

        return redirect(url_for("main.qr", t_id=ticket.t_id))

    payments = Payment.query.all()
    businesses = Business.query.all()

    return render_template("ticket.html", payments=payments, businesses=businesses)

# QRコード表示ページ
@bp.route("/ticket/<int:t_id>/qr")
def qr(t_id):
    ticket = Ticket.query.get_or_404(t_id)

    # QR に埋め込む内容（MVP では t_id だけでOK）
    qr_data = f"https://example.com/ticket/{t_id}/option"

    qr_base64 = generate_qr_base64(qr_data)

    return render_template("qr.html", ticket=ticket, qr_base64=qr_base64, t_id=t_id)

# オプション選択ページ
@bp.route("/ticket/<int:t_id>/option", methods=["GET", "POST"])
def option(t_id):
    ticket = Ticket.query.get_or_404(t_id)

    if request.method == "POST":
        date_str = request.form.get("date")
        time_str = request.form.get("preferred_time")

        option = Option(
            t_id=t_id,
            date=datetime.strptime(date_str, "%Y-%m-%d").date(),
            dep_st=request.form.get("dep_st"),
            arr_st=request.form.get("arr_st"),
            adults=int(request.form.get("adults")),
            childs=int(request.form.get("childs")),
            dep_or_arr=(request.form.get("dep_or_arr") == "1"),
            preferred_time=datetime.strptime(time_str, "%H:%M").time() if time_str else None,
            preference=request.form.get("preference")
        )

        db.session.add(option)
        db.session.commit()
        # 続きの行程を入力するためにリダイレクト
        return redirect(url_for("main.option", t_id=t_id))

    # 入力済み行程一覧
    options = Option.query.filter_by(t_id=t_id).all()

    return render_template("option.html", ticket=ticket, options=options)

# 係員用一覧
@bp.route("/list")
def list_tickets():
    today = date.today()
    station_id = 2  # 固定（将来はセッション化）

    tickets = (
        Ticket.query
        .filter_by(dep_date=today, s_id=station_id)
        .order_by(Ticket.status.asc()).order_by(Ticket.number.asc())
        .all()
    )

    return render_template("list.html", tickets=tickets, today=today)

# 詳細表示ページ
@bp.route("/detail/<int:t_id>", methods=["GET", "POST"])
def detail(t_id):
    ticket = Ticket.query.get_or_404(t_id)
    options = ticket.options  # 1:N

    if request.method == "POST":
        ticket.status = True
        db.session.commit()
        return redirect(url_for("main.list_tickets"))

    return render_template("detail.html", ticket=ticket, options=options)
