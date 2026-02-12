import json
import tkinter as tk
import turtle
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from tkinter import ttk
from typing import Dict, Tuple

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

EXAMPLES_MAP: Dict[str, Example] = {
    dragon_curve.DragonCurve.name(): (dragon_curve.DragonCurve(), dragon_curve.DEFAULT_TURTLE_CONFIG),
    sierpinski_gask.SierpinskiGask.name(): (sierpinski_gask.SierpinskiGask(), sierpinski_gask.DEFAULT_TURTLE_CONFIG),
    koch_island.KochIsland.name(): (koch_island.KochIsland(), koch_island.DEFAULT_TURTLE_CONFIG),
    hexagonal_gosper_curve.HexagonalGosperCurve.name(): (
        hexagonal_gosper_curve.HexagonalGosperCurve(),
        hexagonal_gosper_curve.DEFAULT_TURTLE_CONFIG,
    ),
    islands_and_lakes.IslandsAndLakes.name(): (
        islands_and_lakes.IslandsAndLakes(),
        islands_and_lakes.DEFAULT_TURTLE_CONFIG,
    ),
    bracketed_ol_system_fig1_24a.BracketedOlSystemFig124a.name(): (
        bracketed_ol_system_fig1_24a.BracketedOlSystemFig124a(),
        bracketed_ol_system_fig1_24a.DEFAULT_TURTLE_CONFIG,
    ),
    bracketed_ol_system_fig1_24b.BracketedOlSystemFig124b.name(): (
        bracketed_ol_system_fig1_24b.BracketedOlSystemFig124b(),
        bracketed_ol_system_fig1_24b.DEFAULT_TURTLE_CONFIG,
    ),
    bracketed_ol_system_fig1_24c.BracketedOlSystemFig124c.name(): (
        bracketed_ol_system_fig1_24c.BracketedOlSystemFig124c(),
        bracketed_ol_system_fig1_24c.DEFAULT_TURTLE_CONFIG,
    ),
    bracketed_ol_system_fig1_24d.BracketedOlSystemFig124d.name(): (
        bracketed_ol_system_fig1_24d.BracketedOlSystemFig124d(),
        bracketed_ol_system_fig1_24d.DEFAULT_TURTLE_CONFIG,
    ),
    bracketed_ol_system_fig1_24f.BracketedOlSystemFig124f.name(): (
        bracketed_ol_system_fig1_24f.BracketedOlSystemFig124f(),
        bracketed_ol_system_fig1_24f.DEFAULT_TURTLE_CONFIG,
    ),
    koch_curves_fig1_7b.QuadraticSnowFlakeCurve.name(): (
        koch_curves_fig1_7b.QuadraticSnowFlakeCurve(),
        koch_curves_fig1_7b.DEFAULT_TURTLE_CONFIG,
    ),
    koch_curves_fig1_9a.KochCurvesFig19a.name(): (
        koch_curves_fig1_9a.KochCurvesFig19a(),
        koch_curves_fig1_9a.DEFAULT_TURTLE_CONFIG,
    ),
    koch_curves_fig1_9b.KochCurvesFig19b.name(): (
        koch_curves_fig1_9b.KochCurvesFig19b(),
        koch_curves_fig1_9b.DEFAULT_TURTLE_CONFIG,
    ),
    koch_curves_fig1_9c.KochCurvesFig19c.name(): (
        koch_curves_fig1_9c.KochCurvesFig19c(),
        koch_curves_fig1_9c.DEFAULT_TURTLE_CONFIG,
    ),
    koch_curves_fig1_9d.KochCurvesFig19d.name(): (
        koch_curves_fig1_9d.KochCurvesFig19d(),
        koch_curves_fig1_9d.DEFAULT_TURTLE_CONFIG,
    ),
    koch_curves_fig1_9e.KochCurvesFig19e.name(): (
        koch_curves_fig1_9e.KochCurvesFig19e(),
        koch_curves_fig1_9e.DEFAULT_TURTLE_CONFIG,
    ),
    koch_curves_fig1_9f.KochCurvesFig19f.name(): (
        koch_curves_fig1_9f.KochCurvesFig19f(),
        koch_curves_fig1_9f.DEFAULT_TURTLE_CONFIG,
    ),
}

DEFAULT_L_SYSTEM, DEFAULT_TURTLE_CONFIG = EXAMPLES_MAP[dragon_curve.DragonCurve.name()]


@dataclass
class GlobalSettings:
    animate: bool


DEFAULT_ROOT_WIDTH = 400
DEFAULT_ROOT_HEIGHT = 400

STATIC_PADDING = 5


