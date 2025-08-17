import reflex as rx

from .github_state import GithubState


@rx.page("/github", "Componente github teste")
def github():
    return rx.container(
        rx.hstack(
            rx.link(
                rx.avatar(src=GithubState.profile_image),
                href=GithubState.url,
            ),
            rx.input(
                placeholder="Your Github username",
                on_blur=GithubState.set_profile,
                auto_focus=True,
            ),
            rx.link("Página inicial", href="/", title="Via react-router"),
        )
    )
