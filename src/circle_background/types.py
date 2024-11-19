# SPDX-FileCopyrightText: 2024-present Silvio Knizek <killermoehre@gmx.net>
#
# SPDX-License-Identifier: eupl-1.2

import decimal

import webcolors
from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated


def is_webcolor(color: str) -> str:
    assert color in webcolors.names() or webcolors.normalize_hex(
        color
    ), "{color} is not a recognized webcolor!"
    return color


type Color = Annotated[str, AfterValidator(is_webcolor)]


class Corner(BaseModel):
    x: decimal.Decimal = Field(ge=0)
    y: decimal.Decimal = Field(ge=0)


class Patch(BaseModel):
    height: decimal.Decimal = Field(gt=0)
    width: decimal.Decimal = Field(gt=0)
