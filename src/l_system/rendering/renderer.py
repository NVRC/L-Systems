import tkinter as tk
import turtle
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import List, Tuple

import tqdm
from examples import (
    bracketed_ol_system_fig1_24a,
    bracketed_ol_system_fig1_24b,
    bracketed_ol_system_fig1_24c,
    bracketed_ol_system_fig1_24d,
    bracketed_ol_system_fig1_24f,
    dragon_curve,
    hexagonal_gosper_curve,
    islands_and_lakes,
    koch_curves_fig1_7b,
    koch_curves_fig1_9a,
    koch_curves_fig1_9b,
    koch_curves_fig1_9c,
    koch_curves_fig1_9d,
    koch_curves_fig1_9e,
    koch_curves_fig1_9f,
    koch_island,
    sierpinski_gask,
)

from l_system.base import Lsystem
from l_system.rendering.turtle import LSystemTurtle, TurtleConfiguration

Example = Tuple[Lsystem, TurtleConfiguration]

EXAMPLES: List[Example] = [
    (dragon_curve.DragonCurve(), dragon_curve.DEFAULT_TURTLE_CONFIG),
    (sierpinski_gask.SierpinskiGask(), sierpinski_gask.DEFAULT_TURTLE_CONFIG),
    (koch_island.KochIsland(), koch_island.DEFAULT_TURTLE_CONFIG),
    (hexagonal_gosper_curve.HexagonalGosperCurve(), hexagonal_gosper_curve.DEFAULT_TURTLE_CONFIG),
    (islands_and_lakes.IslandsAndLakes(), islands_and_lakes.DEFAULT_TURTLE_CONFIG),
    (bracketed_ol_system_fig1_24a.BracketedOlSystemFig124a(), bracketed_ol_system_fig1_24a.DEFAULT_TURTLE_CONFIG),
    (bracketed_ol_system_fig1_24b.BracketedOlSystemFig124b(), bracketed_ol_system_fig1_24b.DEFAULT_TURTLE_CONFIG),
    (bracketed_ol_system_fig1_24c.BracketedOlSystemFig124c(), bracketed_ol_system_fig1_24c.DEFAULT_TURTLE_CONFIG),
    (bracketed_ol_system_fig1_24d.BracketedOlSystemFig124d(), bracketed_ol_system_fig1_24d.DEFAULT_TURTLE_CONFIG),
    (bracketed_ol_system_fig1_24f.BracketedOlSystemFig124f(), bracketed_ol_system_fig1_24f.DEFAULT_TURTLE_CONFIG),
    (koch_curves_fig1_7b.QuadraticSnowFlakeCurve(), koch_curves_fig1_7b.DEFAULT_TURTLE_CONFIG),
    (koch_curves_fig1_9a.KochCurvesFig19a(), koch_curves_fig1_9a.DEFAULT_TURTLE_CONFIG),
    (koch_curves_fig1_9b.KochCurvesFig19b(), koch_curves_fig1_9b.DEFAULT_TURTLE_CONFIG),
    (koch_curves_fig1_9c.KochCurvesFig19c(), koch_curves_fig1_9c.DEFAULT_TURTLE_CONFIG),
    (koch_curves_fig1_9d.KochCurvesFig19d(), koch_curves_fig1_9d.DEFAULT_TURTLE_CONFIG),
    (koch_curves_fig1_9e.KochCurvesFig19e(), koch_curves_fig1_9e.DEFAULT_TURTLE_CONFIG),
    (koch_curves_fig1_9f.KochCurvesFig19f(), koch_curves_fig1_9f.DEFAULT_TURTLE_CONFIG),
]

DEFAULT_L_SYSTEM, DEFAULT_TURTLE_CONFIG = EXAMPLES[0]


@dataclass
class GlobalSettings:
    animate: bool


