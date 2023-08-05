import flet as ft
from typing import Union
from custom_flet.components.custom_icon import CustomIcon


class ElevatedCustomLogoButton(ft.UserControl):
    def __init__(
            self,
            text: str,
            icon: str,
            size: Union[int, None] = 21,
            font_family: Union[str, None] = None,
            icon_color: Union[str, None] = "white",
            button_color: Union[str, None] = "green",
            text_color: Union[str, None] = "white",
            border_radius: Union[int, None] = 5,
            icon_at_end: Union[bool, None] = True,
            ref: Union[ft.Ref, None] = None
    ):
        super().__init__()
        self.text = text
        self.icon = icon
        self.size = size
        self.icon_color = icon_color
        self.button_color = button_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.font_family = font_family
        self.icon_at_end = icon_at_end
        self.ref = ref

    def build(self):
        button_content = ft.Row(
            [
                ft.Text(self.text, font_family=self.font_family, size=15),
            ],
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        if self.icon_at_end:
            button_content.controls.append(
                CustomIcon(
                    icon=self.icon,
                    size=self.size,
                    color=self.icon_color
                )
            )
        else:
            button_content.controls.insert(
                0,
                CustomIcon(
                    icon=self.icon,
                    size=self.size,
                    color=self.icon_color
                )
            )

        return ft.ElevatedButton(
            content=button_content,
            style=ft.ButtonStyle(
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=5),
                bgcolor=self.button_color,
                color=self.text_color,
            ),
            ref=self.ref
        )
