# nurses_2 - Terminal Graphics

A widgetful and async-centric library for creating graphical applications in the terminal.

Create games:

![Tetris](https://raw.githubusercontent.com/salt-die/nurses_2/main/preview_images/tetris.png)

Simulations:

![Cloth](https://raw.githubusercontent.com/salt-die/nurses_2/main/preview_images/cloth.png)

Or entire feature-filled applications:

![Windows](https://raw.githubusercontent.com/salt-die/nurses_2/main/preview_images/windows.png)

See it in action: [Video Preview](https://youtu.be/LLI6ANQ6MH4).

[Read the docs](https://salt-die.github.io/nurses_2/index.html) (*work in progress*)

Getting Started: A Pong Tutorial
--------------------------------

Create a new file, `pong.py`. Let's just get our app running first:
```py
from nurses_2.app import App


class Pong(App):
    async def on_start():
        pass


if __name__ == "__main__":
    Pong().run()
```

This should show just a blank terminal.  To exit, press `escape`. We can create a green play field
by adding a new widget with a background color pair with green background. (`ColorPair`s include a foreground color and a background color. In this case, the foreground color is not used.)

```py
from nurses_2.app import App
from nurses_2.colors import GREEN, WHITE, ColorPair
from nurses_2.widgets.widget import Widget

FIELD_HEIGHT = 25
FIELD_WIDTH = 100
WHITE_ON_GREEN = ColorPair.from_colors(WHITE, GREEN)


class Pong(App):
    async def on_start(self):
        game_field = Widget(
            size=(FIELD_HEIGHT, FIELD_WIDTH),
            background_color_pair=WHITE_ON_GREEN,
        )

        self.add_widget(game_field)


if __name__ == "__main__":
    Pong().run()
```

Next, let's add paddles for each player. We can respond to key presses by implementing a widget's `on_press` method. Player 1's paddle can be moved up and down with `w` and `s` and Player 2's paddle can be moved up and down with `up` and `down`:

```py
from nurses_2.app import App
from nurses_2.colors import GREEN, BLUE, WHITE, ColorPair
from nurses_2.widgets.widget import Widget

FIELD_HEIGHT = 25
FIELD_WIDTH = 100
WHITE_ON_GREEN = ColorPair.from_colors(WHITE, GREEN)

PADDLE_HEIGHT = 5
PADDLE_WIDTH = 1
WHITE_ON_BLUE = ColorPair.from_colors(WHITE, BLUE)


class Paddle(Widget):
    def __init__(self, player, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = player

    def on_press(self, key_press_event):
        if self.player == 1:
            if key_press_event.key == "w":
                self.y -= 1
            elif key_press_event.key == "s":
                self.y += 1
        elif self.player == 2:
            if key_press_event.key == "up":
                self.y -= 1
            elif key_press_event.key == "down":
                self.y += 1

        if self.y < 0:
            self.y = 0
        elif self.y > FIELD_HEIGHT - PADDLE_HEIGHT:
            self.y = FIELD_HEIGHT - PADDLE_HEIGHT


class Pong(App):
    async def on_start(self):
        game_field = Widget(
            size=(FIELD_HEIGHT, FIELD_WIDTH),
            background_color_pair=WHITE_ON_GREEN,
        )

        vertical_center = FIELD_HEIGHT // 2 - PADDLE_HEIGHT // 2

        left_paddle = Paddle(
            player=1,
            size=(PADDLE_HEIGHT, PADDLE_WIDTH),
            pos=(vertical_center, 1),
            background_color_pair=WHITE_ON_BLUE,
        )

        right_paddle = Paddle(
            player=2,
            size=(PADDLE_HEIGHT, PADDLE_WIDTH),
            pos=(vertical_center, FIELD_WIDTH - 2),
            background_color_pair=WHITE_ON_BLUE,
        )

        game_field.add_widgets(left_paddle, right_paddle)
        self.add_widget(game_field)


if __name__ == "__main__":
    Pong().run()
```

With size hints and position hints we can easily place a divider in the game field:

```py
...
        right_paddle = Paddle(
            player=2,
            size=(PADDLE_HEIGHT, PADDLE_WIDTH),
            pos=(vertical_center, FIELD_WIDTH - 2),
            background_color_pair=WHITE_ON_BLUE,
        )

        divider = Widget(
            size=(1, 1),
            size_hint=(1.0, None),
            pos_hint=(None, .5),
            background_color_pair=WHITE_ON_BLUE,
        )

        game_field.add_widgets(left_paddle, right_paddle, divider)
        self.add_widget(game_field)
```

We should add a ball. We want the ball to bounce off the top and bottom of the play field and off the paddles. To keep the ball moving we can just create an `asyncio.Task`:

```py
import asyncio
import random

from nurses_2.app import App
from nurses_2.colors import GREEN, BLUE, WHITE, ColorPair
from nurses_2.widgets.widget import Widget

FIELD_HEIGHT = 25
FIELD_WIDTH = 100
WHITE_ON_GREEN = ColorPair.from_colors(WHITE, GREEN)

PADDLE_HEIGHT = 5
PADDLE_WIDTH = 1
WHITE_ON_BLUE = ColorPair.from_colors(WHITE, BLUE)


class Paddle(Widget):
    def __init__(self, player, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = player

    def on_press(self, key_press_event):
        if self.player == 1:
            if key_press_event.key == "w":
                self.y -= 1
            elif key_press_event.key == "s":
                self.y += 1
        elif self.player == 2:
            if key_press_event.key == "up":
                self.y -= 1
            elif key_press_event.key == "down":
                self.y += 1

        if self.y < 0:
            self.y = 0
        elif self.y > FIELD_HEIGHT - PADDLE_HEIGHT:
            self.y = FIELD_HEIGHT - PADDLE_HEIGHT


class Ball(Widget):
    def __init__(self, left_paddle, right_paddle, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left_paddle = left_paddle
        self.right_paddle = right_paddle
        asyncio.create_task(self.update())

    def reset(self):
        self.y_pos = FIELD_HEIGHT / 2
        self.x_pos = FIELD_WIDTH / 2 - 1
        self.y_velocity = 0.0
        self.x_velocity = 1.0
        self.speed = 1.0

    def bounce_paddle(self, paddle):
        self.x_velocity *= -1
        self.x_pos += 2 * self.x_velocity
        paddle_middle = (paddle.bottom + paddle.top) // 2
        self.y_velocity += (self.y - paddle_middle) / 5 + random.random() / 20
        self.speed *= 1.1

    def normalize_speed(self):
        current_speed = (self.y_velocity**2 + self.x_velocity**2)**.5
        if current_speed > self.speed:
            self.x_velocity *= self.speed / current_speed
            self.y_velocity *= self.speed / current_speed

    async def update(self):
        self.reset()

        while True:
            self.y_pos += self.y_velocity
            self.x_pos += self.x_velocity

            if self.collides_widget(self.left_paddle):
                self.bounce_paddle(self.left_paddle)
            elif self.collides_widget(self.right_paddle):
                self.bounce_paddle(self.right_paddle)

            if self.y_pos < 0 or self.y_pos >= FIELD_HEIGHT:
                self.y_velocity *= -1
                self.y_pos += 2 * self.y_velocity

            if self.x_pos < 0 or self.x_pos >= FIELD_WIDTH:
                self.reset()

            self.normalize_speed()

            self.y = int(self.y_pos)
            self.x = int(self.x_pos)

            await asyncio.sleep(.04)


class Pong(App):
    async def on_start(self):
        game_field = Widget(
            size=(FIELD_HEIGHT, FIELD_WIDTH),
            background_color_pair=WHITE_ON_GREEN,
        )

        vertical_center = FIELD_HEIGHT // 2 - PADDLE_HEIGHT // 2

        left_paddle = Paddle(
            player=1,
            size=(PADDLE_HEIGHT, PADDLE_WIDTH),
            pos=(vertical_center, 1),
            background_color_pair=WHITE_ON_BLUE,
        )

        right_paddle = Paddle(
            player=2,
            size=(PADDLE_HEIGHT, PADDLE_WIDTH),
            pos=(vertical_center, FIELD_WIDTH - 2),
            background_color_pair=WHITE_ON_BLUE,
        )

        divider = Widget(
            size=(1, 1),
            size_hint=(1.0, None),
            pos_hint=(None, .5),
            background_color_pair=WHITE_ON_BLUE,
        )

        ball = Ball(
            left_paddle,
            right_paddle,
            size=(1, 2),
            background_color_pair=WHITE_ON_BLUE,
        )

        game_field.add_widgets(left_paddle, right_paddle, divider, ball)
        self.add_widget(game_field)


if __name__ == "__main__":
    Pong().run()
```

Finally, let's keep track of the players' score. To place the scores in the correct place, we can use `pos_hint` again, but we'll also use the `anchor` kwarg to make sure the hint is applied to the center of the widgets and not the default (top-left). We'll also need a `TextWidget` which can contain arbitrary text, as normal `Widget`s only have at most a single background character:

```py
import asyncio
import random

from nurses_2.app import App
from nurses_2.colors import GREEN, BLUE, WHITE, ColorPair
from nurses_2.widgets.widget import Widget
from nurses_2.widgets.text_widget import TextWidget

FIELD_HEIGHT = 25
FIELD_WIDTH = 100
WHITE_ON_GREEN = ColorPair.from_colors(WHITE, GREEN)

PADDLE_HEIGHT = 5
PADDLE_WIDTH = 1
WHITE_ON_BLUE = ColorPair.from_colors(WHITE, BLUE)


class Paddle(Widget):
    def __init__(self, player, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = player

    def on_press(self, key_press_event):
        if self.player == 1:
            if key_press_event.key == "w":
                self.y -= 1
            elif key_press_event.key == "s":
                self.y += 1
        elif self.player == 2:
            if key_press_event.key == "up":
                self.y -= 1
            elif key_press_event.key == "down":
                self.y += 1

        if self.y < 0:
            self.y = 0
        elif self.y > FIELD_HEIGHT - PADDLE_HEIGHT:
            self.y = FIELD_HEIGHT - PADDLE_HEIGHT


class Ball(Widget):
    def __init__(self, left_paddle, right_paddle, left_label, right_label, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left_paddle = left_paddle
        self.right_paddle = right_paddle
        self.left_label = left_label
        self.right_label = right_label
        self.left_score = self.right_score = 0
        asyncio.create_task(self.update())

    def reset(self):
        self.y_pos = FIELD_HEIGHT / 2
        self.x_pos = FIELD_WIDTH / 2 - 1
        self.y_velocity = 0.0
        self.x_velocity = 1.0
        self.speed = 1.0

    def bounce_paddle(self, paddle):
        self.x_velocity *= -1
        self.x_pos += 2 * self.x_velocity
        paddle_middle = (paddle.bottom + paddle.top) // 2
        self.y_velocity += (self.y - paddle_middle) / 5 + random.random() / 20
        self.speed *= 1.1

    def normalize_speed(self):
        current_speed = (self.y_velocity**2 + self.x_velocity**2)**.5
        if current_speed > self.speed:
            self.x_velocity *= self.speed / current_speed
            self.y_velocity *= self.speed / current_speed

    async def update(self):
        self.reset()
        left_score = right_score = 0
        self.left_label.add_text(f"{0:^5}")
        self.right_label.add_text(f"{0:^5}")

        while True:
            self.y_pos += self.y_velocity
            self.x_pos += self.x_velocity

            if self.collides_widget(self.left_paddle):
                self.bounce_paddle(self.left_paddle)
            elif self.collides_widget(self.right_paddle):
                self.bounce_paddle(self.right_paddle)

            if self.y_pos < 0 or self.y_pos >= FIELD_HEIGHT:
                self.y_velocity *= -1
                self.y_pos += 2 * self.y_velocity

            if self.x_pos < 0:
                self.reset()
                right_score += 1
                self.right_label.add_text(f"{right_score:^5}")
            elif self.x_pos >= FIELD_WIDTH:
                self.reset()
                left_score += 1
                self.left_label.add_text(f"{left_score:^5}")

            self.normalize_speed()

            self.y = int(self.y_pos)
            self.x = int(self.x_pos)

            await asyncio.sleep(.04)


class Pong(App):
    async def on_start(self):
        game_field = Widget(
            size=(FIELD_HEIGHT, FIELD_WIDTH),
            background_color_pair=WHITE_ON_GREEN,
        )

        vertical_center = FIELD_HEIGHT // 2 - PADDLE_HEIGHT // 2

        left_paddle = Paddle(
            player=1,
            size=(PADDLE_HEIGHT, PADDLE_WIDTH),
            pos=(vertical_center, 1),
            background_color_pair=WHITE_ON_BLUE,
        )

        right_paddle = Paddle(
            player=2,
            size=(PADDLE_HEIGHT, PADDLE_WIDTH),
            pos=(vertical_center, FIELD_WIDTH - 2),
            background_color_pair=WHITE_ON_BLUE,
        )

        divider = Widget(
            size=(1, 1),
            size_hint=(1.0, None),
            pos_hint=(None, .5),
            background_color_pair=WHITE_ON_BLUE,
        )

        left_score_label = TextWidget(
            size=(1, 5),
            pos=(1, 1),
            pos_hint=(None, .25),
            anchor="center",
        )

        right_score_label = TextWidget(
            size=(1, 5),
            pos=(1, 1),
            pos_hint=(None, .75),
            anchor="center",
        )

        ball = Ball(
            left_paddle,
            right_paddle,
            left_score_label,
            right_score_label,
            size=(1, 2),
            background_color_pair=WHITE_ON_BLUE,
        )

        game_field.add_widgets(left_paddle, right_paddle, divider, left_score_label, right_score_label, ball)
        self.add_widget(game_field)


if __name__ == "__main__":
    Pong(title="Pong").run()
```