class LSystemRenderer:
    def __init__(
        self,
        global_settings: GlobalSettings,
        l_system: Lsystem = DEFAULT_L_SYSTEM,
        turtle_configuration: TurtleConfiguration = DEFAULT_TURTLE_CONFIG,
        width: int = 400,
        height: int = 400,
    ):
        """
        Renders an L-system (`l_system`) on screen using`turtle` graphics.

        Args:
            l_system: An instantiated L-System object.
            turtle_configuration: A configuration object for the turtle rendering.
            width: Window width.
            height: Window height.
        """
        self.width = width
        self.height = height
        self.global_settings = global_settings

        # Initialize a root Tk to manage the canvas within this single `LSystemRenderer`
        self._root = tk.Tk()
        self._root.option_add("*tearOff", tk.FALSE)
        self._canvas = turtle.ScrolledCanvas(self._root, width=width, height=height)
        self._canvas.pack(side=tk.LEFT)
        self._screen = turtle.TurtleScreen(self._canvas)

        # Add a menu to select from existing examples
        menubar = tk.Menu(self._root)
        self._root.config(menu=menubar)
        file_menu = tk.Menu(menubar)

        examples_menu = tk.Menu(file_menu)
        for example in EXAMPLES:
            lsystem, lsystem_config = example
            print(f"Registering L-System({lsystem.name()}) with turtle configuration: {lsystem_config}")
            examples_menu.add_command(label=lsystem.name(), command=partial(self.set_system, lsystem, lsystem_config))

        file_menu.add_cascade(label="Select Example", menu=examples_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._root.destroy)

        menubar.add_cascade(label="File", menu=file_menu, underline=0)
        menubar.add_command(label="Settings", command=self.settings_modal)

        self.set_system(l_system, turtle_configuration)

    def settings_modal(self) -> None:
        """Initialize a pop-up modal to mutate global settings."""
        modal = tk.Toplevel(self._root)
        modal.title("Settings")

        # Define a `TurtleConfiguration` callback
        animate_var = tk.BooleanVar(modal, value=self.global_settings.animate, name="animate")
        animate_var.set(self.global_settings.animate)

        def set_animate() -> None:
            self.global_settings.animate = animate_var.get()
            self.draw()

        animate_checkbox = tk.Checkbutton(
            modal, text="Animate", command=set_animate, variable=animate_var, onvalue=True, offvalue=False
        )
        animate_checkbox.pack()

        modal.grab_set()

    def set_system(self, l_system: Lsystem, turtle_config: TurtleConfiguration) -> None:
        self._screen.clear()

        self.lsystem = l_system
        self._turtle_conf = turtle_config
        print(f"Setting L-System({self.lsystem.name()}) with turtle configuration: {turtle_config}")

        self._screen.bgcolor(*self._turtle_conf.bg_color)

        self._turtle = LSystemTurtle(
            self._screen,
            delta=self._turtle_conf.angle,
            forward_step=self._turtle_conf.forward_step,
            speed=self._turtle_conf.speed,
            heading=self._turtle_conf.initial_heading_angle,
            fg_color=self._turtle_conf.fg_color,
        )
        self.title = self.lsystem.name()
        self._root.title(self.title)
        self.lsystem.apply()
        self.draw()

    def draw(self, save_to_eps_file: Path | None = None) -> None:
        """
        Draw the L-system on screen using the `turtle` Python module.

        Args:
            animate: Will show turtle animations if set to `True`, otherwise it will render the final state of the
                L-System without any animations.
            save_to_eps_file: If a `Path` object provided, it will save the rendered L-System to an `eps` file. If set
                to `None` it will only render the L-System without storing it.
        """
        try:
            self._update_world_coordinates()
            self._turtle.animate(self.global_settings.animate)
            self._run_all_moves()
            self._turtle.hideturtle()
            self._turtle.update()
            if save_to_eps_file:
                self._turtle.save_to_eps(f"{save_to_eps_file}.eps")
            self._turtle.mainloop()
        except (turtle.Terminator, tk.TclError):
            print("Exiting...")

    def _run_all_moves(self) -> None:
        """Runs all the `turtle` moves of the L-system."""
        for i, l_str in tqdm.tqdm(
            enumerate(self.lsystem, start=1),
            total=len(self.lsystem),
            desc=f"Rendering L-System '{self.lsystem.name()}'",
        ):
            self._root.title(f"{self.title} | {100*(i/len(self.lsystem)):.0f} %")
            k = self._turtle_conf.turtle_move_mapper.get(l_str, l_str)
            self._turtle.move(k)

    def _update_world_coordinates(self) -> None:
        """Updates the `turtle` world coordinates by first running the `turtle` on the L-System to find min, max
        coordinates. Then it uses these values to make sure the final L-System is visible in the window.
        """

        # NOTE: This implementation is computationally expensive
        self._turtle.reset()
        self._turtle.animate(False)
        self._run_all_moves()

        minx, miny, maxx, maxy = self._turtle.bounding_box.to_tuple()
        w = maxx - minx
        h = maxy - miny
        epsilon = 0.00001
        r = max(w, h) / (min(w, h) + epsilon)
        if maxx - minx > maxy - miny:
            self._turtle.screen.setworldcoordinates(minx, miny - 1, maxx, (maxy - 1) * r)
        else:
            self._turtle.screen.setworldcoordinates(minx, miny, maxx * r, maxy)
        self._turtle.reset()
