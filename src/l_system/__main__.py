import argparse

from l_system.rendering.renderer import GlobalSettings, LSystemRenderer


def main() -> None:
    parser = argparse.ArgumentParser(prog="l-system", description="Render L-systems with turtle graphics.")
    parser.add_argument(
        "--animate",
        "-a",
        dest="animate",
        action="store_true",
        default=True,
        help="If provided, animate turtle movement. (default: False)",
    )

    args = parser.parse_args()

    global_settings = GlobalSettings(args.animate)
    renderer = LSystemRenderer(global_settings)
    renderer.draw()


if __name__ == "__main__":
    main()
