"""
A movable, resizable window widget.
"""
from wcwidth import wcswidth

from ..clamp import clamp
from ..colors import ColorPair, AColor
from .behaviors.focus_behavior import FocusBehavior
from .behaviors.grabbable_behavior import GrabbableBehavior
from .behaviors.grab_resize_behavior import GrabResizeBehavior
from .behaviors.themable import Themable
from .graphic_widget import GraphicWidget
from .text_widget import TextWidget
from .widget import Widget, Size, Anchor

__all__ = "Window",


class _TitleBar(GrabbableBehavior, TextWidget):
    def __init__(self, **kwargs):
        super().__init__(disable_ptf=True, **kwargs)

        self._label = TextWidget(pos_hint=(None, .5), anchor=Anchor.TOP_CENTER)
        self.add_widget(self._label)

    def grab_update(self, mouse_event):
        self.parent.top += self.mouse_dy
        self.parent.left += self.mouse_dx

    def update_geometry(self):
        bh, bw = self.parent.border_size
        self.size = bh, self.parent.width - 2 * bw


class _View(GraphicWidget):
    def update_geometry(self):
        h, w = self.parent.size
        bh, bw = self.parent.border_size
        self.size = h - 1 - 2 * bh, w - 2 * bw
        self.is_visible = h > bh * 3 and w > bw * 2


