from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # インスタンスフォルダ（ローカル用）
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Render の DATABASE_URL を優先
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        # ローカル SQLite
        database_url = f"sqlite:///{os.path.join(app.instance_path, 'app.db')}"

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,

        # 🔥 Render の無料 PostgreSQL で接続枯渇を防ぐ設定
        SQLALCHEMY_ENGINE_OPTIONS={
            "pool_pre_ping": True,
            "pool_size": 1,
            "max_overflow": 0,
        }
    )

    # DB 初期化
    db.init_app(app)
    migrate.init_app(app, db)

    # モデル読み込み
    from . import models

    # Blueprint 登録
    from .route import bp as main_bp
    app.register_blueprint(main_bp)

    # 🔥 Render 専用：起動時に自動 migrate + seed
    if os.environ.get("RENDER") == "true":
        with app.app_context():
            try:
                print("Running upgrade...")
                upgrade()
                print("Upgrade done.")

                print("Seeding initial data...")
                from scripts.seed import main as seed_main
                seed_main()
                print("Seed done.")

            except Exception as e:
                print(f"Migration failed: {e}")

    return app

app = create_app()
