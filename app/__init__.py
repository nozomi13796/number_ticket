from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # インスタンスフォルダ（instance/）を確実に作成（ローカル用）
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Render の DATABASE_URL を優先
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        # SQLite の場合は "sqlite:////tmp/app.db" のように指定される想定
        if database_url.startswith("/"):
            # 環境変数が "/tmp/app.db" の場合に対応
            database_url = f"sqlite:///{database_url}"
    else:
        # ローカル開発用 SQLite
        database_url = f"sqlite:///{os.path.join(app.instance_path, 'app.db')}"

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # DB初期化
    db.init_app(app)
    migrate.init_app(app, db)

    # モデル読み込み
    from . import models

    # ルート登録
    from .route import bp as main_bp
    app.register_blueprint(main_bp)

    return app
