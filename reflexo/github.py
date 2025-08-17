import httpx
import reflex as rx


class GithubState(rx.State):
    url: str = "https://github.com/reflex-dev"
    profile_image: str = "https://avatars.githubusercontent.com/u/104714959"

    @rx.event(background=True)
    async def set_profile(self, username: str):
        if username == "":
            return

        try:
            async with httpx.AsyncClient() as c:
                response = await c.get(f"https://api.github.com/users/{username}")
                github_data = response.json()

        except Exception:
            return

        async with self:
            self.url = github_data["url"]
            self.profile_image = github_data["avatar_url"]


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
