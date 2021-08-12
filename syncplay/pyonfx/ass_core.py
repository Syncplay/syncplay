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
import os
import sys
import time
import copy
import subprocess
from typing import List, Tuple, Union, Optional

from .font_utility import Font
from .convert import Convert


class Meta:
    """Meta object contains informations about the Ass.

    More info about each of them can be found on http://docs.aegisub.org/manual/Styles

    Attributes:
        wrap_style (int): Determines how line breaking is applied to the subtitle line
        scaled_border_and_shadow (bool): Determines if it has to be used script resolution (*True*) or video resolution (*False*) to scale border and shadow
        play_res_x (int): Video Width
        play_res_y (int): Video Height
        audio (str): Loaded audio path (absolute)
        video (str): Loaded video path (absolute)
    """

    wrap_style: int
    scaled_border_and_shadow: bool
    play_res_x: int
    play_res_y: int
    audio: str
    video: str

    def __repr__(self):
        return pretty_print(self)


class Style:
    """Style object contains a set of typographic formatting rules that is applied to dialogue lines.

    More info about styles can be found on http://docs.aegisub.org/3.2/ASS_Tags/.

    Attributes:
        fontname (str): Font name
        fontsize (float): Font size in points
        color1 (str): Primary color (fill)
        alpha1 (str): Transparency of color1
        color2 (str): Secondary color (secondary fill, for karaoke effect)
        alpha2 (str): Transparency of color2
        color3 (str): Outline (border) color
        alpha3 (str): Transparency of color3
        color4 (str): Shadow color
        alpha4 (str): Transparency of color4
        bold (bool): Font with bold
        italic (bool): Font with italic
        underline (bool): Font with underline
        strikeout (bool): Font with strikeout
        scale_x (float): Text stretching in the horizontal direction
        scale_y (float): Text stretching in the vertical direction
        spacing (float): Horizontal spacing between letters
        angle (float): Rotation of the text
        border_style (bool): *True* for opaque box, *False* for standard outline
        outline (float): Border thickness value
        shadow (float): How far downwards and to the right a shadow is drawn
        alignment (int): Alignment of the text
        margin_l (int): Distance from the left of the video frame
        margin_r (int): Distance from the right of the video frame
        margin_v (int): Distance from the bottom (or top if alignment >= 7) of the video frame
        encoding (int): Codepage used to map codepoints to glyphs
    """

    fontname: str
    fontsize: float
    color1: str
    alpha1: str
    color2: str
    alpha2: str
    color3: str
    alpha3: str
    color4: str
    alpha4: str
    bold: bool
    italic: bool
    underline: bool
    strikeout: bool
    scale_x: float
    scale_y: float
    spacing: float
    angle: float
    border_style: bool
    outline: float
    shadow: float
    alignment: int
    margin_l: int
    margin_r: int
    margin_v: int
    encoding: int

    def __repr__(self):
        return pretty_print(self)


class Char:
    """Char object contains informations about a single char of a line in the Ass.

    A char is defined by some text between two karaoke tags (k, ko, kf).

    Attributes:
        i (int): Char index number
        word_i (int): Char word index (e.g.: In line text ``Hello PyonFX users!``, letter "u" will have word_i=2).
        syl_i (int): Char syl index (e.g.: In line text ``{\\k0}Hel{\\k0}lo {\\k0}Pyon{\\k0}FX {\\k0}users!``, letter "F" will have syl_i=3).
        syl_char_i (int): Char invidual syl index (e.g.: In line text ``{\\k0}Hel{\\k0}lo {\\k0}Pyon{\\k0}FX {\\k0}users!``, letter "e" of "users" will have syl_char_i=2).
        start_time (int): Char start time (in milliseconds).
        end_time (int): Char end time (in milliseconds).
        duration (int): Char duration (in milliseconds).
        styleref (obj): Reference to the Style object of this object original line.
        text (str): Char text.
        inline_fx (str): Char inline effect (marked as \\-EFFECT in karaoke-time).
        prespace (int): Char free space before text.
        postspace (int): Char free space after text.
        width (float): Char text width.
        height (float): Char text height.
        x (float): Char text position horizontal (depends on alignment).
        y (float): Char text position vertical (depends on alignment).
        left (float): Char text position left.
        center (float): Char text position center.
        right (float): Char text position right.
        top (float): Char text position top.
        middle (float): Char text position middle.
        bottom (float): Char text position bottom.
    """

    i: int
    word_i: int
    syl_i: int
    syl_char_i: int
    start_time: int
    end_time: int
    duration: int
    styleref: Style
    text: str
    inline_fx: str
    prespace: int
    postspace: int
    width: float
    height: float
    x: float
    y: float
    left: float
    center: float
    right: float
    top: float
    middle: float
    bottom: float

    def __repr__(self):
        return pretty_print(self)


