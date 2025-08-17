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
