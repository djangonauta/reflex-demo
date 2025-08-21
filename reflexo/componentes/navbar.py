import reflex as rx


def navbar():
    return (
        rx.hstack(
            rx.link(
                rx.hstack(rx.icon("home", size=15), rx.text("Home"), align="center", gap=3),
                href="/",
            ),
            rx.link("Outra página", href="/github", title="Via react-router"),
            rx.link("Spline", href="/spline"),
            rx.link("Cache", href="/cache"),
            justify="end",
        ),
    )
