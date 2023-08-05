import flet as ft
from typing import Union


class CustomIconButton(ft.UserControl):
    def __init__(
            self,
            icon,
            size: Union[None, int, float] = 24,
            color: Union[str, None] = None,
            ink_radius: Union[int, None] = 12,
            on_click=None,
            url: Union[str, None] = None,
            ref=None
    ):
        super().__init__()
        self.icon = icon
        self.size = size
        self.color = color
        self.ink_radius = ink_radius
        self.on_click = on_click
        self.url = url
        self.ref = ref

    def build(self):
        return ft.Container(
            content=ft.Image(self.icon, color=self.color, height=self.size, width=self.size, ),
            padding=self.ink_radius,
            ink=True,
            border_radius=35,
            on_click=self.on_click,
            url=self.url,
            ref=self.ref
        )