class Syllable:
    """Syllable object contains informations about a single syl of a line in the Ass.

    A syl can be defined as some text after a karaoke tag (k, ko, kf)
    (e.g.: In ``{\\k0}Hel{\\k0}lo {\\k0}Pyon{\\k0}FX {\\k0}users!``, "Pyon" and "FX" are distinct syllables),

    Attributes:
        i (int): Syllable index number
        word_i (int): Syllable word index (e.g.: In line text ``{\\k0}Hel{\\k0}lo {\\k0}Pyon{\\k0}FX {\\k0}users!``, syl "Pyon" will have word_i=1).
        start_time (int): Syllable start time (in milliseconds).
        end_time (int): Syllable end time (in milliseconds).
        duration (int): Syllable duration (in milliseconds).
        styleref (obj): Reference to the Style object of this object original line.
        text (str): Syllable text.
        tags (str): All the remaining tags before syl text apart \\k ones.
        inline_fx (str): Syllable inline effect (marked as \\-EFFECT in karaoke-time).
        prespace (int): Syllable free space before text.
        postspace (int): Syllable free space after text.
        width (float): Syllable text width.
        height (float): Syllable text height.
        x (float): Syllable text position horizontal (depends on alignment).
        y (float): Syllable text position vertical (depends on alignment).
        left (float): Syllable text position left.
        center (float): Syllable text position center.
        right (float): Syllable text position right.
        top (float): Syllable text position top.
        middle (float): Syllable text position middle.
        bottom (float): Syllable text position bottom.
    """

    i: int
    word_i: int
    start_time: int
    end_time: int
    duration: int
    styleref: Style
    text: str
    tags: str
    inline_fx: str
    prespace: int
    postspace: int
    width: float
    height: float
    x: float
    y: float
    left: float
    center: float
    right: float
    top: float
    middle: float
    bottom: float

    def __repr__(self):
        return pretty_print(self)


class Word:
    """Word object contains informations about a single word of a line in the Ass.

    A word can be defined as some text with some optional space before or after
    (e.g.: In the string "What a beautiful world!", "beautiful" and "world" are both distinct words).

    Attributes:
        i (int): Word index number
        start_time (int): Word start time (same as line start time) (in milliseconds).
        end_time (int): Word end time (same as line end time) (in milliseconds).
        duration (int): Word duration (same as line duration) (in milliseconds).
        styleref (obj): Reference to the Style object of this object original line.
        text (str): Word text.
        prespace (int): Word free space before text.
        postspace (int): Word free space after text.
        width (float): Word text width.
        height (float): Word text height.
        x (float): Word text position horizontal (depends on alignment).
        y (float): Word text position vertical (depends on alignment).
        left (float): Word text position left.
        center (float): Word text position center.
        right (float): Word text position right.
        top (float): Word text position top.
        middle (float): Word text position middle.
        bottom (float): Word text position bottom.
    """

    i: int
    start_time: int
    end_time: int
    duration: int
    styleref: Style
    text: str
    prespace: int
    postspace: int
    width: float
    height: float
    x: float
    y: float
    left: float
    center: float
    right: float
    top: float
    middle: float
    bottom: float

    def __repr__(self):
        return pretty_print(self)


class Line:
    """Line object contains informations about a single line in the Ass.

    Note:
        (*) = This field is available only if :class:`extended<Ass>` = True

    Attributes:
        i (int): Line index number
        comment (bool): If *True*, this line will not be displayed on the screen.
        layer (int): Layer for the line. Higher layer numbers are drawn on top of lower ones.
        start_time (int): Line start time (in milliseconds).
        end_time (int): Line end time (in milliseconds).
        duration (int): Line duration (in milliseconds) (*).
        leadin (float): Time between this line and the previous one (in milliseconds; first line = 1000.1) (*).
        leadout (float): Time between this line and the next one (in milliseconds; first line = 1000.1) (*).
        style (str): Style name used for this line.
        styleref (obj): Reference to the Style object of this line (*).
        actor (str): Actor field.
        margin_l (int): Left margin for this line.
        margin_r (int): Right margin for this line.
        margin_v (int): Vertical margin for this line.
        effect (str): Effect field.
        raw_text (str): Line raw text.
        text (str): Line stripped text (no tags).
        width (float): Line text width (*).
        height (float): Line text height (*).
        ascent (float): Line font ascent (*).
        descent (float): Line font descent (*).
        internal_leading (float): Line font internal lead (*).
        external_leading (float): Line font external lead (*).
        x (float): Line text position horizontal (depends on alignment) (*).
        y (float): Line text position vertical (depends on alignment) (*).
        left (float): Line text position left (*).
        center (float): Line text position center (*).
        right (float): Line text position right (*).
        top (float): Line text position top (*).
        middle (float): Line text position middle (*).
        bottom (float): Line text position bottom (*).
        words (list): List containing objects :class:`Word` in this line (*).
        syls (list): List containing objects :class:`Syllable` in this line (if available) (*).
        chars (list): List containing objects :class:`Char` in this line (*).
    """

    i: int
    comment: bool
    layer: int
    start_time: int
    end_time: int
    duration: int
    leadin: float
    leadout: float
    style: str
    styleref: Style
    actor: str
    margin_l: int
    margin_r: int
    margin_v: int
    effect: str
    raw_text: str
    text: str
    width: float
    height: float
    ascent: float
    descent: float
    internal_leading: float
    external_leading: float
    x: float
    y: float
    left: float
    center: float
    right: float
    top: float
    middle: float
    bottom: float
    words: List[Word]
    syls: List[Syllable]
    chars: List[Char]

    def __repr__(self):
        return pretty_print(self)

    def copy(self) -> Line:
        """
        Returns:
            A deep copy of this object (line)
        """
        return copy.deepcopy(self)


