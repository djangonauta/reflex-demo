import time

import reflex as rx

from ..template import template


class CachedVarState(rx.State):
    counter_a: int = 0
    counter_b: int = 0

    @rx.var
    def last_touch_time(self) -> str:
        # This is updated anytime the state is updated.
        _ = (
            self.counter_a + self.counter_b
        )  # não consta na documentação, as dependências precisam mudar
        return time.strftime("%H:%M:%S")

    @rx.event
    def increment_a(self):
        self.counter_a += 1

    @rx.var(cache=True)
    def last_counter_a_update(self) -> str:
        # só muda quando counter_a muda
        return f"{self.counter_a} at {time.strftime('%H:%M:%S')}"

    @rx.event
    def increment_b(self):
        self.counter_b += 1

    @rx.var(cache=True)
    def last_counter_b_update(self) -> str:
        # só muda quando counter_b muda
        return f"{self.counter_b} at {time.strftime('%H:%M:%S')}"


@rx.page("/cache")  # type: ignore
@template
def cached_var_example():
    return rx.vstack(
        rx.text(f"State touched at: {CachedVarState.last_touch_time}"),
        rx.text(f"Counter A: {CachedVarState.last_counter_a_update}"),
        rx.text(f"Counter B: {CachedVarState.last_counter_b_update}"),
        rx.hstack(
            rx.button(
                "Increment A",
                on_click=CachedVarState.increment_a,
            ),
            rx.button(
                "Increment B",
                on_click=CachedVarState.increment_b,
            ),
        ),
    )
