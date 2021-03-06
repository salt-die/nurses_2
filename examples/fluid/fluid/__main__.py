import asyncio

import numpy as np

from nurses_2.app import App
from nurses_2.colors import Color, ColorPair, BLACK, BLACK_ON_BLACK, WHITE_ON_BLACK
from nurses_2.io import MouseButton
from nurses_2.widgets.text_widget import TextWidget
from nurses_2.widgets.graphic_widget import GraphicWidget, Anchor
from nurses_2.widgets.slider import Slider

from .sph import SPHSolver

WATER_COLOR = Color.from_hex("1e1ea8")
FILL_COLOR = Color.from_hex("2fa399")
WATER_ON_BLACK = ColorPair.from_colors(WATER_COLOR, BLACK)


class Fluid(GraphicWidget):
    def __init__(self, nparticles=1000, **kwargs):
        super().__init__(**kwargs)
        y, x = self.size
        self.sph_solver = SPHSolver((2 * y - 1, x - 1), nparticles)
        self._update_task = asyncio.create_task(self._update())

    def on_press(self, key_press_event):
        match key_press_event.key:
            case "r":
                self.sph_solver.init_dam()
                return True

        return False

    def on_click(self, mouse_event):
        if (
            mouse_event.button is MouseButton.NO_BUTTON
            or not self.collides_point(mouse_event.position)
        ):
            return False

        # Apply a force from click to every particle in the solver.
        my, mx = self.to_local(mouse_event.position)

        relative_positions = self.sph_solver.state[:, :2] - (2 * my, mx)

        self.sph_solver.state[:, 4:6] += (
            1000 * relative_positions
            / np.linalg.norm(relative_positions, axis=-1, keepdims=True)
        )

        return True

    async def _update(self):
        while True:
            solver = self.sph_solver
            solver.step()

            positions = solver.state[:, :2]
            ys, xs = positions.astype(int).T

            pressure = solver.state[:, -1]
            alphas = (255 / (1 + np.e**-(.125 * pressure))).astype(int)

            self.texture[:] = self.default_color
            self.texture[ys, xs, :3] = WATER_COLOR
            self.texture[ys, xs, 3] = alphas

            await asyncio.sleep(0)


class MyApp(App):
    async def on_start(self):
        WIDTH = 51
        HWIDTH = WIDTH // 2

        container = TextWidget(
            size=(26, WIDTH),
            pos_hint=(.5, .5),
            anchor=Anchor.CENTER,
            default_color_pair=BLACK_ON_BLACK
        )
        container.colors[:6] = WHITE_ON_BLACK

        fluid = Fluid(pos=(6, 0), size=(20, 50))
        solver = fluid.sph_solver

        slider_settings = {
            "width": HWIDTH,
            "fill_color": FILL_COLOR,
            "default_color_pair": WATER_ON_BLACK,
        }

        adjust_H = Slider(
            pos=(1, 0),
            min=.4,
            max=1.44,
            proportion=.04711,
            callback=lambda value: (
                setattr(solver, "H", value),
                container.add_text(
                    f'{f"Smoothing Length: {round(solver.H, 4)}":<{HWIDTH}}',
                ),
            ),
            **slider_settings,
        )

        adjust_GAS_CONST = Slider(
            pos=(1, HWIDTH + 1),
            min=100.0,
            max=4000.0,
            proportion=.02564,
            callback=lambda value: (
                setattr(solver, "GAS_CONST", value),
                container.add_text(
                    f'{f"Gas Constant: {round(solver.GAS_CONST, 4)}":<{HWIDTH}}',
                    column=HWIDTH,
                ),
            ),
            **slider_settings,
        )

        adjust_REST_DENS = Slider(
            pos=(3, 0),
            min=40.0,
            max=400.0,
            proportion=.44444,
            callback=lambda value: (
                setattr(solver, "REST_DENS", value),
                container.add_text(
                    f'{f"Rest Density: {round(solver.REST_DENS, 4)}":<{HWIDTH}}',
                    row=2,
                ),
            ),
            **slider_settings,
        )

        adjust_POLYF = Slider(
            pos=(3, HWIDTH + 1),
            min=1.0,
            max=10.0,
            proportion=0.0,
            callback=lambda value: (
                setattr(solver, "POLYF", value),
                container.add_text(
                    f'{f"Poly 6 Kernel: {round(solver.POLYF, 4)}":<{HWIDTH}}',
                    row=2,
                    column=HWIDTH,
                ),
            ),
            **slider_settings,
        )

        adjust_VISCF = Slider(
            pos=(5, 0),
            min=1000.0,
            max=5000.0,
            proportion=1.0,
            callback=lambda value: (
                setattr(solver, "VISCF", value),
                container.add_text(
                    f'{f"Viscosity: {round(solver.VISCF, 4)}":<{HWIDTH}}',
                    row=4,
                ),
            ),
            **slider_settings,
        )

        adjust_SPIKYF = Slider(
            pos=(5, HWIDTH + 1),
            min=-10.0,
            max=-1.0,
            proportion=.55555,
            callback=lambda value: (
                setattr(solver, "SPIKYF", value),
                container.add_text(
                    f'{f"Spiky Gradient: {round(solver.SPIKYF, 4)}":<{HWIDTH}}',
                    row=4,
                    column=HWIDTH,
                ),
            ),
            **slider_settings,
        )

        container.add_widgets(
            fluid,
            adjust_H,
            adjust_GAS_CONST,
            adjust_REST_DENS,
            adjust_POLYF,
            adjust_VISCF,
            adjust_SPIKYF,
        )

        self.add_widget(container)


MyApp(title="Smooth Particle Hydrodynamics Example").run()
