# -*- coding: utf-8 -*-
# PyonFX: An easy way to create KFX (Karaoke Effects) and complex typesetting using the ASS format (Advanced Substation Alpha).
# Copyright (C) 2019 Antonio Strippoli (CoffeeStraw/YellowFlash)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyonFX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.

from __future__ import annotations
import re
import math
import colorsys
from enum import Enum
from typing import List, NamedTuple, Tuple, Union, TYPE_CHECKING

from .font_utility import Font

if TYPE_CHECKING:
    from .ass_core import Line, Word, Syllable, Char
    from .shape import Shape

# A simple NamedTuple to represent pixels
Pixel = NamedTuple("Pixel", [("x", float), ("y", float), ("alpha", int)])


class ColorModel(Enum):
    ASS = "&HBBGGRR&"
    ASS_STYLE = "&HAABBGGRR"
    RGB = "(r, g, b)"
    RGB_STR = "#RRGGBB"
    RGBA = "(r, g, b, a)"
    RGBA_STR = "#RRGGBBAA"
    HSV = "(h, s, v)"


class Convert:
    """
    This class is a collection of static methods that will help
    the user to convert everything needed to the ASS format.
    """

    @staticmethod
    def time(ass_ms: Union[int, str]) -> Union[str, int, ValueError]:
        """Converts between milliseconds and ASS timestamp.

        You can probably ignore that function, you will not make use of it for KFX or typesetting generation.

        Parameters:
            ass_ms (int or str): If int, than milliseconds are expected, else ASS timestamp as str is expected.

        Returns:
            If milliseconds -> ASS timestamp, else if ASS timestamp -> milliseconds, else ValueError will be raised.
        """
        # Milliseconds?
        if type(ass_ms) is int and ass_ms >= 0:
            return "{:d}:{:02d}:{:02d}.{:02d}".format(
                math.floor(ass_ms / 3600000) % 10,
                math.floor(ass_ms % 3600000 / 60000),
                math.floor(ass_ms % 60000 / 1000),
                math.floor(ass_ms % 1000 / 10),
            )
        # ASS timestamp?
        elif type(ass_ms) is str and re.match(r"^\d:\d+:\d+\.\d+$", ass_ms):
            return (
                int(ass_ms[0]) * 3600000
                + int(ass_ms[2:4]) * 60000
                + int(ass_ms[5:7]) * 1000
                + int(ass_ms[8:10]) * 10
            )
        else:
            raise ValueError("Milliseconds or ASS timestamp expected")

    @staticmethod
    def alpha_ass_to_dec(alpha_ass: str) -> int:
        """Converts from ASS alpha string to corresponding decimal value.

        Parameters:
            alpha_ass (str): A string in the format '&HXX&'.

        Returns:
            A decimal in [0, 255] representing ``alpha_ass`` converted.

        Examples:
            ..  code-block:: python3

                print(Convert.alpha_ass_to_dec("&HFF&"))

            >>> 255
        """
        try:
            match = re.fullmatch(r"&H([0-9A-F]{2})&", alpha_ass)
            return int(match.group(1), 16)
        except TypeError as e:
            raise TypeError(
                f"Provided ASS alpha was expected of type 'str', but you provided a '{type(alpha_ass)}'."
            ) from e
        except AttributeError as e:
            raise ValueError(
                f"Provided ASS alpha string '{alpha_ass}' is not in the expected format '&HXX&'."
            ) from e

    @staticmethod
    def alpha_dec_to_ass(alpha_dec: Union[int, float]) -> str:
        """Converts from decimal value to corresponding ASS alpha string.

        Parameters:
            alpha_dec (int or float): Decimal in [0, 255] representing an alpha value.

        Returns:
            A string in the format '&HXX&' representing ``alpha_dec`` converted.

        Examples:
            ..  code-block:: python3

                print(Convert.alpha_dec_to_ass(255))
                print(Convert.alpha_dec_to_ass(255.0))

            >>> "&HFF&"
            >>> "&HFF&"
        """
        try:
            if not 0 <= alpha_dec <= 255:
                raise ValueError(
                    f"Provided alpha decimal '{alpha_dec}' is out of the range [0, 255]."
                )
        except TypeError as e:
            raise TypeError(
                f"Provided alpha decimal was expected of type 'int' or 'float', but you provided a '{type(alpha_dec)}'."
            ) from e
        return f"&H{round(alpha_dec):02X}&"

    @staticmethod
    def color(
        c: Union[
            str,
            Union[
                Tuple[
                    Union[int, float],
                    Union[int, float],
                    Union[int, float],
                ],
                Tuple[
                    Union[int, float],
                    Union[int, float],
                    Union[int, float],
                    Union[int, float],
                ],
            ],
        ],
        input_format: ColorModel,
        output_format: ColorModel,
        round_output: bool = True,
    ) -> Union[
        str,
        Tuple[int, int, int],
        Tuple[int, int, int, int],
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]:
        """Converts a provided color from a color model to another.

        Parameters:
            c (str or tuple of int or tuple of float): A color in the format ``input_format``.
            input_format (ColorModel): The color format of ``c``.
            output_format (ColorModel): The color format for the output.
            round_output (bool): A boolean to determine whether the output should be rounded or not.

        Returns:
            A color in the format ``output_format``.

        Examples:
            ..  code-block:: python3

                print(Convert.color("&H0000FF&", ColorModel.ASS, ColorModel.RGB))

            >>> (255, 0, 0)
        """
        try:
            # Text for exception if input is out of ranges
            input_range_e = f"Provided input '{c}' has value(s) out of the range "

            # Parse input, obtaining its corresponding (r,g,b,a) values
            if input_format == ColorModel.ASS:
                match = re.fullmatch(r"&H([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})&", c)
                (b, g, r), a = map(lambda x: int(x, 16), match.groups()), 255
            elif input_format == ColorModel.ASS_STYLE:
                match = re.fullmatch(
                    r"&H([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})", c
                )
                a, b, g, r = map(lambda x: int(x, 16), match.groups())
            elif input_format == ColorModel.RGB:
                if not all(0 <= n <= 255 for n in c):
                    raise ValueError(input_range_e + "[0, 255].")
                (r, g, b), a = c, 255
            elif input_format == ColorModel.RGB_STR:
                match = re.fullmatch(r"#([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})", c)
                (r, g, b), a = map(lambda x: int(x, 16), match.groups()), 255
            elif input_format == ColorModel.RGBA:
                if not all(0 <= n <= 255 for n in c):
                    raise ValueError(input_range_e + "[0, 255].")
                r, g, b, a = c
            elif input_format == ColorModel.RGBA_STR:
                match = re.fullmatch(
                    r"#([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})", c
                )
                r, g, b, a = map(lambda x: int(x, 16), match.groups())
            elif input_format == ColorModel.HSV:
                if not (0 <= c[0] < 360 and 0 <= c[1] <= 100 and 0 <= c[2] <= 100):
                    raise ValueError(
                        input_range_e + "( [0, 360), [0, 100], [0, 100] )."
                    )
                h, s, v = c[0] / 360, c[1] / 100, c[2] / 100
                (r, g, b), a = map(lambda x: 255 * x, colorsys.hsv_to_rgb(h, s, v)), 255
        except (AttributeError, ValueError, TypeError) as e:
            # AttributeError -> re.fullmatch failed
            # ValueError     -> too many values to unpack
            # TypeError      -> in case the provided tuple is not a list of numbers
            raise ValueError(
                f"Provided input '{c}' is not in the format '{input_format}'."
            ) from e

        # Convert (r,g,b,a) to the desired output_format
        try:
            if output_format == ColorModel.ASS:
                return f"&H{round(b):02X}{round(g):02X}{round(r):02X}&"
            elif output_format == ColorModel.ASS_STYLE:
                return f"&H{round(a):02X}{round(b):02X}{round(g):02X}{round(r):02X}"
            elif output_format == ColorModel.RGB:
                method = round if round_output else float
                return tuple(map(method, (r, g, b)))
            elif output_format == ColorModel.RGB_STR:
                return f"#{round(r):02X}{round(g):02X}{round(b):02X}"
            elif output_format == ColorModel.RGBA:
                method = round if round_output else float
                return tuple(map(method, (r, g, b, a)))
            elif output_format == ColorModel.RGBA_STR:
                return f"#{round(r):02X}{round(g):02X}{round(b):02X}{round(a):02X}"
            elif output_format == ColorModel.HSV:
                method = round if round_output else float
                h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                return method(h * 360) % 360, method(s * 100), method(v * 100)
            else:
                raise ValueError(f"Unsupported output_format ('{output_format}').")
        except NameError as e:
            raise ValueError(f"Unsupported input_format ('{input_format}').") from e

    @staticmethod
    def color_ass_to_rgb(
        color_ass: str, as_str: bool = False
    ) -> Union[str, Tuple[int, int, int]]:
        """Converts from ASS color string to corresponding RGB color.

        Parameters:
            color_ass (str): A string in the format '&HBBGGRR&'.
            as_str (bool): A boolean to determine the output type format.

        Returns:
            The output represents ``color_ass`` converted. If ``as_str`` = False, the output is a tuple of integers in range *[0, 255]*.
            Else, the output is a string in the format '#RRGGBB'.

        Examples:
            ..  code-block:: python3

                print(Convert.color_ass_to_rgb("&HABCDEF&"))
                print(Convert.color_ass_to_rgb("&HABCDEF&", as_str=True))

            >>> (239, 205, 171)
            >>> "#EFCDAB"
        """
        return Convert.color(
            color_ass, ColorModel.ASS, ColorModel.RGB_STR if as_str else ColorModel.RGB
        )

    @staticmethod
    def color_ass_to_hsv(
        color_ass: str, round_output: bool = True
    ) -> Union[Tuple[int, int, int], Tuple[float, float, float]]:
        """Converts from ASS color string to corresponding HSV color.

        Parameters:
            color_ass (str): A string in the format '&HBBGGRR&'.
            round_output (bool): A boolean to determine whether the output should be rounded or not.

        Returns:
            The output represents ``color_ass`` converted. If ``round_output`` = True, the output is a tuple of integers in range *( [0, 360), [0, 100], [0, 100] )*.
            Else, the output is a tuple of floats in range *( [0, 360), [0, 100], [0, 100] )*.

        Examples:
            ..  code-block:: python3

                print(Convert.color_ass_to_hsv("&HABCDEF&"))
                print(Convert.color_ass_to_hsv("&HABCDEF&", round_output=False))

            >>> (30, 28, 94)
            >>> (30.000000000000014, 28.451882845188294, 93.72549019607843)
        """
        return Convert.color(color_ass, ColorModel.ASS, ColorModel.HSV, round_output)

    @staticmethod
    def color_rgb_to_ass(
        color_rgb: Union[
            str, Tuple[Union[int, float], Union[int, float], Union[int, float]]
        ]
    ) -> str:
        """Converts from RGB color to corresponding ASS color.

        Parameters:
            color_rgb (str or tuple of int or tuple of float): Either a string in the format '#RRGGBB' or a tuple of three integers (or floats) in the range *[0, 255]*.

        Returns:
            A string in the format '&HBBGGRR&' representing ``color_rgb`` converted.

        Examples:
            ..  code-block:: python3

                print(Convert.color_rgb_to_ass("#ABCDEF"))

            >>> "&HEFCDAB&"
        """
        return Convert.color(
            color_rgb,
            ColorModel.RGB_STR if type(color_rgb) is str else ColorModel.RGB,
            ColorModel.ASS,
        )

    @staticmethod
    def color_rgb_to_hsv(
        color_rgb: Union[
            str, Tuple[Union[int, float], Union[int, float], Union[int, float]]
        ],
        round_output: bool = True,
    ) -> Union[Tuple[int, int, int], Tuple[float, float, float]]:
        """Converts from RGB color to corresponding HSV color.

        Parameters:
            color_rgb (str or tuple of int or tuple of float): Either a string in the format '#RRGGBB' or a tuple of three integers (or floats) in the range *[0, 255]*.
            round_output (bool): A boolean to determine whether the output should be rounded or not.

        Returns:
            The output represents ``color_rgb`` converted. If ``round_output`` = True, the output is a tuple of integers in range *( [0, 360), [0, 100], [0, 100] )*.
            Else, the output is a tuple of floats in range *( [0, 360), [0, 100], [0, 100] )*.

        Examples:
            ..  code-block:: python3

                print(Convert.color_rgb_to_hsv("#ABCDEF"))
                print(Convert.color_rgb_to_hsv("#ABCDEF"), round_output=False)

            >>> (210, 28, 94)
            >>> (210.0, 28.451882845188294, 93.72549019607843)
        """
        return Convert.color(
            color_rgb,
            ColorModel.RGB_STR if type(color_rgb) is str else ColorModel.RGB,
            ColorModel.HSV,
            round_output,
        )

    @staticmethod
    def color_hsv_to_ass(
        color_hsv: Tuple[Union[int, float], Union[int, float], Union[int, float]]
    ) -> str:
        """Converts from HSV color string to corresponding ASS color.

        Parameters:
            color_hsv (tuple of int/float): A tuple of three integers (or floats) in the range *( [0, 360), [0, 100], [0, 100] )*.

        Returns:
            A string in the format '&HBBGGRR&' representing ``color_hsv`` converted.

        Examples:
            ..  code-block:: python3

                print(Convert.color_hsv_to_ass((100, 100, 100)))

            >>> "&H00FF55&"
        """
        return Convert.color(color_hsv, ColorModel.HSV, ColorModel.ASS)

    @staticmethod
    def color_hsv_to_rgb(
        color_hsv: Tuple[Union[int, float], Union[int, float], Union[int, float]],
        as_str: bool = False,
        round_output: bool = True,
    ) -> str:
        """Converts from HSV color string to corresponding RGB color.

        Parameters:
            color_hsv (tuple of int/float): A tuple of three integers (or floats) in the range *( [0, 360), [0, 100], [0, 100] )*.
            as_str (bool): A boolean to determine the output type format.
            round_output (bool): A boolean to determine whether the output should be rounded or not.

        Returns:
            The output represents ``color_hsv`` converted. If ``as_str`` = False, the output is a tuple
            ( also, if ``round_output`` = True, the output is a tuple of integers in range *( [0, 360), [0, 100], [0, 100] )*, else a tuple of float in range *( [0, 360), [0, 100], [0, 100] ) )*.
            Else, the output is a string in the format '#RRGGBB'.

        Examples:
            ..  code-block:: python3

                print(Convert.color_hsv_to_rgb((100, 100, 100)))
                print(Convert.color_hsv_to_rgb((100, 100, 100), as_str=True))
                print(Convert.color_hsv_to_rgb((100, 100, 100), round_output=False))

            >>> (85, 255, 0)
            >>> "#55FF00"
            >>> (84.99999999999999, 255.0, 0.0)
        """
        return Convert.color(
            color_hsv,
            ColorModel.HSV,
            ColorModel.RGB_STR if as_str else ColorModel.RGB,
            round_output,
        )

    @staticmethod
    def text_to_shape(
        obj: Union[Line, Word, Syllable, Char], fscx: float = None, fscy: float = None
    ) -> Shape:
        """Converts text with given style information to an ASS shape.

        **Tips:** *You can easily create impressive deforming effects.*

        Parameters:
            obj (Line, Word, Syllable or Char): An object of class Line, Word, Syllable or Char.
            fscx (float, optional): The scale_x value for the shape.
            fscy (float, optional): The scale_y value for the shape.

        Returns:
            A Shape object, representing the text with the style format values of the object.

        Examples:
            ..  code-block:: python3

                line = Line.copy(lines[1])
                line.text = "{\\\\an7\\\\pos(%.3f,%.3f)\\\\p1}%s" % (line.left, line.top, Convert.text_to_shape(line))
                io.write_line(line)
        """
        # Obtaining information and editing values of style if requested
        original_scale_x = obj.styleref.scale_x
        original_scale_y = obj.styleref.scale_y

        # Editing temporary the style to properly get the shape
        if fscx is not None:
            obj.styleref.scale_x = fscx
        if fscy is not None:
            obj.styleref.scale_y = fscy

        # Obtaining font information from style and obtaining shape
        font = Font(obj.styleref)
        shape = font.text_to_shape(obj.text)
        # Clearing resources to not let overflow errors take over
        del font

        # Restoring values of style and returning the shape converted
        if fscx is not None:
            obj.styleref.scale_x = original_scale_x
        if fscy is not None:
            obj.styleref.scale_y = original_scale_y
        return shape

    @staticmethod
    def text_to_clip(
        obj: Union[Line, Word, Syllable, Char],
        an: int = 5,
        fscx: float = None,
        fscy: float = None,
    ) -> Shape:
        """Converts text with given style information to an ASS shape, applying some translation/scaling to it since
        it is not possible to position a shape with \\pos() once it is in a clip.

        This is an high level function since it does some additional operations, check text_to_shape for further infromations.

        **Tips:** *You can easily create text masks even for growing/shrinking text without too much effort.*

        Parameters:
            obj (Line, Word, Syllable or Char): An object of class Line, Word, Syllable or Char.
            an (integer, optional): The alignment wanted for the shape.
            fscx (float, optional): The scale_x value for the shape.
            fscy (float, optional): The scale_y value for the shape.

        Returns:
            A Shape object, representing the text with the style format values of the object.

        Examples:
            ..  code-block:: python3

                line = Line.copy(lines[1])
                line.text = "{\\\\an5\\\\pos(%.3f,%.3f)\\\\clip(%s)}%s" % (line.center, line.middle, Convert.text_to_clip(line), line.text)
                io.write_line(line)
        """
        # Checking for errors
        if an < 1 or an > 9:
            raise ValueError("Alignment value must be an integer between 1 and 9")

        # Setting default values
        if fscx is None:
            fscx = obj.styleref.scale_x
        if fscy is None:
            fscy = obj.styleref.scale_y

        # Obtaining text converted to shape
        shape = Convert.text_to_shape(obj, fscx, fscy)

        # Setting mult_x based on alignment
        if an % 3 == 1:  # an=1 or an=4 or an=7
            mult_x = 0
        elif an % 3 == 2:  # an=2 or an=5 or an=8
            mult_x = 1 / 2
        else:
            mult_x = 1

        # Setting mult_y based on alignment
        if an < 4:
            mult_y = 1
        elif an < 7:
            mult_y = 1 / 2
        else:
            mult_y = 0

        # Calculating offsets
        cx = (
            obj.left
            - obj.width * mult_x * (fscx - obj.styleref.scale_x) / obj.styleref.scale_x
        )
        cy = (
            obj.top
            - obj.height * mult_y * (fscy - obj.styleref.scale_y) / obj.styleref.scale_y
        )

        return shape.move(cx, cy)

    @staticmethod
    def text_to_pixels(
        obj: Union[Line, Word, Syllable, Char], supersampling: int = 8
    ) -> List[Pixel]:
        """| Converts text with given style information to a list of pixel data.
        | A pixel data is a dictionary containing 'x' (horizontal position), 'y' (vertical position) and 'alpha' (alpha/transparency).

        It is highly suggested to create a dedicated style for pixels,
        because you will write less tags for line in your pixels, which means less size for your .ass file.

        | The style suggested is:
        | - **an=7 (very important!);**
        | - bord=0;
        | - shad=0;
        | - For Font informations leave whatever the default is;

        **Tips:** *It allows easy creation of text decaying or light effects.*

        Parameters:
            obj (Line, Word, Syllable or Char): An object of class Line, Word, Syllable or Char.
            supersampling (int): Value used for supersampling. Higher value means smoother and more precise anti-aliasing (and more computational time for generation).

        Returns:
            A list of dictionaries representing each individual pixel of the input text styled.

        Examples:
            ..  code-block:: python3

                line = lines[2].copy()
                line.style = "p"
                p_sh = Shape.rectangle()
                for pixel in Convert.text_to_pixels(line):
                    x, y = math.floor(line.left) + pixel['x'], math.floor(line.top) + pixel['y']
                    alpha = "\\alpha" + Convert.color_alpha_to_ass(pixel['alpha']) if pixel['alpha'] != 255 else ""

                    line.text = "{\\p1\\pos(%d,%d)%s}%s" % (x, y, alpha, p_sh)
                    io.write_line(line)
        """
        shape = Convert.text_to_shape(obj).move(obj.left % 1, obj.top % 1)
        return Convert.shape_to_pixels(shape, supersampling)

    @staticmethod
    def shape_to_pixels(shape: Shape, supersampling: int = 8) -> List[Pixel]:
        """| Converts a Shape object to a list of pixel data.
        | A pixel data is a dictionary containing 'x' (horizontal position), 'y' (vertical position) and 'alpha' (alpha/transparency).

        It is highly suggested to create a dedicated style for pixels,
        because you will write less tags for line in your pixels, which means less size for your .ass file.

        | The style suggested is:
        | - **an=7 (very important!);**
        | - bord=0;
        | - shad=0;
        | - For Font informations leave whatever the default is;

        **Tips:** *As for text, even shapes can decay!*

        Parameters:
            shape (Shape): An object of class Shape.
            supersampling (int): Value used for supersampling. Higher value means smoother and more precise anti-aliasing (and more computational time for generation).

        Returns:
            A list of dictionaries representing each individual pixel of the input shape.

        Examples:
            ..  code-block:: python3

                line = lines[2].copy()
                line.style = "p"
                p_sh = Shape.rectangle()
                for pixel in Convert.shape_to_pixels(Shape.heart(100)):
                    # Random circle to pixel effect just to show
                    x, y = math.floor(line.left) + pixel.x, math.floor(line.top) + pixel.y
                    alpha = "\\alpha" + Convert.color_alpha_to_ass(pixel.alpha) if pixel.alpha != 255 else ""

                    line.text = "{\\p1\\pos(%d,%d)%s\\fad(0,%d)}%s" % (x, y, alpha, l.dur/4, p_sh)
                    io.write_line(line)
        """
        # Scale values for supersampled rendering
        upscale = supersampling
        downscale = 1 / upscale

        # Upscale shape for later downsampling
        shape.map(lambda x, y: (x * upscale, y * upscale))

        # Bring shape near origin in positive room
        x1, y1, x2, y2 = shape.bounding()
        shift_x, shift_y = -1 * (x1 - x1 % upscale), -1 * (y1 - y1 % upscale)
        shape.move(shift_x, shift_y)

        # Create image
        width, height = (
            math.ceil((x2 + shift_x) * downscale) * upscale,
            math.ceil((y2 + shift_y) * downscale) * upscale,
        )
        image = [False for i in range(width * height)]

        # Renderer (on binary image with aliasing)
        lines, last_point, last_move = [], {}, {}

        def collect_lines(x, y, typ):
            # Collect lines (points + vectors)
            nonlocal lines, last_point, last_move
            x, y = int(round(x)), int(round(y))  # Use integers to avoid rounding errors

            # Move
            if typ == "m":
                # Close figure with non-horizontal line in image
                if (
                    last_move
                    and last_move["y"] != last_point["y"]
                    and not (last_point["y"] < 0 and last_move["y"] < 0)
                    and not (last_point["y"] > height and last_move["y"] > height)
                ):
                    lines.append(
                        [
                            last_point["x"],
                            last_point["y"],
                            last_move["x"] - last_point["x"],
                            last_move["y"] - last_point["y"],
                        ]
                    )

                last_move = {"x": x, "y": y}
            # Non-horizontal line in image
            elif (
                last_point
                and last_point["y"] != y
                and not (last_point["y"] < 0 and y < 0)
                and not (last_point["y"] > height and y > height)
            ):
                lines.append(
                    [
                        last_point["x"],
                        last_point["y"],
                        x - last_point["x"],
                        y - last_point["y"],
                    ]
                )

            # Remember last point
            last_point = {"x": x, "y": y}

        shape.flatten().map(collect_lines)

        # Close last figure with non-horizontal line in image
        if (
            last_move
            and last_move["y"] != last_point["y"]
            and not (last_point["y"] < 0 and last_move["y"] < 0)
            and not (last_point["y"] > height and last_move["y"] > height)
        ):
            lines.append(
                [
                    last_point["x"],
                    last_point["y"],
                    last_move["x"] - last_point["x"],
                    last_move["y"] - last_point["y"],
                ]
            )

        # Calculates line x horizontal line intersection
        def line_x_hline(x, y, vx, vy, y2):
            if vy != 0:
                s = (y2 - y) / vy
                if s >= 0 and s <= 1:
                    return x + s * vx
            return None

        # Scan image rows in shape
        _, y1, _, y2 = shape.bounding()
        for y in range(max(math.floor(y1), 0), min(math.ceil(y2), height)):
            # Collect row intersections with lines
            row_stops = []
            for line in lines:
                cx = line_x_hline(line[0], line[1], line[2], line[3], y + 0.5)
                if cx is not None:
                    row_stops.append(
                        [max(0, min(cx, width)), 1 if line[3] > 0 else -1]
                    )  # image trimmed stop position & line vertical direction

            # Enough intersections / something to render?
            if len(row_stops) > 1:
                # Sort row stops by horizontal position
                row_stops.sort(key=lambda x: x[0])
                # Render!
                status, row_index = 0, y * width
                for i in range(0, len(row_stops) - 1):
                    status = status + row_stops[i][1]
                    if status != 0:
                        for x in range(
                            math.ceil(row_stops[i][0] - 0.5),
                            math.floor(row_stops[i + 1][0] + 0.5),
                        ):
                            image[row_index + x] = True

        # Extract pixels from image
        pixels = []
        for y in range(0, height, upscale):
            for x in range(0, width, upscale):
                opacity = 0
                for yy in range(0, upscale):
                    for xx in range(0, upscale):
                        if image[(y + yy) * width + (x + xx)]:
                            opacity = opacity + 255

                if opacity > 0:
                    pixels.append(
                        Pixel(
                            x=(x - shift_x) * downscale,
                            y=(y - shift_y) * downscale,
                            alpha=round(opacity * downscale ** 2),
                        )
                    )

        return pixels

    @staticmethod
    def image_to_ass(image):
        pass

    @staticmethod
    def image_to_pixels(image):
        pass
