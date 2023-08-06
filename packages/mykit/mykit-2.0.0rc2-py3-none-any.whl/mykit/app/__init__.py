import tkinter as _tk
import typing as _typing

from mykit.app._runtime import Runtime as _Rt
from mykit.app.button import Button as _Button
from mykit.app.label import Label as _Label
from mykit.app.slider import _Slider


class App(_Rt):
    """
    Single-page app.

    ---

    ## Limitations
    - currently available only in fullscreen mode
    """

    def __init__(self, title: str = 'app', bg: str = '#111111') -> None:
        
        self.root = _tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.title(title)

        page = _tk.Canvas(
            master=self.root,
            width=self.root.winfo_screenwidth(),
            height=self.root.winfo_screenheight(),
            background=bg,
            borderwidth=0, highlightthickness=0
        )
        page.place(x=0, y=0)
        App.page = page


        ## <constants>
        self.MON_WIDTH = self.root.winfo_screenwidth()
        self.MON_HEIGHT = self.root.winfo_screenheight()
        ## </constants>


        ## <runtime>
        self._left_mouse_press = []
        self._left_mouse_hold = []
        self._left_mouse_release = []

        self._setup = None
        self._teardown = None
        ## </runtime>

    def listen(self, to: str, do: _typing.Callable[[_tk.Event], None]):
        """
        Add event listener.

        ---

        ## Params
        - `to`: `Literal["left-mouse-press", "left-mouse-hold", "left-mouse-release"]`

        ## Docs
        - `do` function takes 1 positional parameter, which is a tkinter event object
        """
        
        if to == 'left-mouse-press':
            self._left_mouse_press.append(do)
        elif to == 'left-mouse-hold':
            self._left_mouse_hold.append(do)
        elif to == 'left-mouse-release':
            self._left_mouse_release.append(do)
        else:
            ValueError(f'Invalid event: {repr(to)}.')

    def setup(self, funcs: list[_typing.Callable[[], None]]):
        self._setup = funcs

    def teardown(self, funcs: list[_typing.Callable[[], None]]):
        self._teardown = funcs

    def run(self):
        
        ## <listeners>

        def left_mouse_press(e):
            
            ## internal
            _Button.press_listener()
            _Slider.press_listener()
            
            ## external
            for fn in self._left_mouse_press:
                fn(e)

        self.root.bind('<ButtonPress-1>', left_mouse_press)

        def left_mouse_hold(e):
            
            ## internal
            _Slider.hold_listener()

            ## external
            for fn in self._left_mouse_hold:
                fn(e)

        self.root.bind('<B1-Motion>', left_mouse_hold)

        def left_mouse_release(e):

            ## internal
            _Button.release_listener()
            _Slider.release_listener()

            ## external
            for fn in self._left_mouse_release:
                fn(e)
        self.root.bind('<ButtonRelease-1>', left_mouse_release)

        self.root.bind('<Escape>', lambda e: self.root.destroy())

        ## </listeners>


        ## <background processes>
        
        def repeat50():
            _Button.hover_listener()
            _Slider.hover_listener()
            self.root.after(50, repeat50)
        repeat50()
        
        ## </background processes>


        ## setup
        if self._setup is not None:
            for fn in self._setup:
                fn()


        ## run
        self.root.mainloop()


        ## teardown
        if self._teardown is not None:
            for fn in self._teardown:
                fn()