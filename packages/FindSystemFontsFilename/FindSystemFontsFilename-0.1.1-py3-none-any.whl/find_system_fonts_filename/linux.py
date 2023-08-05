import sys
import time
from ctypes import byref, c_char_p, c_int, c_void_p, cdll, POINTER, Structure
from ctypes import util
from enum import Enum, IntEnum
from typing import Set


class FcFontFormat(Enum):
    # https://freetype.org/freetype2/docs/reference/ft2-font_formats.html#ft_get_font_format
    # https://gitlab.freedesktop.org/freetype/freetype/-/blob/0a3836c97d5e84d6721ac0fd2839e8ae1b7be8d9/include/freetype/internal/services/svfntfmt.h#L36
    FT_FONT_FORMAT_TRUETYPE = b"TrueType"
    FT_FONT_FORMAT_TYPE_1 = b"Type 1"
    FT_FONT_FORMAT_BDF = b"BDF"
    FT_FONT_FORMAT_PCF = b"PCF"
    FT_FONT_FORMAT_TYPE_42 = b"Type 42"
    FT_FONT_FORMAT_CID = b"CID Type 1"
    FT_FONT_FORMAT_CFF = b"CFF"
    FT_FONT_FORMAT_PFR = b"PFR"
    FT_FONT_FORMAT_WINFNT = b"Windows FNT"


class FcResult(IntEnum):
    # https://gitlab.freedesktop.org/fontconfig/fontconfig/-/blob/222d058525506e587a45368f10e45e4b80ca541f/fontconfig/fontconfig.h#L241
    FcResultMatch = 0
    FcResultNoMatch = 1
    FcResultTypeMismatch = 2
    FcResultNoId = 3
    FcResultOutOfMemory = 4


class FcFontSet(Structure):
    # https://gitlab.freedesktop.org/fontconfig/fontconfig/-/blob/222d058525506e587a45368f10e45e4b80ca541f/fontconfig/fontconfig.h#L278
    _fields_ = [
        ("nfont", c_int),
        ("sfont", c_int),
        ("fonts", POINTER(POINTER(c_void_p))),
    ]


def get_fonts_filepath_linux() -> Set[str]:
    """
    Inspired by: https://stackoverflow.com/questions/10542832/how-to-use-fontconfig-to-get-font-list-c-c/14634033#14634033

    Return an list of all the font installed.
    """
    font_config_library_name = util.find_library("fontconfig")

    if font_config_library_name is None:
        raise Exception("You need to have installed FontConfig")
    
    VALID_FONT_FORMATS = [FcFontFormat.FT_FONT_FORMAT_TRUETYPE, FcFontFormat.FT_FONT_FORMAT_CFF]

    font_config = cdll.LoadLibrary(font_config_library_name)

    font_config.FcInitLoadConfigAndFonts.restype = c_void_p
    font_config.FcInitLoadConfigAndFonts.argtypes = []

    font_config.FcPatternCreate.restype = c_void_p
    font_config.FcPatternCreate.argtypes = []

    font_config.FcObjectSetBuild.restype = c_void_p
    font_config.FcObjectSetBuild.argtypes = [c_char_p, c_void_p]

    font_config.FcFontList.restype = POINTER(FcFontSet)
    font_config.FcFontList.argtypes = [c_void_p, c_void_p, c_void_p]

    font_config.FcPatternGetString.restype = FcResult
    font_config.FcPatternGetString.argtypes = [c_void_p, c_char_p, c_int, POINTER(c_char_p)]

    config = font_config.FcInitLoadConfigAndFonts()
    pat = font_config.FcPatternCreate()
    os = font_config.FcObjectSetBuild(b"file", b"fontformat", 0)
    fs = font_config.FcFontList(config, pat, None)

    fonts_path = set()

    for i in range(fs.contents.nfont):
        font = fs.contents.fonts[i]
        file_path_ptr = c_char_p()
        font_format_ptr = c_char_p()

        if (
            font_config.FcPatternGetString(font, b"fontformat", 0, byref(font_format_ptr)) == FcResult.FcResultMatch and
            font_config.FcPatternGetString(font, b"file", 0, byref(file_path_ptr)) == FcResult.FcResultMatch
        ):
            font_format = FcFontFormat(font_format_ptr.value)

            if font_format in VALID_FONT_FORMATS:
                # Decode with utf-8 since FcChar8
                fonts_path.add(file_path_ptr.value.decode())

    # I am not 100% if we need to call all of these. We may only need to call FcFontSetDestroy.
    font_config.FcConfigDestroy(config)
    font_config.FcPatternDestroy(pat)
    font_config.FcObjectSetDestroy(os)
    font_config.FcFontSetDestroy(fs)

    return fonts_path


def main():
    start = time.time()
    fonts_path_dwrite = get_fonts_filepath_linux()
    print(f"Time elapsed: {time.time() - start}")
    print(len(fonts_path_dwrite))


if __name__ == "__main__":
    sys.exit(main())
