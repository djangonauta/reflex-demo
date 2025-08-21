import reflex as rx

from ..componentes.spline import spline
from ..template import template


@rx.page("/spline")  # type: ignore
@template
def spline_page():
    return rx.vstack(
        spline(scene="https://prod.spline.design/joLpOOYbGL-10EJ4/scene.splinecode"),
        spline(scene="https://prod.spline.design/6Wq1Q7YGyM-iab9i/scene.splinecode"),
    )
