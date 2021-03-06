"""
Paste into the terminal to test paste dispatching.
"""
import asyncio

from nurses_2.app import run_widget_as_app
from nurses_2.widgets.text_widget import TextWidget
from nurses_2.io import PasteEvent

class PasteWidget(TextWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._clear_task = asyncio.create_task(asyncio.sleep(0))  # dummy task

    async def _clear_paste(self):
        await asyncio.sleep(5)
        self.canvas[:] = " "

    def on_paste(self, paste_event: PasteEvent):
        self.add_text("Got paste:")

        for i, line in enumerate(paste_event.paste.splitlines(), start=1):
            self.add_text(line[:self.width], row=i)

        if self._clear_task.done():
            self._clear_task = asyncio.create_task(self._clear_paste())


run_widget_as_app(PasteWidget, size=(10, 100))
