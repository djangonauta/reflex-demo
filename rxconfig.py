import reflex as rx
from decouple import config

config = rx.Config(
    app_name="reflexo",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    db_url=config("DATABASE_URL"),  # type: ignore
    async_db_url=config("DATABASE_URL"),  # type: ignore
)
