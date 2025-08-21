import reflex as rx

from ..template import template
from .github_state import GithubState


@rx.page("/github", "Componente github teste")  # type: ignore
@template
def github():
    return rx.hstack(
        rx.link(
            rx.avatar(src=GithubState.profile_image),
            href=GithubState.url,
        ),
        rx.input(
            placeholder="Your Github username",
            on_blur=GithubState.set_profile,
            auto_focus=True,
        ),
    )
