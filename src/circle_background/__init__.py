# SPDX-FileCopyrightText: 2024-present Silvio Knizek <killermoehre@gmx.net>
#
# SPDX-License-Identifier: eupl-1.2


import decimal
from pathlib import Path

from pydantic import BaseModel, Field

from circle_background.types import Color


class Config(BaseModel):
    # colors taken from https://lospec.com/palette-list/dreamscape8
    colors: list[Color] = Field(
        default=[
            "#c9cca1",
            "#caa05a",
            "#ae6a47",
            "#8b4049",
            "#543344",
            "#515262",
            "#63787d",
            "#8ea091",
        ],
        description="Colors to use. Each patch are assigned two random values from this list. Those can be the same values.",
    )
    fields_per_col: int = Field(
        default=20,
        description="Number of fields per column. Default 20.",
        gt=0,
    )
    fields_per_row: int = Field(
        default=20,
        description="Number of fields per row. Default 20.",
        gt=0,
    )
    height: decimal.Decimal = Field(
        default=4096,
        description="Canvas height in px. Default 4096.",
        gt=0,
    )
    output_file: Path = Field(
        default="-",
        description="Output path. Default writes to STDOUT.",
    )
    width: decimal.Decimal = Field(
        default=4096,
        description="Canvas width in px. Default 4096.",
        gt=0,
    )
