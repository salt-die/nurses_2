from nurses_2.colors import ColorPair, Color
from nurses_2.widgets import Widget
from nurses_2.widgets.button_behavior import ButtonBehavior
from nurses_2.widgets.auto_position_behavior import AutoPositionBehavior

from .particles import Element

MENU_BACKGROUND_COLOR = Color(222, 224, 127)  # Mustard


class ElementDisplay(AutoPositionBehavior, Widget):
    """
    Display of currently selected element.
    """


class ElementButton(ButtonBehavior, Widget):
    """
    Button which selects an element when pressed and updates the element display.
    """
    def __init__(self, pos, element):
        self.element = element

        super().__init__(
            dim=(2, 4),
            pos=pos,
            default_color=ColorPair(0, 0, 0, *element.COLOR),
            always_release=True,
        )
        self.down_color = ColorPair(*((255 + c) // 2 for c in self.default_color))

    def update_down(self):
        self.colors[:, :] = self.down_color

    def update_normal(self):
        self.colors[:, :] = self.default_color

    def on_release(self):
        element = self.element
        sandbox = self.parent.parent

        sandbox.particle_type = element
        sandbox.display.add_text(f"{element.__name__:^{sandbox.display.width}}")


class ButtonContainer(Widget):
    """
    Container widget of `ElementButton`s.
    """
    def __init__(self):
        nelements = len(Element.all_elements)

        super().__init__(
            dim=(3 * nelements + 1, 8),
            default_color=ColorPair(0, 0, 0, *MENU_BACKGROUND_COLOR),
        )

        for i, element in enumerate(Element.all_elements.values()):
            self.add_widget(ElementButton(pos=(3 * i + 1, 2), element=element))

    def on_click(self, mouse_event):
        return self.collides_coords(mouse_event.position)
