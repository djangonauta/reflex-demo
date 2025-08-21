from typing import Callable

import reflex as rx

from .componentes.navbar import navbar


def template(page: Callable[[], rx.Component]) -> rx.Component:
    return rx.vstack(
        rx.container(navbar(), page(), width="100%"),
    )