class Ass:
    """Contains all the informations about a file in the ASS format and the methods to work with it for both input and output.

    | Usually you will create an Ass object and use it for input and output (see example_ section).
    | PyonFX set automatically an absolute path for all the info in the output, so that wherever you will
      put your generated file, it should always load correctly video and audio.

    Args:
        path_input (str): Path for the input file (either relative to your .py file or absolute).
        path_output (str): Path for the output file (either relative to your .py file or absolute) (DEFAULT: "Output.ass").
        keep_original (bool): If True, you will find all the lines of the input file commented before the new lines generated.
        extended (bool): Calculate more informations from lines (usually you will not have to touch this).
        vertical_kanji (bool): If True, line text with alignment 4, 5 or 6 will be positioned vertically.
            Additionally, ``line`` fields will be re-calculated based on the re-positioned ``line.chars``.

    Attributes:
        path_input (str): Path for input file (absolute). If none create default from scratch like in aegisub Untitled.ass
        path_output (str): Path for output file (absolute).
        meta (:class:`Meta`): Contains informations about the ASS given.
        styles (list of :class:`Style`): Contains all the styles in the ASS given.
        lines (list of :class:`Line`): Contains all the lines (events) in the ASS given.

    .. _example:
    Example:
        ..  code-block:: python3

            io = Ass ("in.ass")
            meta, styles, lines = io.get_data()
    """

    def __init__( self,
        path_input: str = "",
        path_output: str = "Output.ass",
        keep_original: bool = True,
        extended: bool = True,
        vertical_kanji: bool = False,):
        # Starting to take process time
            self.__saved = False
            self.__plines = 0
            self.__ptime = time.time()
            self.meta, self.styles, self.lines = Meta(), {}, []

            #if(path_input != ""):
            #    print("Warning path input is ignored, please use input() or load()")
            #self.input(path_input)

            self.__output = []
            self.__output_extradata = []

            self.parse_ass(path_input, path_output,  keep_original, extended, vertical_kanji)

    def set_input(self, path_input)   :
        """
           Allow to set the input file
           Args:
             path_input (str): Path for the input file (either relative to your .py file or absolute).
         """
        section_pattern = re.compile(r"^\[Script Info\]")
        if(path_input == ""):
                #Use aesisub default template
                path_input=os.path.join(os.path.dirname(os.path.abspath(__file__)),"Untitled.ass")
        elif section_pattern.match(path_input):
                #path input is an ass valid content
                 pass
        else:
                # Getting absolute sub file path
                dirname = os.path.dirname(os.path.abspath(sys.argv[0]))

                if(re.search("\.(ass|ssa|jass|jsos)$",path_input)):
                    if not os.path.isabs(path_input):
                        path_input = os.path.join(dirname, path_input)

                    # Checking sub file validity (does it exists?)
                    if not os.path.isfile(path_input):
                        raise FileNotFoundError(
                            "Invalid path for the Subtitle file: %s" % path_input
                        )
                else:
                    raise FileNotFoundError(
                        "Invalid input for the Subtitle file"
                    )
        self.path_input = path_input

    def set_output(self, path_output)   :
        """
             Allow to set the output file
             Args:
                     path_output (str): Path for the output file (either relative to your .py file or absolute)
         """
        # Getting absolute sub file path
        dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
        # Getting absolute output file path
        if path_output == "Output.ass" or path_output == "Untitled.ass":
            path_output = os.path.join(dirname, path_output)
        elif not os.path.isabs(path_output):
            path_output = os.path.join(dirname, path_output)

        self.path_output = path_output
    
    def parse_ass(
        self,
        path_input: str = "",
        path_output: str = "Output.ass",
        keep_original: bool = True,
        extended: bool = True,
        vertical_kanji: bool = False,
    ):
        """
             Parse an input ASS file using its path
        Args:
            path_input (str): Path for the input file (either relative to your .py file or absolute).
            path_output (str): Path for the output file (either relative to your .py file or absolute) (DEFAULT: "Output.ass").
            keep_original (bool): If True, you will find all the lines of the input file commented before the new lines generated.
            extended (bool): Calculate more informations from lines (usually you will not have to touch this).
            vertical_kanji (bool): If True, line text with alignment 4, 5 or 6 will be positioned vertically.
                Additionally, ``line`` fields will be re-calculated based on the re-positioned ``line.chars``.

        Attributes:
            path_input (str): Path for input file (absolute). If none create default from scratch like in aegisub Untitled.ass
            path_output (str): Path for output file (absolute).
            meta (:class:`Meta`): Contains informations about the ASS given.
            styles (list of :class:`Style`): Contains all the styles in the ASS given.
            lines (list of :class:`Line`): Contains all the lines (events) in the ASS given.

        .. _example:
        Example:
            ..  code-block:: python3

                io = Ass ("in.ass")
                meta, styles, lines = io.get_data()
         """
        # Starting to take process time
        self.__saved = False
        self.__plines = 0
        self.__ptime = time.time()

        self.meta, self.styles, self.lines = Meta(), {}, []

        content=""
        section_pattern = re.compile(r"^\[Script Info\]")
        if(section_pattern.match(path_input)):
            # input is a content
            content = path_input
        elif(path_input ==""):
            dirname = os.path.dirname(__file__)
            path_input  = os.path.join(dirname, "Untitled.ass")
        else:
            # input is a path file
            self.set_input(path_input)
            path_input =self.path_input

        self.set_output(path_output)

        self.__output = []
        self.__output_extradata = []

        section = ""
        li = 0

        #Get the stream of content or file content
        if(content):
            from io import StringIO
            stream = StringIO(content)
        else:
            try:
                stream = open(path_input, "r", encoding="utf-8-sig")
            except FileNotFoundError:
                raise FileNotFoundError(
                    "Unsupported or broken subtitle file: '%s'" % path_input
                )
            #previous read set the cursor at the end, put it back at the start
            stream.seek(0,0)
        for line in stream:
            # Getting section
            section_pattern = re.compile(r"^\[([^\]]*)")
            if section_pattern.match(line):
                # Updating section
                section = section_pattern.match(line)[1]
                # Appending line to output
                if section != "Aegisub Extradata":
                    self.__output.append(line)

            # Parsing Meta data
            elif section == "Script Info" or section == "Aegisub Project Garbage":
                # Internal function that tries to get the absolute path for media files in meta
                def get_media_abs_path(mediafile):
                    # If this is not a dummy video, let's try to get the absolute path for the video
                    if not mediafile.startswith("?dummy"):
                        tmp = mediafile
                        media_dir = os.path.dirname(self.path_input)

                        while mediafile.startswith("../"):
                            media_dir = os.path.dirname(media_dir)
                            mediafile = mediafile[3:]

                        mediafile = os.path.normpath(
                            "%s%s%s" % (media_dir, os.sep, mediafile)
                        )

                        if not os.path.isfile(mediafile):
                            mediafile = tmp

                    return mediafile

                # Switch
                if re.match(r"WrapStyle: *?(\d+)$", line):
                    self.meta.wrap_style = int(line[11:].strip())
                elif re.match(r"ScaledBorderAndShadow: *?(.+)$", line):
                    self.meta.scaled_border_and_shadow = line[23:].strip() == "yes"
                elif re.match(r"PlayResX: *?(\d+)$", line):
                    self.meta.play_res_x = int(line[10:].strip())
                elif re.match(r"PlayResY: *?(\d+)$", line):
                    self.meta.play_res_y = int(line[10:].strip())
                elif re.match(r"Audio File: *?(.*)$", line):
                    self.meta.audio = get_media_abs_path(line[11:].strip())
                    line = "Audio File: %s\n" % self.meta.audio
                elif re.match(r"Video File: *?(.*)$", line):
                    self.meta.video = get_media_abs_path(line[11:].strip())
                    line = "Video File: %s\n" % self.meta.video

                # Appending line to output
                self.__output.append(line)

            # Parsing Styles
            elif section == "V4+ Styles":
                # Appending line to output
                self.__output.append(line)
                style = re.match(r"Style: (.+?)$", line)

                if style:
                    # Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour,
                    # Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,
                    # BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
                    style = [el for el in style[1].split(",")]
                    tmp = Style()

                    tmp.fontname = style[1]
                    tmp.fontsize = float(style[2])

                    tmp.color1, tmp.alpha1 = f"&H{style[3][4:]}&", f"{style[3][:4]}&"
                    tmp.color2, tmp.alpha2 = f"&H{style[4][4:]}&", f"{style[4][:4]}&"
                    tmp.color3, tmp.alpha3 = f"&H{style[5][4:]}&", f"{style[5][:4]}&"
                    tmp.color4, tmp.alpha4 = f"&H{style[6][4:]}&", f"{style[6][:4]}&"

                    tmp.bold = style[7] == "-1"
                    tmp.italic = style[8] == "-1"
                    tmp.underline = style[9] == "-1"
                    tmp.strikeout = style[10] == "-1"

                    tmp.scale_x = float(style[11])
                    tmp.scale_y = float(style[12])

                    tmp.spacing = float(style[13])
                    tmp.angle = float(style[14])

                    tmp.border_style = style[15] == "3"
                    tmp.outline = float(style[16])
                    tmp.shadow = float(style[17])

                    tmp.alignment = int(style[18])
                    tmp.margin_l = int(style[19])
                    tmp.margin_r = int(style[20])
                    tmp.margin_v = int(style[21])

                    tmp.encoding = int(style[22])

                    self.styles[style[0]] = tmp

            # Parsing Dialogues
            elif section == "Events":
                # Appending line to output (commented) if keep_original is True
                if keep_original:
                    self.__output.append(
                        re.sub(r"^(Dialogue|Comment):", "Comment:", line, count=1)
                    )
                elif line.startswith("Format"):
                    self.__output.append(line.strip())

                # Analyzing line
                line = re.match(r"(Dialogue|Comment): (.+?)$", line)

                if line:
                    # Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
                    tmp = Line()

                    tmp.i = li
                    li += 1

                    tmp.comment = line[1] == "Comment"
                    line = [el for el in line[2].split(",")]

                    tmp.layer = int(line[0])

                    tmp.start_time = Convert.time(line[1])
                    tmp.end_time = Convert.time(line[2])

                    tmp.style = line[3]
                    tmp.actor = line[4]

                    tmp.margin_l = int(line[5])
                    tmp.margin_r = int(line[6])
                    tmp.margin_v = int(line[7])

                    tmp.effect = line[8]

                    tmp.raw_text = ",".join(line[9:])

                    self.lines.append(tmp)

            elif section == "Aegisub Extradata":
                self.__output_extradata.append(line)

            else:
                raise ValueError(f"Unexpected section in the input file: [{section}]")

        # Adding informations to lines and meta?
        if not extended:
            return None
        else:
            return self.add_pyonfx_extension()

    def add_pyonfx_extension(self):
        """
        Calculate more informations from lines ( this affects the lines only if play_res_x and play_res_y are provided in the Script info section).
        Args: None
        return None
        """
        #security check if no video provided, abort calculations
        if (not hasattr(self.meta,"play_res_x") or not hasattr(self.meta,"play_res_y")):
            return None
        lines_by_styles = {}
        # Let the fun begin (Pyon!)
        for li, line in enumerate(self.lines):
            try:
                line.styleref = self.styles[line.style]
            except KeyError:
                line.styleref = None

            # Append dialog to styles (for leadin and leadout later)
            if line.style not in lines_by_styles:
                lines_by_styles[line.style] = []
            lines_by_styles[line.style].append(line)

            line.duration = line.end_time - line.start_time
            line.text = re.sub(r"\{.*?\}", "", line.raw_text)

            # Add dialog text sizes and positions (if possible)
            if line.styleref:
                # Creating a Font object and saving return values of font.get_metrics() for the future
                font = Font(line.styleref)
                font_metrics = font.get_metrics()

                line.width, line.height = font.get_text_extents(line.text)
                (
                    line.ascent,
                    line.descent,
                    line.internal_leading,
                    line.external_leading,
                ) = font_metrics

                if self.meta.play_res_x > 0 and self.meta.play_res_y > 0:
                    # Horizontal position
                    tmp_margin_l = (
                        line.margin_l if line.margin_l != 0 else line.styleref.margin_l
                    )
                    tmp_margin_r = (
                        line.margin_r if line.margin_r != 0 else line.styleref.margin_r
                    )

                    if (line.styleref.alignment - 1) % 3 == 0:
                        line.left = tmp_margin_l
                        line.center = line.left + line.width / 2
                        line.right = line.left + line.width
                        line.x = line.left
                    elif (line.styleref.alignment - 2) % 3 == 0:
                        line.left = (
                            self.meta.play_res_x / 2
                            - line.width / 2
                            + tmp_margin_l / 2
                            - tmp_margin_r / 2
                        )
                        line.center = line.left + line.width / 2
                        line.right = line.left + line.width
                        line.x = line.center
                    else:
                        line.left = self.meta.play_res_x - tmp_margin_r - line.width
                        line.center = line.left + line.width / 2
                        line.right = line.left + line.width
                        line.x = line.right

                    # Vertical position
                    if line.styleref.alignment > 6:
                        line.top = (
                            line.margin_v
                            if line.margin_v != 0
                            else line.styleref.margin_v
                        )
                        line.middle = line.top + line.height / 2
                        line.bottom = line.top + line.height
                        line.y = line.top
                    elif line.styleref.alignment > 3:
                        line.top = self.meta.play_res_y / 2 - line.height / 2
                        line.middle = line.top + line.height / 2
                        line.bottom = line.top + line.height
                        line.y = line.middle
                    else:
                        line.top = (
                            self.meta.play_res_y
                            - (
                                line.margin_v
                                if line.margin_v != 0
                                else line.styleref.margin_v
                            )
                            - line.height
                        )
                        line.middle = line.top + line.height / 2
                        line.bottom = line.top + line.height
                        line.y = line.bottom

                # Calculating space width and saving spacing
                space_width = font.get_text_extents(" ")[0]
                style_spacing = line.styleref.spacing

                # Adding words
                line.words = []

                wi = 0
                for prespace, word_text, postspace in re.findall(
                    r"(\s*)([^\s]+)(\s*)", line.text
                ):
                    word = Word()

                    word.i = wi
                    wi += 1

                    word.start_time = line.start_time
                    word.end_time = line.end_time
                    word.duration = line.duration

                    word.styleref = line.styleref
                    word.text = word_text

                    word.prespace = len(prespace)
                    word.postspace = len(postspace)

                    word.width, word.height = font.get_text_extents(word.text)
                    (
                        word.ascent,
                        word.descent,
                        word.internal_leading,
                        word.external_leading,
                    ) = font_metrics

                    line.words.append(word)

                # Calculate word positions with all words data already available
                if line.words and self.meta.play_res_x > 0 and self.meta.play_res_y > 0:
                    if line.styleref.alignment > 6 or line.styleref.alignment < 4:
                        cur_x = line.left
                        for word in line.words:
                            # Horizontal position
                            cur_x = cur_x + word.prespace * (
                                space_width + style_spacing
                            )

                            word.left = cur_x
                            word.center = word.left + word.width / 2
                            word.right = word.left + word.width

                            if (line.styleref.alignment - 1) % 3 == 0:
                                word.x = word.left
                            elif (line.styleref.alignment - 2) % 3 == 0:
                                word.x = word.center
                            else:
                                word.x = word.right

                            # Vertical position
                            word.top = line.top
                            word.middle = line.middle
                            word.bottom = line.bottom
                            word.y = line.y

                            # Updating cur_x
                            cur_x = (
                                cur_x
                                + word.width
                                + word.postspace * (space_width + style_spacing)
                                + style_spacing
                            )
                    else:
                        max_width, sum_height = 0, 0
                        for word in line.words:
                            max_width = max(max_width, word.width)
                            sum_height = sum_height + word.height

                        cur_y = x_fix = self.meta.play_res_y / 2 - sum_height / 2
                        for word in line.words:
                            # Horizontal position
                            x_fix = (max_width - word.width) / 2

                            if line.styleref.alignment == 4:
                                word.left = line.left + x_fix
                                word.center = word.left + word.width / 2
                                word.right = word.left + word.width
                                word.x = word.left
                            elif line.styleref.alignment == 5:
                                word.left = self.meta.play_res_x / 2 - word.width / 2
                                word.center = word.left + word.width / 2
                                word.right = word.left + word.width
                                word.x = word.center
                            else:
                                word.left = line.right - word.width - x_fix
                                word.center = word.left + word.width / 2
                                word.right = word.left + word.width
                                word.x = word.right

                            # Vertical position
                            word.top = cur_y
                            word.middle = word.top + word.height / 2
                            word.bottom = word.top + word.height
                            word.y = word.middle
                            cur_y = cur_y + word.height

                # Search for dialog's text chunks, to later create syllables
                # A text chunk is a text with one or more {tags} preceding it
                # Tags can be some text or empty string
                text_chunks = []
                tag_pattern = re.compile(r"(\{.*?\})+")
                tag = tag_pattern.search(line.raw_text)
                word_i = 0

                if not tag:
                    # No tags found
                    text_chunks.append({"tags": "", "text": line.raw_text})
                else:
                    # First chunk without tags?
                    if tag.start() != 0:
                        text_chunks.append(
                            {"tags": "", "text": line.raw_text[0 : tag.start()]}
                        )

                    # Searching for other tags
                    while True:
                        next_tag = tag_pattern.search(line.raw_text, tag.end())
                        tmp = {
                            # Note that we're removing possibles '}{' caused by consecutive tags
                            "tags": line.raw_text[
                                tag.start() + 1 : tag.end() - 1
                            ].replace("}{", ""),
                            "text": line.raw_text[
                                tag.end() : (next_tag.start() if next_tag else None)
                            ],
                            "word_i": word_i,
                        }
                        text_chunks.append(tmp)

                        # If there are some spaces after text, then we're at the end of the current word
                        if re.match(r"(.*?)(\s+)$", tmp["text"]):
                            word_i = word_i + 1

                        if not next_tag:
                            break
                        tag = next_tag

                # Adding syls
                si = 0
                last_time = 0
                inline_fx = ""
                syl_tags_pattern = re.compile(r"(.*?)\\[kK][of]?(\d+)(.*)")

                line.syls = []
                for tc in text_chunks:
                    # If we don't have at least one \k tag, everything is invalid
                    if not syl_tags_pattern.match(tc["tags"]):
                        line.syls.clear()
                        break

                    posttags = tc["tags"]
                    syls_in_text_chunk = []
                    while True:
                        # Are there \k in posttags?
                        tags_syl = syl_tags_pattern.match(posttags)

                        if not tags_syl:
                            # Append all the temporary syls, except last one
                            for syl in syls_in_text_chunk[:-1]:
                                curr_inline_fx = re.search(r"\\\-([^\\]+)", syl.tags)
                                if curr_inline_fx:
                                    inline_fx = curr_inline_fx[1]
                                syl.inline_fx = inline_fx

                                # Hidden syls are treated like empty syls
                                syl.prespace, syl.text, syl.postspace = 0, "", 0

                                syl.width, syl.height = font.get_text_extents("")
                                (
                                    syl.ascent,
                                    syl.descent,
                                    syl.internal_leading,
                                    syl.external_leading,
                                ) = font_metrics

                                line.syls.append(syl)

                            # Append last syl
                            syl = syls_in_text_chunk[-1]
                            syl.tags += posttags

                            curr_inline_fx = re.search(r"\\\-([^\\]+)", syl.tags)
                            if curr_inline_fx:
                                inline_fx = curr_inline_fx[1]
                            syl.inline_fx = inline_fx

                            if tc["text"].isspace():
                                syl.prespace, syl.text, syl.postspace = 0, tc["text"], 0
                            else:
                                syl.prespace, syl.text, syl.postspace = re.match(
                                    r"(\s*)(.*?)(\s*)$", tc["text"]
                                ).groups()
                                syl.prespace, syl.postspace = (
                                    len(syl.prespace),
                                    len(syl.postspace),
                                )

                            syl.width, syl.height = font.get_text_extents(syl.text)
                            (
                                syl.ascent,
                                syl.descent,
                                syl.internal_leading,
                                syl.external_leading,
                            ) = font_metrics

                            line.syls.append(syl)
                            break

                        pretags, kdur, posttags = tags_syl.groups()

                        # Create a Syllable object
                        syl = Syllable()

                        syl.start_time = last_time
                        syl.end_time = last_time + int(kdur) * 10
                        syl.duration = int(kdur) * 10

                        syl.styleref = line.styleref
                        syl.tags = pretags

                        syl.i = si
                        syl.word_i = tc["word_i"]

                        syls_in_text_chunk.append(syl)

                        # Update working variable
                        si += 1
                        last_time = syl.end_time

                # Calculate syllables positions with all syllables data already available
                if line.syls and self.meta.play_res_x > 0 and self.meta.play_res_y > 0:
                    if (
                        line.styleref.alignment > 6
                        or line.styleref.alignment < 4
                        or not vertical_kanji
                    ):
                        cur_x = line.left
                        for syl in line.syls:
                            cur_x = cur_x + syl.prespace * (space_width + style_spacing)
                            # Horizontal position
                            syl.left = cur_x
                            syl.center = syl.left + syl.width / 2
                            syl.right = syl.left + syl.width

                            if (line.styleref.alignment - 1) % 3 == 0:
                                syl.x = syl.left
                            elif (line.styleref.alignment - 2) % 3 == 0:
                                syl.x = syl.center
                            else:
                                syl.x = syl.right

                            cur_x = (
                                cur_x
                                + syl.width
                                + syl.postspace * (space_width + style_spacing)
                                + style_spacing
                            )

                            # Vertical position
                            syl.top = line.top
                            syl.middle = line.middle
                            syl.bottom = line.bottom
                            syl.y = line.y

                    else:  # Kanji vertical position
                        max_width, sum_height = 0, 0
                        for syl in line.syls:
                            max_width = max(max_width, syl.width)
                            sum_height = sum_height + syl.height

                        cur_y = self.meta.play_res_y / 2 - sum_height / 2

                        for syl in line.syls:
                            # Horizontal position
                            x_fix = (max_width - syl.width) / 2
                            if line.styleref.alignment == 4:
                                syl.left = line.left + x_fix
                                syl.center = syl.left + syl.width / 2
                                syl.right = syl.left + syl.width
                                syl.x = syl.left
                            elif line.styleref.alignment == 5:
                                syl.left = line.center - syl.width / 2
                                syl.center = syl.left + syl.width / 2
                                syl.right = syl.left + syl.width
                                syl.x = syl.center
                            else:
                                syl.left = line.right - syl.width - x_fix
                                syl.center = syl.left + syl.width / 2
                                syl.right = syl.left + syl.width
                                syl.x = syl.right

                            # Vertical position
                            syl.top = cur_y
                            syl.middle = syl.top + syl.height / 2
                            syl.bottom = syl.top + syl.height
                            syl.y = syl.middle
                            cur_y = cur_y + syl.height

                # Adding chars
                line.chars = []

                # If we have syls in line, we prefert to work with them to provide more informations
                if line.syls:
                    words_or_syls = line.syls
                else:
                    words_or_syls = line.words

                # Getting chars
                char_index = 0
                for el in words_or_syls:
                    el_text = "{}{}{}".format(
                        " " * el.prespace, el.text, " " * el.postspace
                    )
                    for ci, char_text in enumerate(list(el_text)):
                        char = Char()
                        char.i = ci

                        # If we're working with syls, we can add some indexes
                        char.i = char_index
                        char_index += 1
                        if line.syls:
                            char.word_i = el.word_i
                            char.syl_i = el.i
                            char.syl_char_i = ci
                        else:
                            char.word_i = el.i

                        # Adding last fields based on the existance of syls or not
                        char.start_time = el.start_time
                        char.end_time = el.end_time
                        char.duration = el.duration

                        char.styleref = line.styleref
                        char.text = char_text

                        char.width, char.height = font.get_text_extents(char.text)
                        (
                            char.ascent,
                            char.descent,
                            char.internal_leading,
                            char.external_leading,
                        ) = font_metrics

                        line.chars.append(char)

                # Calculate character positions with all characters data already available
                if line.chars and self.meta.play_res_x > 0 and self.meta.play_res_y > 0:
                    if (
                        line.styleref.alignment > 6
                        or line.styleref.alignment < 4
                        or not vertical_kanji
                    ):
                        cur_x = line.left
                        for char in line.chars:
                            # Horizontal position
                            char.left = cur_x
                            char.center = char.left + char.width / 2
                            char.right = char.left + char.width

                            if (line.styleref.alignment - 1) % 3 == 0:
                                char.x = char.left
                            elif (line.styleref.alignment - 2) % 3 == 0:
                                char.x = char.center
                            else:
                                char.x = char.right

                            cur_x = cur_x + char.width + style_spacing

                            # Vertical position
                            char.top = line.top
                            char.middle = line.middle
                            char.bottom = line.bottom
                            char.y = line.y
                    else:
                        max_width, sum_height = 0, 0
                        for char in line.chars:
                            max_width = max(max_width, char.width)
                            sum_height = sum_height + char.height

                        cur_y = x_fix = self.meta.play_res_y / 2 - sum_height / 2

                        # Fixing line positions
                        line.top = cur_y
                        line.middle = self.meta.play_res_y / 2
                        line.bottom = line.top + sum_height
                        line.width = max_width
                        line.height = sum_height
                        if line.styleref.alignment == 4:
                            line.center = line.left + max_width / 2
                            line.right = line.left + max_width
                        elif line.styleref.alignment == 5:
                            line.left = line.center - max_width / 2
                            line.right = line.left + max_width
                        else:
                            line.left = line.right - max_width
                            line.center = line.left + max_width / 2

                        for char in line.chars:
                            # Horizontal position
                            x_fix = (max_width - char.width) / 2
                            if line.styleref.alignment == 4:
                                char.left = line.left + x_fix
                                char.center = char.left + char.width / 2
                                char.right = char.left + char.width
                                char.x = char.left
                            elif line.styleref.alignment == 5:
                                char.left = self.meta.play_res_x / 2 - char.width / 2
                                char.center = char.left + char.width / 2
                                char.right = char.left + char.width
                                char.x = char.center
                            else:
                                char.left = line.right - char.width - x_fix
                                char.center = char.left + char.width / 2
                                char.right = char.left + char.width
                                char.x = char.right

                            # Vertical position
                            char.top = cur_y
                            char.middle = char.top + char.height / 2
                            char.bottom = char.top + char.height
                            char.y = char.middle
                            cur_y = cur_y + char.height

        # Add durations between dialogs
        for style in lines_by_styles:
            lines_by_styles[style].sort(key=lambda x: x.start_time)
            for li, line in enumerate(lines_by_styles[style]):
                line.leadin = (
                    1000.1
                    if li == 0
                    else line.start_time - lines_by_styles[style][li - 1].end_time
                )
                line.leadout = (
                    1000.1
                    if li == len(lines_by_styles[style]) - 1
                    else lines_by_styles[style][li + 1].start_time - line.end_time
                )

    def get_data(self) -> Tuple[Meta, Style, List[Line]]:
        """Utility function to retrieve easily meta styles and lines.

            Returns:
                :attr:`meta`, :attr:`styles` and :attr:`lines`
        """
        return self.meta, self.styles, self.lines
        
    def del_line(self,no):
        """Delete a line of the output list (which is private) """
        nb=-1
        
        # Retrieve the index of the first line, this is ugly having to do so
        #as is if we could'nt rectify self.lines instead and generate self.__output on save()
        # in lua this is what has been done when you get the aegisub object
        for li, line in enumerate(self.__output):
            if  re.match(r"\n?(Dialogue|Comment): (.+?)$", line):
                nb=li-1
                break;
    
        if (nb >=0) and isinstance(self.__output[no+nb], str):
            del self.__output[no+nb]
            self.__plines -= 1
        else:
            raise TypeError("No Line %d exists"  % no)

    def write_line(self, line: Line) -> Optional[TypeError]:
        """Appends a line to the output list (which is private) that later on will be written to the output file when calling save().

        Use it whenever you've prepared a line, it will not impact performance since you
        will not actually write anything until :func:`save` will be called.

        Parameters:
            line (:class:`Line`): A line object. If not valid, TypeError is raised.
        """
        if isinstance(line, Line):
            self.__output.append(
                "\n%s: %d,%s,%s,%s,%s,%04d,%04d,%04d,%s,%s"
                % (
                    "Comment" if line.comment else "Dialogue",
                    line.layer,
                    Convert.time(max(0, int(line.start_time))),
                    Convert.time(max(0, int(line.end_time))),
                    line.style,
                    line.actor,
                    line.margin_l,
                    line.margin_r,
                    line.margin_v,
                    line.effect,
                    line.text,
                )
            )
            self.__plines += 1
        else:
            raise TypeError("Expected Line object, got %s." % type(line))

    def save(self, quiet: bool = False) -> None:
        """Write everything inside the private output list to a file.

        Parameters:
            quiet (bool): If True, you will not get printed any message.
        """

        # Writing to file
        with open(self.path_output, "w", encoding="utf-8-sig") as f:
            f.writelines(self.__output + ["\n"])
            if self.__output_extradata:
                f.write("\n[Aegisub Extradata]\n")
                f.writelines(self.__output_extradata)

        self.__saved = True

        if not quiet:
            print(
                "Produced lines: %d\nProcess duration (in seconds): %.3f"
                % (self.__plines, time.time() - self.__ptime)
            )

    def open_aegisub(self) -> int:
        """Open the output (specified in self.path_output) with Aegisub.

        This can be usefull if you don't have MPV installed or you want to look at your output in detailed.

        Returns:
            0 if success, -1 if the output couldn't be opened.
        """

        # Check if it was saved
        if not self.__saved:
            print(
                "[WARNING] You've tried to open the output with Aegisub before having saved. Check your code."
            )
            return -1

        if sys.platform == "win32":
            os.startfile(self.path_output)
        else:
            try:
                subprocess.call(["aegisub", os.path.abspath(self.path_output)])
            except FileNotFoundError:
                print("[WARNING] Aegisub not found.")
                return -1

        return 0

    def open_mpv(
        self, video_path: str = "", video_start: str = "", full_screen: bool = False
    ) -> int:
        """Open the output (specified in self.path_output) in softsub with the MPV player.
        To utilize this function, MPV player is required. Additionally if you're on Windows, MPV must be in the PATH (check https://pyonfx.readthedocs.io/en/latest/quick%20start.html#installation-extra-step).

        This is one of the fastest way to reproduce your output in a comfortable way.

        Parameters:
            video_path (string): The video file path (absolute) to reproduce. If not specified, **meta.video** is automatically taken.
            video_start (string): The start time for the video (more info: https://mpv.io/manual/master/#options-start). If not specified, 0 is automatically taken.
            full_screen (bool): If True, it will reproduce the output in full screen. If not specified, False is automatically taken.
        """

        # Check if it was saved
        if not self.__saved:
            print(
                "[ERROR] You've tried to open the output with MPV before having saved. Check your code."
            )
            return -1

        # Check if mpv is usable
        if self.meta.video.startswith("?dummy") and not video_path:
            print(
                "[WARNING] Cannot use MPV (if you have it in your PATH) for file preview, since your .ass contains a dummy video.\n"
                "You can specify a new video source using video_path parameter, check the documentation of the function."
            )
            return -1

        # Setting up the command to execute
        cmd = ["mpv"]

        if not video_path:
            cmd.append(self.meta.video)
        else:
            cmd.append(video_path)
        if video_start:
            cmd.append("--start=" + video_start)
        if full_screen:
            cmd.append("--fs")

        cmd.append("--sub-file=" + self.path_output)

        try:
            subprocess.call(cmd)
        except FileNotFoundError:
            print(
                "[WARNING] MPV not found in your environment variables.\n"
                "Please refer to the documentation's \"Quick Start\" section if you don't know how to solve it."
            )
            return -1

        return 0


