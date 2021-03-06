"""
Base for particle fields.
"""
from typing import Literal

from ...data_structures import *
from ...io import MouseEvent, KeyPressEvent, PasteEvent
from ..widget import Widget


class _ParticleFieldBase(Widget):
    """
    A widget that specializes in rendering 1x1 particles.
    """
    def add_widget(self, widget):
        if not isinstance(widget, self._child_type):
            raise TypeError(
                f"expected {self._child_type.__name__}, got {type(widget).__name__}"
            )

        super().add_widget(widget)

    def add_particle(self, particle):
        """
        Alias for :meth:`add_widget`.
        """
        self.add_widget(particle)

    def walk(self):
        """
        Yield all descendents.
        """
        yield from self.children

    def dispatch_press(self, key_press_event: KeyPressEvent) -> bool | None:
        """
        Dispatch key press to children.

        Notes
        -----
        Particle fields, unlike usual widgets, will try to handle events before passing them
        to their children.
        """
        return (
            self.on_press(key_press_event)
            or any(
                particle.on_press(key_press_event)
                for particle in reversed(self.children)
                if particle.is_enabled
            )
        )

    def dispatch_click(self, mouse_event: MouseEvent) -> bool | None:
        """
        Dispatch mouse event to children.

        Notes
        -----
        Particle fields, unlike usual widgets, will try to handle events before passing them
        to their children.
        """
        return (
            self.on_click(mouse_event)
            or any(
                particle.on_click(mouse_event)
                for particle in reversed(self.children)
                if particle.is_enabled
            )
        )

    def dispatch_double_click(self, mouse_event: MouseEvent) -> bool | None:
        """
        Dispatch double-click mouse event to children.

        Notes
        -----
        Particle fields, unlike usual widgets, will try to handle events before passing them
        to their children.
        """
        return (
            self.on_double_click(mouse_event)
            or any(
                particle.on_double_click(mouse_event)
                for particle in reversed(self.children)
                if particle.is_enabled
            )
        )

    def dispatch_triple_click(self, mouse_event: MouseEvent) -> bool | None:
        """
        Dispatch triple-click mouse event to children.

        Notes
        -----
        Particle fields, unlike usual widgets, will try to handle events before passing them
        to their children.
        """
        return (
            self.on_triple_click(mouse_event)
            or any(
                particle.on_triple_click(mouse_event)
                for particle in reversed(self.children)
                if particle.is_enabled
            )
        )

    def dispatch_paste(self, paste_event: PasteEvent) -> bool | None:
        """
        Dispatch paste event to children.

        Notes
        -----
        Particle fields, unlike usual widgets, will try to handle events before passing them
        to their children.
        """
        return (
            self.on_paste(mouse_event)
            or any(
                particle.on_paste(mouse_event)
                for particle in reversed(self.children)
                if particle.is_enabled
            )
        )

    def render(self, canvas_view, colors_view, source: tuple[slice, slice]):
        raise NotImplementedError("Render method not implemented in base class.")


class _ParticleBase:
    """
    Base for 1x1 text or graphic elements.

    Notes
    -----
    Particles are widget-like, but they have no `render` method (they are rendered
    by their parents) and their size is always (1, 1).
    """
    def __init__(
        self,
        *,
        pos=Point(0, 0),
        is_transparent=False,
        is_visible=True,
        is_enabled=True,
    ):
        self.parent = None
        self.pos = pos
        self.is_transparent = is_transparent
        self.is_visible = is_visible
        self.is_enabled = is_enabled

    def update_geometry(self):
        """
        Update geometry due to a change in parent's size.
        """

    @property
    def size(self) -> Size:
        return Size(1, 1)

    @property
    def pos(self) -> Point:
        return self._pos

    @pos.setter
    def pos(self, pos: Point):
        self._pos = Point(*pos)

    @property
    def top(self) -> int:
        return self._pos[0]

    @top.setter
    def top(self, top: int):
        self.pos = top, self.left

    @property
    def left(self) -> int:
        return self._pos[1]

    @left.setter
    def left(self, left: int):
        self.pos = self.top, left

    @property
    def height(self) -> Literal[1]:
        return 1

    @property
    def width(self) -> Literal[1]:
        return 1

    @property
    def bottom(self) -> int:
        return self.top + 1

    @property
    def right(self) -> int:
        return self.left + 1

    def to_local(self, coords) -> Point:
        """
        Convert absolute coordinates to relative coordinates.
        """
        y, x = self.parent.to_local(coords)
        return Point(y - self.top, x - self.left)

    def on_press(self, key_press_event: KeyPressEvent) -> bool | None:
        """
        Handle key press event. (Handled key presses should return True else False or None).
        """

    def on_click(self, mouse_event: MouseEvent) -> bool | None:
        """
        Handle mouse event. (Handled mouse events should return True else False or None).
        """

    def on_double_click(self, mouse_event: MouseEvent) -> bool | None:
        """
        Handle double-click mouse event. (Handled mouse events should return True else False or None).
        """

    def on_triple_click(self, mouse_event: MouseEvent) -> bool | None:
        """
        Handle triple-click mouse event. (Handled mouse events should return True else False or None).
        """

    def on_paste(self, paste_event: PasteEvent) -> bool | None:
        """
        Handle paste event. (Handled paste events should return True else False or None).
        """


_ParticleFieldBase._child_type = _ParticleBase
