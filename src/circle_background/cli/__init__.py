# SPDX-FileCopyrightText: 2024-present Silvio Knizek <killermoehre@gmx.net>
#
# SPDX-License-Identifier: eupl-1.2

import pathlib
import random
from decimal import Decimal

import click
import svg
from pydanclick import from_pydantic

from circle_background import Config
from circle_background.__about__ import __version__
from circle_background.types import Corner, Patch


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="circle-background")
@from_pydantic(Config)
def circle_background(config: Config) -> None:
    patch = Patch(
        height=config.height / config.fields_per_col,
        width=config.width / config.fields_per_row,
    )

    rectangles: list[svg.Rect] = []
    quarter_circles: list[svg.Path] = []

    for y in range(config.fields_per_col):
        for x in range(config.fields_per_row):
            start_x: Decimal = x * patch.width
            start_y: Decimal = y * patch.height
            rectangles.append(
                svg.Rect(
                    fill=random.choice(config.colors),
                    height=patch.height,
                    stroke_width=0,
                    width=patch.width,
                    x=start_x,
                    y=start_y,
                ),
            )

            corners: list[Corner] = []
            corners.append(Corner(x=start_x, y=start_y))
            corners.append(Corner(x=start_x + patch.width, y=start_y))
            corners.append(Corner(x=start_x + patch.width, y=start_y + patch.height))
            corners.append(Corner(x=start_x, y=start_y + patch.height))

            start_corner: int = random.choice(range(len(corners)))
            start_c = corners[start_corner]
            opp_c = corners[(start_corner + 2) % 4]
            last_c = corners[(start_corner + 3) % 4]

            quarter_circles.append(
                svg.Path(
                    fill=random.choice(config.colors),
                    stroke_width=0,
                    d=[
                        svg.MoveTo(x=start_c.x, y=start_c.y),
                        svg.Arc(
                            angle=0,
                            large_arc=False,
                            rx=opp_c.x - start_c.x,
                            ry=opp_c.y - start_c.y,
                            sweep=True,
                            x=opp_c.x,
                            y=opp_c.y,
                        ),
                        svg.LineTo(x=last_c.x, y=last_c.y),
                        svg.ClosePath(),
                    ],
                )
            )
    data: svg.SVG = svg.SVG(
        viewBox=svg.ViewBoxSpec(0, 0, config.width, config.height),
        elements=rectangles + quarter_circles,
    )

    if config.output_file == "-":
        pathlib.sys.stdout.write(data.as_str())
    else:
        with open(pathlib.Path(config.output_file), "w") as output_file:
            output_file.write(data.as_str())