def check_var_isset(val: str) -> bool:
    if val is not None and val:
        return True
    return False


class LSystemRenderer(tk.Tk):
    def __init__(
        self,
        global_settings: GlobalSettings,
        l_system: Lsystem = DEFAULT_L_SYSTEM,
        turtle_configuration: TurtleConfiguration = DEFAULT_TURTLE_CONFIG,
        width: int = DEFAULT_ROOT_WIDTH,
        height: int = DEFAULT_ROOT_HEIGHT,
    ):
        """
        Renders an L-system (`l_system`) on screen using`turtle` graphics.

        Args:
            global_settings: A global settings object to configure turtle rendering.
            l_system: An instantiated L-System object.
            turtle_configuration: A configuration object for the turtle rendering.
            width: Window width.
            height: Window height.
        """
        super().__init__()
        self.width = width
        self.height = height
        self.global_settings = global_settings

        # Initialize a root Tk to manage the canvas within this single `LSystemRenderer`
        self.option_add("*tearOff", tk.FALSE)
        self._canvas = turtle.ScrolledCanvas(self, width=width, height=height)
        self._canvas.pack(side=tk.LEFT)
        self._screen = turtle.TurtleScreen(self._canvas)

        # Add a menu to select from existing examples
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar)

        examples_menu = tk.Menu(file_menu)
        for lsystem, lsystem_config in EXAMPLES_MAP.values():
            print(f"Registering L-System({lsystem.name()}) with turtle configuration: {lsystem_config}")
            examples_menu.add_command(label=lsystem.name(), command=partial(self.set_system, lsystem, lsystem_config))

        file_menu.add_cascade(label="Select Example", menu=examples_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)

        menubar.add_cascade(label="File", menu=file_menu, underline=0)
        menubar.add_command(label="Settings", command=self.settings_modal)

        self.set_system(l_system, turtle_configuration)

    def settings_modal(self) -> None:
        """Initialize a pop-up modal to mutate global and turtle settings."""

        # NOTE: Overall this modal implementation is poor.
        #       Get it to work, then polish.
        #       Have `TurtleConfiguration` extend `tk.Variable` to set/get related vars.

        modal = tk.Toplevel(self)
        modal.title("Settings")

        # Define a `TurtleConfiguration` callback
        animate_var = tk.BooleanVar(modal, value=self.global_settings.animate, name="animate")

        def _set_animate() -> None:
            self.global_settings.animate = animate_var.get()
            self.draw()

        animate_checkbox = tk.Checkbutton(
            modal, text="Animate", command=_set_animate, variable=animate_var, onvalue=True, offvalue=False
        )
        animate_checkbox.grid(row=0, column=0, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.W)

        v_check_var = (modal.register(check_var_isset), "%P")

        # Turtle Configuration labels and entries
        forward_step_var = tk.IntVar(modal, value=self._turtle_conf.forward_step, name="forward_step")
        angle_var = tk.DoubleVar(modal, value=self._turtle_conf.angle, name="angle")
        initial_heading_angle_var = tk.IntVar(
            modal, value=self._turtle_conf.initial_heading_angle, name="initial_heading_angle"
        )
        speed_var = tk.IntVar(modal, value=self._turtle_conf.speed, name="speed")
        fg_color_var = tk.StringVar(modal, value=json.dumps(self._turtle_conf.fg_color), name="fg_color")
        bg_color_var = tk.StringVar(modal, value=json.dumps(self._turtle_conf.bg_color), name="bg_color")
        turtle_move_map_var = tk.StringVar(
            modal, value=json.dumps(self._turtle_conf.turtle_move_mapper), name="turtle_move_map"
        )

        # State closure over Settings modal components
        def _set_turtle_conf() -> None:
            try:
                fg_color: Tuple[float, float, float] = json.loads(fg_color_var.get())
                bg_color: Tuple[float, float, float] = json.loads(bg_color_var.get())
                move_mapper: Dict[str, str] = json.loads(turtle_move_map_var.get())
                new_turtle_conf = TurtleConfiguration(
                    forward_step=forward_step_var.get(),
                    angle=angle_var.get(),
                    initial_heading_angle=initial_heading_angle_var.get(),
                    speed=speed_var.get(),
                    fg_color=fg_color,
                    bg_color=bg_color,
                    turtle_move_mapper=move_mapper,
                )
                self.set_system(self.lsystem, new_turtle_conf)
            except tk.TclError as ex:
                print(f"Unable to update turtle configuration: {ex}")

        apply_button = tk.Button(modal, text="Apply", command=_set_turtle_conf)
        apply_button.grid(row=0, column=1, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.E)
        separator = ttk.Separator(modal, orient=tk.HORIZONTAL)
        separator.grid(row=1, columnspan=2, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.EW)

        # Combobox L-system defaults selector
        l_system_name_var = tk.StringVar(modal, value=self.lsystem.name(), name="l_system_name")

        def _set_combobox(_: tk.Event) -> None:
            try:
                # Select L-system by name
                selected_name = l_system_name_var.get()
                new_lsys, new_lsys_conf = EXAMPLES_MAP.get(selected_name)
                # Set all turtle configuration modal closure vars
                forward_step_var.set(new_lsys_conf.forward_step)
                angle_var.set(new_lsys_conf.angle)
                initial_heading_angle_var.set(new_lsys_conf.initial_heading_angle)
                speed_var.set(new_lsys_conf.speed)
                fg_color_var.set(json.dumps(new_lsys_conf.fg_color))
                bg_color_var.set(json.dumps(new_lsys_conf.bg_color))
                turtle_move_map_var.set(json.dumps(new_lsys_conf.turtle_move_mapper))
                self.set_system(new_lsys, new_lsys_conf)
            except (tk.TclError, KeyError) as ex:
                print(f"Unable select pre-existing configuration: {ex}")

        combobox = ttk.Combobox(modal, values=list(EXAMPLES_MAP), textvariable=l_system_name_var)
        combobox.set(self.lsystem.name())
        combobox.bind("<<ComboboxSelected>>", _set_combobox)
        combobox.grid(row=2, columnspan=2, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.EW)

        forward_step_label = tk.Label(modal, text="Forward Step (int):")
        forward_step_label.grid(row=3, column=0, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.W)
        forward_step_entry = tk.Entry(
            modal, textvariable=forward_step_var, validate="focusout", validatecommand=v_check_var
        )
        forward_step_entry.grid(row=3, column=1, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.E)

        angle_label = tk.Label(modal, text="Angle (float):")
        angle_label.grid(row=4, column=0, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.W)
        angle_entry = tk.Entry(modal, textvariable=angle_var, validate="focusout", validatecommand=v_check_var)
        angle_entry.grid(row=4, column=1, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.E)

        initial_heading_angle_label = tk.Label(modal, text="Initial Heading Angle (int):")
        initial_heading_angle_label.grid(row=5, column=0, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.W)
        initial_heading_angle_entry = tk.Entry(
            modal, textvariable=initial_heading_angle_var, validate="focusout", validatecommand=v_check_var
        )
        initial_heading_angle_entry.grid(row=5, column=1, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.E)

        speed_label = tk.Label(modal, text="Speed (int):")
        speed_label.grid(row=6, column=0, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.W)
        speed_entry = tk.Entry(modal, textvariable=speed_var, validate="focusout", validatecommand=v_check_var)
        speed_entry.grid(row=6, column=1, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.E)

        fg_color_label = tk.Label(modal, text="Foreground color (R,G,B):")
        fg_color_label.grid(row=7, column=0, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.W)
        fg_color_entry = tk.Entry(modal, textvariable=fg_color_var, validate="focusout", validatecommand=v_check_var)
        fg_color_entry.grid(row=7, column=1, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.E)

        bg_color_label = tk.Label(modal, text="Background color (R,G,B):")
        bg_color_label.grid(row=8, column=0, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.W)
        bg_color_entry = tk.Entry(modal, textvariable=bg_color_var, validate="focusout", validatecommand=v_check_var)
        bg_color_entry.grid(row=8, column=1, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.E)

        turtle_move_mapper_label = tk.Label(modal, text="Turtle move mapper (Dict[str, str]):")
        turtle_move_mapper_label.grid(row=9, column=0, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.W)
        turtle_move_mapper_entry = tk.Entry(
            modal, textvariable=turtle_move_map_var, validate="focusout", validatecommand=v_check_var
        )
        turtle_move_mapper_entry.grid(row=9, column=1, padx=STATIC_PADDING, pady=STATIC_PADDING, sticky=tk.E)

        modal.grab_set()

    def set_system(self, l_system: Lsystem, turtle_config: TurtleConfiguration) -> None:
        """
        Update L-System state and rerender turtle with new configuration.
        Mutates private `self._screen: TurtleScreen` and re-assigns `self._turtle: LSystemTurtle`.

        Args:
            l_system: Concrete L-System to render.
            turtle_config: Render the L-System according to this TurtleConfiguration.
        """
        # Clear screen to redraw following assignments
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
        self.wm_title(self.lsystem.name())
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
            self.wm_title(f"{self.lsystem.name()} | {100*(i/len(self.lsystem)):.0f} %")
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