def pretty_print(
    obj: Union[Meta, Style, Line, Word, Syllable, Char], indent: int = 0, name: str = ""
) -> str:
    # Utility function to print object Meta, Style, Line, Word, Syllable and Char (this is a dirty solution probably)
    if type(obj) == Line:
        out = " " * indent + f"lines[{obj.i}] ({type(obj).__name__}):\n"
    elif type(obj) == Word:
        out = " " * indent + f"words[{obj.i}] ({type(obj).__name__}):\n"
    elif type(obj) == Syllable:
        out = " " * indent + f"syls[{obj.i}] ({type(obj).__name__}):\n"
    elif type(obj) == Char:
        out = " " * indent + f"chars[{obj.i}] ({type(obj).__name__}):\n"
    else:
        out = " " * indent + f"{name}({type(obj).__name__}):\n"

    # Let's print all this object fields
    indent += 4
    for k, v in obj.__dict__.items():
        if "__dict__" in dir(v):
            # Work recursively to print another object
            out += pretty_print(v, indent, k + " ")
        elif type(v) == list:
            for i, el in enumerate(v):
                # Work recursively to print other objects inside a list
                out += pretty_print(el, indent, f"{k}[{i}] ")
        else:
            # Just print a field of this object
            out += " " * indent + f"{k}: {str(v)}\n"

    return out
