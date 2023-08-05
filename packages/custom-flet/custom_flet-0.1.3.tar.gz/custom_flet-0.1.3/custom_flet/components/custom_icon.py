import flet as ft
from typing import Union


class CustomIcon(ft.UserControl):
    def __init__(
            self,
            icon: str,
            size: int,
            color: Union[str, None] = None,
            ref: Union[ft.Ref, None] = None
    ):
        super().__init__()
        self.icon = icon
        self.size = size
        self.color = color
        self.ref = ref

    def build(self):
        return ft.Image(
            src=self.icon,
            width=self.size,
            height=self.size,
            color=self.color,
            ref=self.ref
        )