class Window(Themable, FocusBehavior, GrabResizeBehavior, Widget):
    """
    A movable, resizable window widget.

    Parameters
    ----------
    title : str, default: ""
        Title of window.
    alpha : float, default: 1.0
        Transparency of window background and border.
    size : Size, default: Size(10, 10)
        Size of widget.
    pos : Point, default: Point(0, 0)
        Position of upper-left corner in parent.
    size_hint : SizeHint, default: SizeHint(None, None)
        Proportion of parent's height and width. Non-None values will have
        precedent over :attr:`size`.
    min_height : int | None, default: None
        Minimum height set due to size_hint. Ignored if corresponding size
        hint is None.
    max_height : int | None, default: None
        Maximum height set due to size_hint. Ignored if corresponding size
        hint is None.
    min_width : int | None, default: None
        Minimum width set due to size_hint. Ignored if corresponding size
        hint is None.
    max_width : int | None, default: None
        Maximum width set due to size_hint. Ignored if corresponding size
        hint is None.
    pos_hint : PosHint, default: PosHint(None, None)
        Position as a proportion of parent's height and width. Non-None values
        will have precedent over :attr:`pos`.
    anchor : Anchor, default: Anchor.TOP_LEFT
        The point of the widget attached to :attr:`pos_hint`.
    is_transparent : bool, default: False
        If true, background_char and background_color_pair won't be painted.
    is_visible : bool, default: True
        If false, widget won't be painted, but still dispatched.
    is_enabled : bool, default: True
        If false, widget won't be painted or dispatched.
    background_char : str | None, default: None
        The background character of the widget if not `None` and if the widget
        is not transparent.
    background_color_pair : ColorPair | None, default: None
        The background color pair of the widget if not `None` and if the
        widget is not transparent.

    Attributes
    ----------
    size : Size
        Size of widget.
    height : int
        Height of widget.
    rows : int
        Alias for :attr:`height`.
    width : int
        Width of widget.
    columns : int
        Alias for :attr:`width`.
    pos : Point
        Position relative to parent.
    top : int
        Y-coordinate of position.
    y : int
        Y-coordinate of position.
    left : int
        X-coordinate of position.
    x : int
        X-coordinate of position.
    bottom : int
        :attr:`top` + :attr:`height`.
    right : int
        :attr:`left` + :attr:`width`.
    absolute_pos : Point
        Absolute position on screen.
    center : Point
        Center of widget in local coordinates.
    size_hint : SizeHint
        Size as a proportion of parent's size.
    height_hint : float | None
        Height as a proportion of parent's height.
    width_hint : float | None
        Width as a proportion of parent's width.
    min_height : int
        Minimum height allowed when using :attr:`size_hint`.
    max_height : int
        Maximum height allowed when using :attr:`size_hint`.
    min_width : int
        Minimum width allowed when using :attr:`size_hint`.
    max_width : int
        Maximum width allowed when using :attr:`size_hint`.
    pos_hint : PosHint
        Position as a proportion of parent's size.
    y_hint : float | None
        Vertical position as a proportion of parent's size.
    x_hint : float | None
        Horizontal position as a proportion of parent's size.
    anchor : Anchor
        Determines which point is attached to :attr:`pos_hint`.
    background_char : str | None
        Background character.
    background_color_pair : ColorPair | None
        Background color pair.
    parent : Widget | None
        Parent widget.
    children : list[Widget]
        Children widgets.
    is_transparent : bool
        True if widget is transparent.
    is_visible : bool
        True if widget is visible.
    is_enabled : bool
        True if widget is enabled.
    root : Widget | None
        If widget is in widget tree, return the root widget.
    app : App
        The running app.

    Methods
    -------
    on_size:
        Called when widget is resized.
    update_geometry:
        Called when parent is resized. Applies size and pos hints.
    to_local:
        Convert point in absolute coordinates to local coordinates.
    collides_point:
        True if point is within widget's bounding box.
    collides_widget:
        True if other is within widget's bounding box.
    add_widget:
        Add a child widget.
    add_widgets:
        Add multiple child widgets.
    remove_widget:
        Remove a child widget.
    pull_to_front:
        Move to end of widget stack so widget is drawn last.
    walk_from_root:
        Yield all descendents of root widget.
    walk:
        Yield all descendents.
    subscribe:
        Subscribe to a widget property.
    unsubscribe:
        Unsubscribe to a widget property.
    on_press:
        Handle key press event.
    on_click:
        Handle mouse event.
    on_double_click:
        Handle double-click mouse event.
    on_triple_click:
        Handle triple-click mouse event.
    on_paste:
        Handle paste event.
    tween:
        Sequentially update a widget property over time.

    Notes
    -----
    If not given or too small, :attr:`min_height` and :attr:`min_width` will be
    set large enough so that the border is visible and the titlebar's
    label is visible.
    """
    def __init__(self, title="", alpha=1.0, **kwargs):
        self._view = None

        super().__init__(**kwargs)

        if self.min_height is None:
            self.min_height = 1

        if self.min_width is None:
            self.min_width = 1

        self.add_widgets(_View(), _TitleBar())
        self.pull_border_to_front()
        self._view = self.children[0]
        self._titlebar = self.children[1]

        self.alpha = alpha
        self.title = title

        self.update_theme()

        self.border_size = self.border_size  # Reposition titlebar and view

    @property
    def border_size(self) -> Size:
        return self._border_size

    @border_size.setter
    def border_size(self, size: Size):
        h, w = size
        self._border_size = Size(clamp(h, 1, None), clamp(w, 1, None))

        for border in self._borders:
            border.update_geometry()

        if self._view is None:  # Still being initialized.
            return

        self._titlebar.pos = h, w
        self._view.pos = h * 2, w

        self.min_height = max(h * 3, self.min_height)
        self.min_width = max(wcswidth(self._title) + self.border_size.width * 2 + 2, self.min_width)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title
        self._titlebar._label.size = 1, wcswidth(title)
        self._titlebar._label.add_text(title)
        self.min_width = max(wcswidth(title) + self.border_size.width * 2 + 2, self.min_width)

    @property
    def alpha(self) -> float:
        return self._alpha

    @alpha.setter
    def alpha(self, alpha: float):
        self._alpha = clamp(alpha, 0.0, 1.0)
        self.border_alpha = self._view.alpha = self._alpha

    def update_theme(self):
        ct = self.color_theme

        view_background = AColor(*ct.primary_bg_light, 255)
        self._view.default_color = view_background
        self._view.texture[:] = view_background

        if self.is_focused:
            self.border_color = AColor(*ct.secondary_bg, 255)
        else:
            self.border_color = AColor(*ct.primary_bg, 255)

        title_bar_color_pair = ColorPair.from_colors(ct.secondary_bg, ct.primary_bg_dark)
        self._titlebar.default_color_pair = title_bar_color_pair
        self._titlebar.colors[:] = title_bar_color_pair
        self._titlebar._label.default_color_pair = title_bar_color_pair
        self._titlebar._label.colors[:] = title_bar_color_pair

    def on_focus(self):
        self.update_theme()

    def on_blur(self):
        self.update_theme()

    def add_widget(self, widget):
        if self._view is None:  # Still being initialized.
            super().add_widget(widget)
        else:
            self._view.add_widget(widget)

    def remove_widget(self, widget):
        if self._view is None:  # Still being initialized.
            super().remove_widget(widget)
        else:
            self._view.remove_widget(widget)

    def dispatch_click(self, mouse_event):
        return super().dispatch_click(mouse_event) or self.collides_point(mouse_event.position)

    def dispatch_double_click(self, mouse_event):
        return super().dispatch_double_click(mouse_event) or self.collides_point(mouse_event.position)

    def dispatch_triple_click(self, mouse_event):
        return super().dispatch_triple_click(mouse_event) or self.collides_point(mouse_event.position)
