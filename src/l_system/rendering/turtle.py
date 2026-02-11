"""
A helper wrapper class of the [turtle graphics](https://docs.python.org/3/library/turtle.html) used for rendering
L-Systems. The following turtle moves are supported:

https://paulbourke.net/fractals/lsys/
Symbols The following characters have a geometric interpretation.

Character        Meaning
   F	         Move forward by line length drawing a line
   f	         Move forward by line length without drawing a line
   +	         Turn left by turning angle
   -	         Turn right by turning angle
   [	         Push current drawing state onto stack
   ]	         Pop current drawing state from the stack

TODO:
   |	         Reverse direction (ie: turn by 180 degrees)
   #	         Increment the line width by line width increment
   !	         Decrement the line width by line width increment
   @	         Draw a dot with line width radius
   {	         Open a polygon
   }	         Close a polygon and fill it with fill colour
   >	         Multiply the line length by the line length scale factor
   <	         Divide the line length by the line length scale factor
   &	         Swap the meaning of + and -
   (	         Decrement turning angle by turning angle increment
   )	         Increment turning angle by turning angle increment
"""

import turtle
from dataclasses import astuple, dataclass, field


@dataclass
class TurtleConfiguration:
    """Turtle graphics configuration used by the L-System renderer class."""

    forward_step: int = 3
    """This value represents the distance the turtle will travel."""
    angle: float = 90
    """Rotation angle in degrees of the turtle."""
    initial_heading_angle: int = 0
    """Initial [orientation](https://docs.python.org/3/library/turtle.html#turtle.setheading) of the turtle."""
    speed: int = 0
    """The turtle's drawing [speed](https://docs.python.org/3/library/turtle.html#turtle.speed), 0 is the fastest."""
    fg_color: tuple[float, float, float] = (0.76, 0.71, 0.55)
    """The turtle's drawing color in (R, G, B) format."""
    bg_color: tuple[float, float, float] = (0.0, 0.0, 0.0)
    """The background color (window color) in (R, G, B) format."""
    turtle_move_mapper: dict[str, str] = field(default_factory=dict)
    """A dictionary that maps L-System symbols to turtle moves."""


@dataclass(frozen=False)
class TurtleBoundingBox:
    """A bounding box of the area the turtle has drawn to."""

    x_min: float
    y_min: float
    x_max: float
    y_max: float

    def to_tuple(self):
        return astuple(self)


class LSystemTurtle(turtle.RawTurtle):
    def __init__(
        self,
        screen: turtle.TurtleScreen,
        fg_color: tuple[float, float, float] = (0.0, 0.0, 0.0),
        delta: float = 90,
        forward_step: int = 5,
        speed: int = 0,
        heading: int = 0,
    ):
        """
        A turtle class for rendering L-Systems.
        It has a stack to push and pop its state (heading and position).
        It also stores the min and max positions it has visited in a bounding box which is used to adjust the
        coordinates making sure the rendered L-System is visible on screen.

        Args:
            screen: The parent container `turtle.TurtleScreen`.
            fg_color: The turtle's drawing color.
            delta: The angle in degrees the turtle uses to rotate.
            forward_step: The amount of steps the turtle takes every time it moves forward.
            speed: How fast the turtle will draw things. Default value is `0` which is the fastest mode.
            heading: The initial heading of the turtle before starting to draw things on screen.
        """
        super().__init__(screen)

        self._delta = delta
        self._lspeed = speed
        self._heading = heading
        self._forward_step = forward_step
        self._fg_color = fg_color

        self.bounding_box = TurtleBoundingBox(0, 0, 0, 0)
        self._state_stack = []

        self.reset()

        # all the available turtle moves are stored here.
        self._lsystem2turtle_map = {
            'F': self.forward,
            'f': self.up_forward,
            '+': self.left,
            '-': self.right,
            '[': self.push_turtle_state,
            ']': self.pop_turtle_state,
        }

    def reset(self) -> None:
        """Resets the state of the turtle."""
        super().reset()
        self.speed(self._lspeed)
        self.setheading(self._heading)
        self.bounding_box = TurtleBoundingBox(0, 0, 0, 0)
        self.color(*self._fg_color)

    def _update_bounding_box(self) -> None:
        """Every time the turtle makes a move it updates its bounding box. This is used by the renderer to make sure
        the final rendered L-System will be visible."""
        x, y = self.position()

        if x < self.bounding_box.x_min:
            self.bounding_box.x_min = x
        elif x > self.bounding_box.x_max:
            self.bounding_box.x_max = x

        if y < self.bounding_box.y_min:
            self.bounding_box.y_min = y
        elif y > self.bounding_box.y_max:
            self.bounding_box.y_max = y

    def animate(self, value: bool) -> None:
        """
        Whether to draw the L-System with animations.

        Args:
            value: If set to `True` the turtle will render the L-System with animations, otherwise it will only render
                the final state of the L-System.
        """
        self.screen.tracer(value)

    def update(self) -> None:
        """Update the screen."""
        self.screen.update()

    def mainloop(self) -> None:
        self.screen.mainloop()

    def save_to_eps(self, save_to_eps_file: str) -> None:
        """
        Save the rendered graphics to an eps file.

        Args:
            save_to_eps_file: A `Path` object where the rendered turtle graphics will be stored.
        """
        ts = self.getscreen()
        ts.getcanvas().postscript(file=f"{save_to_eps_file}.eps")

    def move(self, mv_cmd: str) -> None:
        """
        It moves the turtle based on an input string.

        Args:
            mv_cmd: A string that defines how the turtle will move next.

        Raises:
            KeyError: If the `mv_cmd` move is not implemented (`mv_cmd` is not a key of the `self._lsystem2turtle_map`
                dictionary).
        """
        try:
            self._lsystem2turtle_map[mv_cmd]()
        except KeyError as exc:
            raise KeyError(f"{mv_cmd} not found!") from exc

    def forward(self, *args) -> None:
        """Moves the turtle forward and updates the turtle's bounding box."""
        super().forward(self._forward_step)
        self._update_bounding_box()

    def left(self, *args) -> None:
        """Rotates the turtle left and updates it's bounding box."""
        super().left(self._delta)
        self._update_bounding_box()

    def right(self, *args) -> None:
        """Rotates the turtle right and updates its bounding box."""
        super().right(self._delta)
        self._update_bounding_box()

    def up_forward(self) -> None:
        """Moves the turtle forward without drawing and updates the turtle's bounding box."""
        super().up()
        self.forward()
        super().down()
        self._update_bounding_box()

    def push_turtle_state(self) -> None:
        """Pushes the current state of the turtle (heading and orientation) to its stack."""
        t_heading = super().heading()
        t_position = super().position()
        self._state_stack.append((t_heading, t_position))

    def pop_turtle_state(self) -> None:
        """Pops a previously stored turtle state (heading and orientation) from stack."""
        t_heading, t_position = self._state_stack.pop()
        super().up()
        super().setheading(t_heading)
        super().setposition(t_position[0], t_position[1])
        super().down()
