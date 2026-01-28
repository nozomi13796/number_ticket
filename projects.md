number_ticket/
│
├── app/
│   ├── __init__.py          # Flaskアプリ初期化
│   ├── config.py            # 設定（DBパス、SECRET_KEYなど）
│   ├── models.py            # SQLAlchemyモデル（Ticket/Option/Station…）
│   ├── route.py
│   ├── services/
│   │   ├── numbering.py     # prefix×連番ロジック
│   │   ├── qr.py            # QR生成（HMAC署名含む）
│   ├── templates/
│   │   ├── base.html        # 共通レイアウト（Tailwind CDN読み込み）
│   │   ├── index.html       # テスト用係員⇔旅客分岐
│   │   ├── ticket.html      # 発券画面（外部ディスプレイ）
│   │   ├── qr.html          # QR表示画面
│   │   ├── option.html      # 旅客スマホ入力画面
│   │   ├── list.html        # 係員一覧画面
│   │   └── detail.html      # 係員詳細画面
│   ├── static/
│   │   └── img/             # 必要ならQR画像など
│   └── instance/
│       └── app.db           # SQLiteファイル
│
├── scripts/
│   ├── init_db.py           # DB初期化スクリプト
│   └── seed_data.py         # マスタ投入（Station/Payment/Business）
│
├── tests/
│   ├── test_numbering.py    # 連番ロジックのテスト
│   ├── test_ticket_api.py
│   └── test_option_api.py
│
└── requirements.txt         # Flask, SQLAlchemy, qrcode など
