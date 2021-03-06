"""
A slider widget.
"""
from collections.abc import Callable

from ...clamp import clamp
from ...colors import Color
from ...io import MouseEventType
from ..text_widget import TextWidget
from .handle import _Handle


class Slider(TextWidget):
    """
    A slider widget.

    Parameters
    ----------
    width : int
        Width of the slider.
    min : float
        Minimum value.
    max : float
        Maximum value.
    proportion : float, default: 0.0
        Starting proportion of slider.
    handle_color : Color | None, default: None
        Color of slider handle. If None, handle color is :attr:`default_fg_color`.
    fill_color: Color | None, default: None
        Color of "filled" portion of slider.
    slider_enabled : bool, default: True
        Allow dragging handle.
    callback : Callable | None, default: None
        Single argument callable called with new value of slider when slider is updated.
    default_char : str, default: " "
        Default background character. This should be a single unicode half-width grapheme.
    default_color_pair : ColorPair, default: WHITE_ON_BLACK
        Default color of widget.
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
    width : int
        Width of the slider.
    min : float
        Minimum value.
    max : float
        Maximum value.
    proportion : float
        Starting proportion of slider.
    handle_color : Color
        Color of slider handle.
    fill_color: Color
        Color of "filled" portion of slider.
    slider_enabled : bool
        Allow dragging handle.
    callback : Callable
        Single argument callable called with new value of slider when slider is updated.
    value : float
        Current value of slider.
    canvas : numpy.ndarray
        The array of characters for the widget.
    colors : numpy.ndarray
        The array of color pairs for each character in `canvas`.
    default_char : str, default: " "
        Default background character.
    default_color_pair : ColorPair, default: WHITE_ON_BLACK
        Default color pair of widget.
    default_fg_color: Color
        The default foreground color.
    default_bg_color: Color
        The default background color.
    get_view: CanvasView
        Return a :class:`nurses_2.widgets.text_widget_data_structures.CanvasView`
        of the underlying :attr:`canvas`.
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
    add_border:
        Add a border to the widget.
    normalize_canvas:
        Add zero-width characters after each full-width character.
    add_text:
        Add text to the canvas.
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
    """
    def __init__(
        self,
        *,
        width: int,
        min: float,
        max: float,
        proportion=0.0,
        handle_color: Color | None=None,
        fill_color: Color | None=None,
        slider_enabled=True,
        callback: Callable | None=None,
        default_char="???",
        **kwargs,
        ):
        super().__init__(size=(1, width), default_char=default_char, **kwargs)

        if min >= max:
            raise ValueError(f"{min=} >= {max=}")

        self.min = min
        self.max = max

        self.slider_enabled = slider_enabled
        self.callback = callback
        self._proportion = 0

        self.fill_color = fill_color or self.default_fg_color

        self.handle = _Handle(color=handle_color or self.default_fg_color)
        self.add_widget(self.handle)
        self.proportion = proportion

    @property
    def proportion(self):
        return self._proportion

    @proportion.setter
    def proportion(self, value):
        if self.slider_enabled:
            self._proportion = clamp(value, 0, 1)

            min, max = self.min, self.max
            self._value = (max - min) * self._proportion + min
            if self.callback is not None:
                self.callback(self._value)

            self.handle.update_geometry()
            handle_x = self.handle.x
            self.colors[:, :handle_x, :3] = self.fill_color
            self.colors[:, handle_x:, :3] = self.default_fg_color

    @property
    def value(self):
        return self._value

    @property
    def fill_width(self):
        """
        Width of the slider minus the width of the handle.
        """
        return self.width - self.handle.width

    def on_click(self, mouse_event):
        if (
            mouse_event.event_type == MouseEventType.MOUSE_DOWN
            and self.collides_point(mouse_event.position)
        ):
            x = self.to_local(mouse_event.position).x

            self.proportion = x / self.fill_width
            self.handle.grab(mouse_event)

            return True
