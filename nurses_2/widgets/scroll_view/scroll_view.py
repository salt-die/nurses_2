"""
A scrollable view widget.
"""
from ...clamp import clamp
from ...io import KeyPressEvent, MouseEventType, MouseEvent
from ..behaviors.grabbable_behavior import GrabbableBehavior
from ..widget import Widget
from .scrollbars import _HorizontalBar, _VerticalBar


class ScrollView(GrabbableBehavior, Widget):
    """
    A scrollable view widget. A scroll view accepts only one child and
    places it in a scrollable viewport.

    Parameters
    ----------
    allow_vertical_scroll : bool, default: True
        Allow vertical scrolling.
    allow_horizontal_scroll : bool, default: True
        Allow horizontal scrolling.
    show_vertical_bar : bool, default: True
        Show the vertical scrollbar.
    show_horizontal_bar : bool, default: True
        Show the horizontal scrollbar.
    is_grabbable : bool, default: True
        Allow moving scroll view by dragging mouse.
    scrollwheel_enabled : bool, default: True
        Allow vertical scrolling with scrollwheel.
    arrow_keys_enabled : bool, default: True
        Allow scrolling with arrow keys.
    vertical_proportion : float, default: 0.0
        Vertical scroll position as a proportion of total.
    horizontal_proportion : float, default: 0.0
        Horizontal scroll position as a proportion of total.
    is_grabbable : bool, default: True
        If False, grabbable behavior is disabled.
    disable_ptf : bool, default: False
        If True, widget will not be pulled to front when grabbed.
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
    allow_vertical_scroll : bool
        Allow vertical scrolling.
    allow_horizontal_scroll : bool
        Allow horizontal scrolling.
    show_vertical_bar : bool
        Show the vertical scrollbar.
    show_horizontal_bar : bool
        Show the horizontal scrollbar.
    is_grabbable : bool
        Allow moving scroll view by dragging mouse.
    scrollwheel_enabled : bool
        Allow vertical scrolling with scrollwheel.
    arrow_keys_enabled : bool
        Allow scrolling with arrow keys.
    vertical_proportion : float
        Vertical scroll position as a proportion of total.
    horizontal_proportion : float
        Horizontal scroll position as a proportion of total.
    view : Widget | None
        The scroll view's child.
    is_grabbable : bool
        If False, grabbable behavior is disabled.
    disable_ptf : bool
        If True, widget will not be pulled to front when grabbed.
    is_grabbed : bool
        True if widget is grabbed.
    mouse_dyx : Point
        Last change in mouse position.
    mouse_dy : int
        Last vertical change in mouse position.
    mouse_dx : int
        Last horizontal change in mouse position.
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
    grab:
        Grab the widget.
    ungrab:
        Ungrab the widget.
    grab_update:
        Update widget with incoming mouse events while grabbed.
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

    Raises
    ------
    ValueError
        If `add_widget` is called while already containing a child.
    """
    def __init__(
        self,
        allow_vertical_scroll=True,
        allow_horizontal_scroll=True,
        show_vertical_bar=True,
        show_horizontal_bar=True,
        is_grabbable=True,
        scrollwheel_enabled=True,
        arrow_keys_enabled=True,
        vertical_proportion=0.0,
        horizontal_proportion=0.0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.allow_vertical_scroll = allow_vertical_scroll
        self.allow_horizontal_scroll = allow_horizontal_scroll
        self.show_vertical_bar = show_vertical_bar
        self.show_horizontal_bar = show_horizontal_bar
        self.is_grabbable = is_grabbable
        self.scrollwheel_enabled = scrollwheel_enabled
        self.arrow_keys_enabled = arrow_keys_enabled
        self._vertical_proportion = clamp(vertical_proportion, 0, 1)
        self._horizontal_proportion = clamp(horizontal_proportion, 0, 1)
        self._view = None

        self.children = [
            _VerticalBar(self),
            _HorizontalBar(self),
        ]

    @property
    def view(self) -> Widget | None:
        return self._view

    @property
    def vertical_proportion(self):
        return self._vertical_proportion

    @vertical_proportion.setter
    def vertical_proportion(self, value):
        if self.allow_vertical_scroll:
            if self._view is None or self._view.height <= self.height:
                self._vertical_proportion = 0
            else:
                self._vertical_proportion = clamp(value, 0, 1)
                self._set_view_top()

            vertical_bar = self.children[0]
            vertical_bar.indicator.update_geometry()

    @property
    def horizontal_proportion(self):
        return self._horizontal_proportion

    @horizontal_proportion.setter
    def horizontal_proportion(self, value):
        if self.allow_horizontal_scroll:
            if self._view is None or self._view.width <= self.width:
                self._horizontal_proportion = 0
            else:
                self._horizontal_proportion = clamp(value, 0, 1)
                self._set_view_left()

            horizontal_bar = self.children[1]
            horizontal_bar.indicator.update_geometry()

    @property
    def total_vertical_distance(self) -> int:
        """
        Return difference between child height and scrollview height.
        """
        if self._view is None:
            return 0

        return self._view.height - self.height + self.show_horizontal_bar

    @property
    def total_horizontal_distance(self) -> int:
        """
        Return difference between child width and scrollview width.
        """
        if self._view is None:
            return 0

        return self._view.width - self.width + self.show_vertical_bar * 2

    def _set_view_top(self):
        """
        Set the top-coordinate of the view.
        """
        if self.total_vertical_distance <= 0:
            self._view.top = 0
        else:
            self._view.top = -round(self.vertical_proportion * self.total_vertical_distance)

    def _set_view_left(self):
        """
        Set the left-coordinate of the view.
        """
        if self.total_horizontal_distance <= 0:
            self._view.left = 0
        else:
            self._view.left = -round(self.horizontal_proportion * self.total_horizontal_distance)

    def _set_view_pos(self):
        """
        Set position of the view.
        """
        self._set_view_top()
        self._set_view_left()

    def add_widget(self, widget):
        if self._view is not None:
            raise ValueError("ScrollView already has child.")

        self._view = widget
        widget.parent = self

        self._set_view_pos()

        self.subscribe(widget, "size", self._set_view_pos)

    def remove_widget(self, widget):
        if widget is not self._view:
            raise ValueError(f"{widget} not in ScrollView")

        self.unsubscribe(widget, "size")

        self._view = None
        widget.parent = None

    def on_size(self):
        if self._view is not None:
            self._set_view_pos()

    def render(self, canvas_view, colors_view, source: tuple[slice, slice]):
        """
        Paint region given by source into canvas_view and colors_view.
        """
        if not self.is_transparent:
            if self.background_char is not None:
                canvas_view[:] = self.background_char

            if self.background_color_pair is not None:
                colors_view[:] = self.background_color_pair

        view = self._view
        if view is not None and view.is_enabled:
            view.render_intersection(source, canvas_view, colors_view)

        vertical_bar, horizontal_bar = self.children
        if self.show_vertical_bar:
            vertical_bar.render_intersection(source, canvas_view, colors_view)

        if self.show_horizontal_bar:
            horizontal_bar.render_intersection(source, canvas_view, colors_view)

    def on_press(self, key_press_event: KeyPressEvent):
        if not self.arrow_keys_enabled:
            return False

        match key_press_event.key:
            case "up":
                self._scroll_up()
            case "down":
                self._scroll_down()
            case "left":
                self._scroll_left()
            case "right":
                self._scroll_right()
            case _:
                return super().on_press(key_press_event)

        return True

    def grab_update(self, mouse_event: MouseEvent):
        self._scroll_up(self.mouse_dy)
        self._scroll_left(self.mouse_dx)

    def _scroll_left(self, n=1):
        if self._view is not None:
            if self.total_horizontal_distance > 0:
                self.horizontal_proportion = clamp((-self.view.left - n) / self.total_horizontal_distance, 0, 1)
            else:
                self.horizontal_proportion = 0

    def _scroll_right(self, n=1):
        self._scroll_left(-n)

    def _scroll_up(self, n=1):
        if self._view is not None:
            if self.total_vertical_distance > 0:
                self.vertical_proportion = clamp((-self.view.top - n) / self.total_vertical_distance, 0, 1)
            else:
                self.vertical_proportion = 0

    def _scroll_down(self, n=1):
        self._scroll_up(-n)

    def dispatch_press(self, key_press_event: KeyPressEvent):
        if (
            self._view is not None
            and self._view.is_enabled
            and self._view.dispatch_press(key_press_event)
        ):
            return True

        return self.on_press(key_press_event)

    def dispatch_click(self, mouse_event: MouseEvent):
        v_bar, h_bar = self.children

        if self.show_horizontal_bar and h_bar.dispatch_click(mouse_event):
            return True

        if self.show_vertical_bar and v_bar.dispatch_click(mouse_event):
            return True

        if (
            self._view is not None
            and self._view.is_enabled
            and self._view.dispatch_click(mouse_event)
        ):
            return True

        return self.on_click(mouse_event)

    def dispatch_double_click(self, mouse_event: MouseEvent):
        v_bar, h_bar = self.children

        if self.show_horizontal_bar and h_bar.dispatch_double_click(mouse_event):
            return True

        if self.show_vertical_bar and v_bar.dispatch_double_click(mouse_event):
            return True

        if (
            self._view is not None
            and self._view.is_enabled
            and self._view.dispatch_double_click(mouse_event)
        ):
            return True

        return self.on_double_click(mouse_event)

    def dispatch_triple_click(self, mouse_event: MouseEvent):
        v_bar, h_bar = self.children

        if self.show_horizontal_bar and h_bar.dispatch_triple_click(mouse_event):
            return True

        if self.show_vertical_bar and v_bar.dispatch_triple_click(mouse_event):
            return True

        if (
            self._view is not None
            and self._view.is_enabled
            and self._view.dispatch_triple_click(mouse_event)
        ):
            return True

        return self.on_triple_click(mouse_event)

    def on_click(self, mouse_event: MouseEvent):
        if (
            self.scrollwheel_enabled
            and self.collides_point(mouse_event.position)
        ):
            match mouse_event.event_type:
                case MouseEventType.SCROLL_UP:
                    self._scroll_up()
                    return True
                case MouseEventType.SCROLL_DOWN:
                    self._scroll_down()
                    return True

        return super().on_click(mouse_event)
