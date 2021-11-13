r"""
ANSI color helper for Python

Example usage:
    >>> from ansicolor import fore, back, style
    >>> print(fore.LIGHT_BLUE + back.RED + style.BOLD + "Hello World !!!" + style.RESET)

Show color palette:
    >>> import ansicolor
    >>> for i, color in enumerate(ansicolor.colors):
    >>>     print(getattr(ansicolor.fore, color), i, color, ansicolor.style.RESET)

WINDOWS USERS:  You must enable ANSI color in the Windows console:
    1. Run regedit.exe
    2. Add a DWORD to HKEY_CURRENT_USER\Console:
        name: VirtualTerminalLevel
        value: 1

    Any cmd.exe windows opened from this point forward will support ANSI
    escape sequences.

https://gitlab.com/dslackw/colored/

Copyright 2014 Dimitris Zlatanidis

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

colors = [
    'BLACK',
    'RED',
    'GREEN',
    'YELLOW',
    'BLUE',
    'MAGENTA',
    'CYAN',
    'LIGHT_GRAY',
    'DARK_GRAY',
    'LIGHT_RED',
    'LIGHT_GREEN',
    'LIGHT_YELLOW',
    'LIGHT_BLUE',
    'LIGHT_MAGENTA',
    'LIGHT_CYAN',
    'WHITE',
    'GREY_0',
    'NAVY_BLUE',
    'DARK_BLUE',
    'BLUE_3A',
    'BLUE_3B',
    'BLUE_1',
    'DARK_GREEN',
    'DEEP_SKY_BLUE_4A',
    'DEEP_SKY_BLUE_4B',
    'DEEP_SKY_BLUE_4C',
    'DODGER_BLUE_3',
    'DODGER_BLUE_2',
    'GREEN_4',
    'SPRING_GREEN_4',
    'TURQUOISE_4',
    'DEEP_SKY_BLUE_3A',
    'DEEP_SKY_BLUE_3B',
    'DODGER_BLUE_1',
    'GREEN_3A',
    'SPRING_GREEN_3A',
    'DARK_CYAN',
    'LIGHT_SEA_GREEN',
    'DEEP_SKY_BLUE_2',
    'DEEP_SKY_BLUE_1',
    'GREEN_3B',
    'SPRING_GREEN_3B',
    'SPRING_GREEN_2A',
    'CYAN_3',
    'DARK_TURQUOISE',
    'TURQUOISE_2',
    'GREEN_1',
    'SPRING_GREEN_2B',
    'SPRING_GREEN_1',
    'MEDIUM_SPRING_GREEN',
    'CYAN_2',
    'CYAN_1',
    'DARK_RED_1',
    'DEEP_PINK_4A',
    'PURPLE_4A',
    'PURPLE_4B',
    'PURPLE_3',
    'BLUE_VIOLET',
    'ORANGE_4A',
    'GREY_37',
    'MEDIUM_PURPLE_4',
    'SLATE_BLUE_3A',
    'SLATE_BLUE_3B',
    'ROYAL_BLUE_1',
    'CHARTREUSE_4',
    'DARK_SEA_GREEN_4A',
    'PALE_TURQUOISE_4',
    'STEEL_BLUE',
    'STEEL_BLUE_3',
    'CORNFLOWER_BLUE',
    'CHARTREUSE_3A',
    'DARK_SEA_GREEN_4B',
    'CADET_BLUE_2',
    'CADET_BLUE_1',
    'SKY_BLUE_3',
    'STEEL_BLUE_1A',
    'CHARTREUSE_3B',
    'PALE_GREEN_3A',
    'SEA_GREEN_3',
    'AQUAMARINE_3',
    'MEDIUM_TURQUOISE',
    'STEEL_BLUE_1B',
    'CHARTREUSE_2A',
    'SEA_GREEN_2',
    'SEA_GREEN_1A',
    'SEA_GREEN_1B',
    'AQUAMARINE_1A',
    'DARK_SLATE_GRAY_2',
    'DARK_RED_2',
    'DEEP_PINK_4B',
    'DARK_MAGENTA_1',
    'DARK_MAGENTA_2',
    'DARK_VIOLET_1A',
    'PURPLE_1A',
    'ORANGE_4B',
    'LIGHT_PINK_4',
    'PLUM_4',
    'MEDIUM_PURPLE_3A',
    'MEDIUM_PURPLE_3B',
    'SLATE_BLUE_1',
    'YELLOW_4A',
    'WHEAT_4',
    'GREY_53',
    'LIGHT_SLATE_GREY',
    'MEDIUM_PURPLE',
    'LIGHT_SLATE_BLUE',
    'YELLOW_4B',
    'DARK_OLIVE_GREEN_3A',
    'DARK_GREEN_SEA',
    'LIGHT_SKY_BLUE_3A',
    'LIGHT_SKY_BLUE_3B',
    'SKY_BLUE_2',
    'CHARTREUSE_2B',
    'DARK_OLIVE_GREEN_3B',
    'PALE_GREEN_3B',
    'DARK_SEA_GREEN_3A',
    'DARK_SLATE_GRAY_3',
    'SKY_BLUE_1',
    'CHARTREUSE_1',
    'LIGHT_GREEN_2',
    'LIGHT_GREEN_3',
    'PALE_GREEN_1A',
    'AQUAMARINE_1B',
    'DARK_SLATE_GRAY_1',
    'RED_3A',
    'DEEP_PINK_4C',
    'MEDIUM_VIOLET_RED',
    'MAGENTA_3A',
    'DARK_VIOLET_1B',
    'PURPLE_1B',
    'DARK_ORANGE_3A',
    'INDIAN_RED_1A',
    'HOT_PINK_3A',
    'MEDIUM_ORCHID_3',
    'MEDIUM_ORCHID',
    'MEDIUM_PURPLE_2A',
    'DARK_GOLDENROD',
    'LIGHT_SALMON_3A',
    'ROSY_BROWN',
    'GREY_63',
    'MEDIUM_PURPLE_2B',
    'MEDIUM_PURPLE_1',
    'GOLD_3A',
    'DARK_KHAKI',
    'NAVAJO_WHITE_3',
    'GREY_69',
    'LIGHT_STEEL_BLUE_3',
    'LIGHT_STEEL_BLUE',
    'YELLOW_3A',
    'DARK_OLIVE_GREEN_3',
    'DARK_SEA_GREEN_3B',
    'DARK_SEA_GREEN_2',
    'LIGHT_CYAN_3',
    'LIGHT_SKY_BLUE_1',
    'GREEN_YELLOW',
    'DARK_OLIVE_GREEN_2',
    'PALE_GREEN_1B',
    'DARK_SEA_GREEN_5B',
    'DARK_SEA_GREEN_5A',
    'PALE_TURQUOISE_1',
    'RED_3B',
    'DEEP_PINK_3A',
    'DEEP_PINK_3B',
    'MAGENTA_3B',
    'MAGENTA_3C',
    'MAGENTA_2A',
    'DARK_ORANGE_3B',
    'INDIAN_RED_1B',
    'HOT_PINK_3B',
    'HOT_PINK_2',
    'ORCHID',
    'MEDIUM_ORCHID_1A',
    'ORANGE_3',
    'LIGHT_SALMON_3B',
    'LIGHT_PINK_3',
    'PINK_3',
    'PLUM_3',
    'VIOLET',
    'GOLD_3B',
    'LIGHT_GOLDENROD_3',
    'TAN',
    'MISTY_ROSE_3',
    'THISTLE_3',
    'PLUM_2',
    'YELLOW_3B',
    'KHAKI_3',
    'LIGHT_GOLDENROD_2A',
    'LIGHT_YELLOW_3',
    'GREY_84',
    'LIGHT_STEEL_BLUE_1',
    'YELLOW_2',
    'DARK_OLIVE_GREEN_1A',
    'DARK_OLIVE_GREEN_1B',
    'DARK_SEA_GREEN_1',
    'HONEYDEW_2',
    'LIGHT_CYAN_1',
    'RED_1',
    'DEEP_PINK_2',
    'DEEP_PINK_1A',
    'DEEP_PINK_1B',
    'MAGENTA_2B',
    'MAGENTA_1',
    'ORANGE_RED_1',
    'INDIAN_RED_1C',
    'INDIAN_RED_1D',
    'HOT_PINK_1A',
    'HOT_PINK_1B',
    'MEDIUM_ORCHID_1B',
    'DARK_ORANGE',
    'SALMON_1',
    'LIGHT_CORAL',
    'PALE_VIOLET_RED_1',
    'ORCHID_2',
    'ORCHID_1',
    'ORANGE_1',
    'SANDY_BROWN',
    'LIGHT_SALMON_1',
    'LIGHT_PINK_1',
    'PINK_1',
    'PLUM_1',
    'GOLD_1',
    'LIGHT_GOLDENROD_2B',
    'LIGHT_GOLDENROD_2C',
    'NAVAJO_WHITE_1',
    'MISTY_ROSE1',
    'THISTLE_1',
    'YELLOW_1',
    'LIGHT_GOLDENROD_1',
    'KHAKI_1',
    'WHEAT_1',
    'CORNSILK_1',
    'GREY_100',
    'GREY_3',
    'GREY_7',
    'GREY_11',
    'GREY_15',
    'GREY_19',
    'GREY_23',
    'GREY_27',
    'GREY_30',
    'GREY_35',
    'GREY_39',
    'GREY_42',
    'GREY_46',
    'GREY_50',
    'GREY_54',
    'GREY_58',
    'GREY_62',
    'GREY_66',
    'GREY_70',
    'GREY_74',
    'GREY_78',
    'GREY_82',
    'GREY_85',
    'GREY_89',
    'GREY_93'
    ]


class fore:
    BLACK = '\x1b[38;5;0m'
    RED = '\x1b[38;5;1m'
    GREEN = '\x1b[38;5;2m'
    YELLOW = '\x1b[38;5;3m'
    BLUE = '\x1b[38;5;4m'
    MAGENTA = '\x1b[38;5;5m'
    CYAN = '\x1b[38;5;6m'
    LIGHT_GRAY = '\x1b[38;5;7m'
    DARK_GRAY = '\x1b[38;5;8m'
    LIGHT_RED = '\x1b[38;5;9m'
    LIGHT_GREEN = '\x1b[38;5;10m'
    LIGHT_YELLOW = '\x1b[38;5;11m'
    LIGHT_BLUE = '\x1b[38;5;12m'
    LIGHT_MAGENTA = '\x1b[38;5;13m'
    LIGHT_CYAN = '\x1b[38;5;14m'
    WHITE = '\x1b[38;5;15m'
    GREY_0 = '\x1b[38;5;16m'
    NAVY_BLUE = '\x1b[38;5;17m'
    DARK_BLUE = '\x1b[38;5;18m'
    BLUE_3A = '\x1b[38;5;19m'
    BLUE_3B = '\x1b[38;5;20m'
    BLUE_1 = '\x1b[38;5;21m'
    DARK_GREEN = '\x1b[38;5;22m'
    DEEP_SKY_BLUE_4A = '\x1b[38;5;23m'
    DEEP_SKY_BLUE_4B = '\x1b[38;5;24m'
    DEEP_SKY_BLUE_4C = '\x1b[38;5;25m'
    DODGER_BLUE_3 = '\x1b[38;5;26m'
    DODGER_BLUE_2 = '\x1b[38;5;27m'
    GREEN_4 = '\x1b[38;5;28m'
    SPRING_GREEN_4 = '\x1b[38;5;29m'
    TURQUOISE_4 = '\x1b[38;5;30m'
    DEEP_SKY_BLUE_3A = '\x1b[38;5;31m'
    DEEP_SKY_BLUE_3B = '\x1b[38;5;32m'
    DODGER_BLUE_1 = '\x1b[38;5;33m'
    GREEN_3A = '\x1b[38;5;34m'
    SPRING_GREEN_3A = '\x1b[38;5;35m'
    DARK_CYAN = '\x1b[38;5;36m'
    LIGHT_SEA_GREEN = '\x1b[38;5;37m'
    DEEP_SKY_BLUE_2 = '\x1b[38;5;38m'
    DEEP_SKY_BLUE_1 = '\x1b[38;5;39m'
    GREEN_3B = '\x1b[38;5;40m'
    SPRING_GREEN_3B = '\x1b[38;5;41m'
    SPRING_GREEN_2A = '\x1b[38;5;42m'
    CYAN_3 = '\x1b[38;5;43m'
    DARK_TURQUOISE = '\x1b[38;5;44m'
    TURQUOISE_2 = '\x1b[38;5;45m'
    GREEN_1 = '\x1b[38;5;46m'
    SPRING_GREEN_2B = '\x1b[38;5;47m'
    SPRING_GREEN_1 = '\x1b[38;5;48m'
    MEDIUM_SPRING_GREEN = '\x1b[38;5;49m'
    CYAN_2 = '\x1b[38;5;50m'
    CYAN_1 = '\x1b[38;5;51m'
    DARK_RED_1 = '\x1b[38;5;52m'
    DEEP_PINK_4A = '\x1b[38;5;53m'
    PURPLE_4A = '\x1b[38;5;54m'
    PURPLE_4B = '\x1b[38;5;55m'
    PURPLE_3 = '\x1b[38;5;56m'
    BLUE_VIOLET = '\x1b[38;5;57m'
    ORANGE_4A = '\x1b[38;5;58m'
    GREY_37 = '\x1b[38;5;59m'
    MEDIUM_PURPLE_4 = '\x1b[38;5;60m'
    SLATE_BLUE_3A = '\x1b[38;5;61m'
    SLATE_BLUE_3B = '\x1b[38;5;62m'
    ROYAL_BLUE_1 = '\x1b[38;5;63m'
    CHARTREUSE_4 = '\x1b[38;5;64m'
    DARK_SEA_GREEN_4A = '\x1b[38;5;65m'
    PALE_TURQUOISE_4 = '\x1b[38;5;66m'
    STEEL_BLUE = '\x1b[38;5;67m'
    STEEL_BLUE_3 = '\x1b[38;5;68m'
    CORNFLOWER_BLUE = '\x1b[38;5;69m'
    CHARTREUSE_3A = '\x1b[38;5;70m'
    DARK_SEA_GREEN_4B = '\x1b[38;5;71m'
    CADET_BLUE_2 = '\x1b[38;5;72m'
    CADET_BLUE_1 = '\x1b[38;5;73m'
    SKY_BLUE_3 = '\x1b[38;5;74m'
    STEEL_BLUE_1A = '\x1b[38;5;75m'
    CHARTREUSE_3B = '\x1b[38;5;76m'
    PALE_GREEN_3A = '\x1b[38;5;77m'
    SEA_GREEN_3 = '\x1b[38;5;78m'
    AQUAMARINE_3 = '\x1b[38;5;79m'
    MEDIUM_TURQUOISE = '\x1b[38;5;80m'
    STEEL_BLUE_1B = '\x1b[38;5;81m'
    CHARTREUSE_2A = '\x1b[38;5;82m'
    SEA_GREEN_2 = '\x1b[38;5;83m'
    SEA_GREEN_1A = '\x1b[38;5;84m'
    SEA_GREEN_1B = '\x1b[38;5;85m'
    AQUAMARINE_1A = '\x1b[38;5;86m'
    DARK_SLATE_GRAY_2 = '\x1b[38;5;87m'
    DARK_RED_2 = '\x1b[38;5;88m'
    DEEP_PINK_4B = '\x1b[38;5;89m'
    DARK_MAGENTA_1 = '\x1b[38;5;90m'
    DARK_MAGENTA_2 = '\x1b[38;5;91m'
    DARK_VIOLET_1A = '\x1b[38;5;92m'
    PURPLE_1A = '\x1b[38;5;93m'
    ORANGE_4B = '\x1b[38;5;94m'
    LIGHT_PINK_4 = '\x1b[38;5;95m'
    PLUM_4 = '\x1b[38;5;96m'
    MEDIUM_PURPLE_3A = '\x1b[38;5;97m'
    MEDIUM_PURPLE_3B = '\x1b[38;5;98m'
    SLATE_BLUE_1 = '\x1b[38;5;99m'
    YELLOW_4A = '\x1b[38;5;100m'
    WHEAT_4 = '\x1b[38;5;101m'
    GREY_53 = '\x1b[38;5;102m'
    LIGHT_SLATE_GREY = '\x1b[38;5;103m'
    MEDIUM_PURPLE = '\x1b[38;5;104m'
    LIGHT_SLATE_BLUE = '\x1b[38;5;105m'
    YELLOW_4B = '\x1b[38;5;106m'
    DARK_OLIVE_GREEN_3A = '\x1b[38;5;107m'
    DARK_GREEN_SEA = '\x1b[38;5;108m'
    LIGHT_SKY_BLUE_3A = '\x1b[38;5;109m'
    LIGHT_SKY_BLUE_3B = '\x1b[38;5;110m'
    SKY_BLUE_2 = '\x1b[38;5;111m'
    CHARTREUSE_2B = '\x1b[38;5;112m'
    DARK_OLIVE_GREEN_3B = '\x1b[38;5;113m'
    PALE_GREEN_3B = '\x1b[38;5;114m'
    DARK_SEA_GREEN_3A = '\x1b[38;5;115m'
    DARK_SLATE_GRAY_3 = '\x1b[38;5;116m'
    SKY_BLUE_1 = '\x1b[38;5;117m'
    CHARTREUSE_1 = '\x1b[38;5;118m'
    LIGHT_GREEN_2 = '\x1b[38;5;119m'
    LIGHT_GREEN_3 = '\x1b[38;5;120m'
    PALE_GREEN_1A = '\x1b[38;5;121m'
    AQUAMARINE_1B = '\x1b[38;5;122m'
    DARK_SLATE_GRAY_1 = '\x1b[38;5;123m'
    RED_3A = '\x1b[38;5;124m'
    DEEP_PINK_4C = '\x1b[38;5;125m'
    MEDIUM_VIOLET_RED = '\x1b[38;5;126m'
    MAGENTA_3A = '\x1b[38;5;127m'
    DARK_VIOLET_1B = '\x1b[38;5;128m'
    PURPLE_1B = '\x1b[38;5;129m'
    DARK_ORANGE_3A = '\x1b[38;5;130m'
    INDIAN_RED_1A = '\x1b[38;5;131m'
    HOT_PINK_3A = '\x1b[38;5;132m'
    MEDIUM_ORCHID_3 = '\x1b[38;5;133m'
    MEDIUM_ORCHID = '\x1b[38;5;134m'
    MEDIUM_PURPLE_2A = '\x1b[38;5;135m'
    DARK_GOLDENROD = '\x1b[38;5;136m'
    LIGHT_SALMON_3A = '\x1b[38;5;137m'
    ROSY_BROWN = '\x1b[38;5;138m'
    GREY_63 = '\x1b[38;5;139m'
    MEDIUM_PURPLE_2B = '\x1b[38;5;140m'
    MEDIUM_PURPLE_1 = '\x1b[38;5;141m'
    GOLD_3A = '\x1b[38;5;142m'
    DARK_KHAKI = '\x1b[38;5;143m'
    NAVAJO_WHITE_3 = '\x1b[38;5;144m'
    GREY_69 = '\x1b[38;5;145m'
    LIGHT_STEEL_BLUE_3 = '\x1b[38;5;146m'
    LIGHT_STEEL_BLUE = '\x1b[38;5;147m'
    YELLOW_3A = '\x1b[38;5;148m'
    DARK_OLIVE_GREEN_3 = '\x1b[38;5;149m'
    DARK_SEA_GREEN_3B = '\x1b[38;5;150m'
    DARK_SEA_GREEN_2 = '\x1b[38;5;151m'
    LIGHT_CYAN_3 = '\x1b[38;5;152m'
    LIGHT_SKY_BLUE_1 = '\x1b[38;5;153m'
    GREEN_YELLOW = '\x1b[38;5;154m'
    DARK_OLIVE_GREEN_2 = '\x1b[38;5;155m'
    PALE_GREEN_1B = '\x1b[38;5;156m'
    DARK_SEA_GREEN_5B = '\x1b[38;5;157m'
    DARK_SEA_GREEN_5A = '\x1b[38;5;158m'
    PALE_TURQUOISE_1 = '\x1b[38;5;159m'
    RED_3B = '\x1b[38;5;160m'
    DEEP_PINK_3A = '\x1b[38;5;161m'
    DEEP_PINK_3B = '\x1b[38;5;162m'
    MAGENTA_3B = '\x1b[38;5;163m'
    MAGENTA_3C = '\x1b[38;5;164m'
    MAGENTA_2A = '\x1b[38;5;165m'
    DARK_ORANGE_3B = '\x1b[38;5;166m'
    INDIAN_RED_1B = '\x1b[38;5;167m'
    HOT_PINK_3B = '\x1b[38;5;168m'
    HOT_PINK_2 = '\x1b[38;5;169m'
    ORCHID = '\x1b[38;5;170m'
    MEDIUM_ORCHID_1A = '\x1b[38;5;171m'
    ORANGE_3 = '\x1b[38;5;172m'
    LIGHT_SALMON_3B = '\x1b[38;5;173m'
    LIGHT_PINK_3 = '\x1b[38;5;174m'
    PINK_3 = '\x1b[38;5;175m'
    PLUM_3 = '\x1b[38;5;176m'
    VIOLET = '\x1b[38;5;177m'
    GOLD_3B = '\x1b[38;5;178m'
    LIGHT_GOLDENROD_3 = '\x1b[38;5;179m'
    TAN = '\x1b[38;5;180m'
    MISTY_ROSE_3 = '\x1b[38;5;181m'
    THISTLE_3 = '\x1b[38;5;182m'
    PLUM_2 = '\x1b[38;5;183m'
    YELLOW_3B = '\x1b[38;5;184m'
    KHAKI_3 = '\x1b[38;5;185m'
    LIGHT_GOLDENROD_2A = '\x1b[38;5;186m'
    LIGHT_YELLOW_3 = '\x1b[38;5;187m'
    GREY_84 = '\x1b[38;5;188m'
    LIGHT_STEEL_BLUE_1 = '\x1b[38;5;189m'
    YELLOW_2 = '\x1b[38;5;190m'
    DARK_OLIVE_GREEN_1A = '\x1b[38;5;191m'
    DARK_OLIVE_GREEN_1B = '\x1b[38;5;192m'
    DARK_SEA_GREEN_1 = '\x1b[38;5;193m'
    HONEYDEW_2 = '\x1b[38;5;194m'
    LIGHT_CYAN_1 = '\x1b[38;5;195m'
    RED_1 = '\x1b[38;5;196m'
    DEEP_PINK_2 = '\x1b[38;5;197m'
    DEEP_PINK_1A = '\x1b[38;5;198m'
    DEEP_PINK_1B = '\x1b[38;5;199m'
    MAGENTA_2B = '\x1b[38;5;200m'
    MAGENTA_1 = '\x1b[38;5;201m'
    ORANGE_RED_1 = '\x1b[38;5;202m'
    INDIAN_RED_1C = '\x1b[38;5;203m'
    INDIAN_RED_1D = '\x1b[38;5;204m'
    HOT_PINK_1A = '\x1b[38;5;205m'
    HOT_PINK_1B = '\x1b[38;5;206m'
    MEDIUM_ORCHID_1B = '\x1b[38;5;207m'
    DARK_ORANGE = '\x1b[38;5;208m'
    SALMON_1 = '\x1b[38;5;209m'
    LIGHT_CORAL = '\x1b[38;5;210m'
    PALE_VIOLET_RED_1 = '\x1b[38;5;211m'
    ORCHID_2 = '\x1b[38;5;212m'
    ORCHID_1 = '\x1b[38;5;213m'
    ORANGE_1 = '\x1b[38;5;214m'
    SANDY_BROWN = '\x1b[38;5;215m'
    LIGHT_SALMON_1 = '\x1b[38;5;216m'
    LIGHT_PINK_1 = '\x1b[38;5;217m'
    PINK_1 = '\x1b[38;5;218m'
    PLUM_1 = '\x1b[38;5;219m'
    GOLD_1 = '\x1b[38;5;220m'
    LIGHT_GOLDENROD_2B = '\x1b[38;5;221m'
    LIGHT_GOLDENROD_2C = '\x1b[38;5;222m'
    NAVAJO_WHITE_1 = '\x1b[38;5;223m'
    MISTY_ROSE1 = '\x1b[38;5;224m'
    THISTLE_1 = '\x1b[38;5;225m'
    YELLOW_1 = '\x1b[38;5;226m'
    LIGHT_GOLDENROD_1 = '\x1b[38;5;227m'
    KHAKI_1 = '\x1b[38;5;228m'
    WHEAT_1 = '\x1b[38;5;229m'
    CORNSILK_1 = '\x1b[38;5;230m'
    GREY_100 = '\x1b[38;5;231m'
    GREY_3 = '\x1b[38;5;232m'
    GREY_7 = '\x1b[38;5;233m'
    GREY_11 = '\x1b[38;5;234m'
    GREY_15 = '\x1b[38;5;235m'
    GREY_19 = '\x1b[38;5;236m'
    GREY_23 = '\x1b[38;5;237m'
    GREY_27 = '\x1b[38;5;238m'
    GREY_30 = '\x1b[38;5;239m'
    GREY_35 = '\x1b[38;5;240m'
    GREY_39 = '\x1b[38;5;241m'
    GREY_42 = '\x1b[38;5;242m'
    GREY_46 = '\x1b[38;5;243m'
    GREY_50 = '\x1b[38;5;244m'
    GREY_54 = '\x1b[38;5;245m'
    GREY_58 = '\x1b[38;5;246m'
    GREY_62 = '\x1b[38;5;247m'
    GREY_66 = '\x1b[38;5;248m'
    GREY_70 = '\x1b[38;5;249m'
    GREY_74 = '\x1b[38;5;250m'
    GREY_78 = '\x1b[38;5;251m'
    GREY_82 = '\x1b[38;5;252m'
    GREY_85 = '\x1b[38;5;253m'
    GREY_89 = '\x1b[38;5;254m'
    GREY_93 = '\x1b[38;5;255m'

class back:
    BLACK = '\x1b[48;5;0m'
    RED = '\x1b[48;5;1m'
    GREEN = '\x1b[48;5;2m'
    YELLOW = '\x1b[48;5;3m'
    BLUE = '\x1b[48;5;4m'
    MAGENTA = '\x1b[48;5;5m'
    CYAN = '\x1b[48;5;6m'
    LIGHT_GRAY = '\x1b[48;5;7m'
    DARK_GRAY = '\x1b[48;5;8m'
    LIGHT_RED = '\x1b[48;5;9m'
    LIGHT_GREEN = '\x1b[48;5;10m'
    LIGHT_YELLOW = '\x1b[48;5;11m'
    LIGHT_BLUE = '\x1b[48;5;12m'
    LIGHT_MAGENTA = '\x1b[48;5;13m'
    LIGHT_CYAN = '\x1b[48;5;14m'
    WHITE = '\x1b[48;5;15m'
    GREY_0 = '\x1b[48;5;16m'
    NAVY_BLUE = '\x1b[48;5;17m'
    DARK_BLUE = '\x1b[48;5;18m'
    BLUE_3A = '\x1b[48;5;19m'
    BLUE_3B = '\x1b[48;5;20m'
    BLUE_1 = '\x1b[48;5;21m'
    DARK_GREEN = '\x1b[48;5;22m'
    DEEP_SKY_BLUE_4A = '\x1b[48;5;23m'
    DEEP_SKY_BLUE_4B = '\x1b[48;5;24m'
    DEEP_SKY_BLUE_4C = '\x1b[48;5;25m'
    DODGER_BLUE_3 = '\x1b[48;5;26m'
    DODGER_BLUE_2 = '\x1b[48;5;27m'
    GREEN_4 = '\x1b[48;5;28m'
    SPRING_GREEN_4 = '\x1b[48;5;29m'
    TURQUOISE_4 = '\x1b[48;5;30m'
    DEEP_SKY_BLUE_3A = '\x1b[48;5;31m'
    DEEP_SKY_BLUE_3B = '\x1b[48;5;32m'
    DODGER_BLUE_1 = '\x1b[48;5;33m'
    GREEN_3A = '\x1b[48;5;34m'
    SPRING_GREEN_3A = '\x1b[48;5;35m'
    DARK_CYAN = '\x1b[48;5;36m'
    LIGHT_SEA_GREEN = '\x1b[48;5;37m'
    DEEP_SKY_BLUE_2 = '\x1b[48;5;38m'
    DEEP_SKY_BLUE_1 = '\x1b[48;5;39m'
    GREEN_3B = '\x1b[48;5;40m'
    SPRING_GREEN_3B = '\x1b[48;5;41m'
    SPRING_GREEN_2A = '\x1b[48;5;42m'
    CYAN_3 = '\x1b[48;5;43m'
    DARK_TURQUOISE = '\x1b[48;5;44m'
    TURQUOISE_2 = '\x1b[48;5;45m'
    GREEN_1 = '\x1b[48;5;46m'
    SPRING_GREEN_2B = '\x1b[48;5;47m'
    SPRING_GREEN_1 = '\x1b[48;5;48m'
    MEDIUM_SPRING_GREEN = '\x1b[48;5;49m'
    CYAN_2 = '\x1b[48;5;50m'
    CYAN_1 = '\x1b[48;5;51m'
    DARK_RED_1 = '\x1b[48;5;52m'
    DEEP_PINK_4A = '\x1b[48;5;53m'
    PURPLE_4A = '\x1b[48;5;54m'
    PURPLE_4B = '\x1b[48;5;55m'
    PURPLE_3 = '\x1b[48;5;56m'
    BLUE_VIOLET = '\x1b[48;5;57m'
    ORANGE_4A = '\x1b[48;5;58m'
    GREY_37 = '\x1b[48;5;59m'
    MEDIUM_PURPLE_4 = '\x1b[48;5;60m'
    SLATE_BLUE_3A = '\x1b[48;5;61m'
    SLATE_BLUE_3B = '\x1b[48;5;62m'
    ROYAL_BLUE_1 = '\x1b[48;5;63m'
    CHARTREUSE_4 = '\x1b[48;5;64m'
    DARK_SEA_GREEN_4A = '\x1b[48;5;65m'
    PALE_TURQUOISE_4 = '\x1b[48;5;66m'
    STEEL_BLUE = '\x1b[48;5;67m'
    STEEL_BLUE_3 = '\x1b[48;5;68m'
    CORNFLOWER_BLUE = '\x1b[48;5;69m'
    CHARTREUSE_3A = '\x1b[48;5;70m'
    DARK_SEA_GREEN_4B = '\x1b[48;5;71m'
    CADET_BLUE_2 = '\x1b[48;5;72m'
    CADET_BLUE_1 = '\x1b[48;5;73m'
    SKY_BLUE_3 = '\x1b[48;5;74m'
    STEEL_BLUE_1A = '\x1b[48;5;75m'
    CHARTREUSE_3B = '\x1b[48;5;76m'
    PALE_GREEN_3A = '\x1b[48;5;77m'
    SEA_GREEN_3 = '\x1b[48;5;78m'
    AQUAMARINE_3 = '\x1b[48;5;79m'
    MEDIUM_TURQUOISE = '\x1b[48;5;80m'
    STEEL_BLUE_1B = '\x1b[48;5;81m'
    CHARTREUSE_2A = '\x1b[48;5;82m'
    SEA_GREEN_2 = '\x1b[48;5;83m'
    SEA_GREEN_1A = '\x1b[48;5;84m'
    SEA_GREEN_1B = '\x1b[48;5;85m'
    AQUAMARINE_1A = '\x1b[48;5;86m'
    DARK_SLATE_GRAY_2 = '\x1b[48;5;87m'
    DARK_RED_2 = '\x1b[48;5;88m'
    DEEP_PINK_4B = '\x1b[48;5;89m'
    DARK_MAGENTA_1 = '\x1b[48;5;90m'
    DARK_MAGENTA_2 = '\x1b[48;5;91m'
    DARK_VIOLET_1A = '\x1b[48;5;92m'
    PURPLE_1A = '\x1b[48;5;93m'
    ORANGE_4B = '\x1b[48;5;94m'
    LIGHT_PINK_4 = '\x1b[48;5;95m'
    PLUM_4 = '\x1b[48;5;96m'
    MEDIUM_PURPLE_3A = '\x1b[48;5;97m'
    MEDIUM_PURPLE_3B = '\x1b[48;5;98m'
    SLATE_BLUE_1 = '\x1b[48;5;99m'
    YELLOW_4A = '\x1b[48;5;100m'
    WHEAT_4 = '\x1b[48;5;101m'
    GREY_53 = '\x1b[48;5;102m'
    LIGHT_SLATE_GREY = '\x1b[48;5;103m'
    MEDIUM_PURPLE = '\x1b[48;5;104m'
    LIGHT_SLATE_BLUE = '\x1b[48;5;105m'
    YELLOW_4B = '\x1b[48;5;106m'
    DARK_OLIVE_GREEN_3A = '\x1b[48;5;107m'
    DARK_GREEN_SEA = '\x1b[48;5;108m'
    LIGHT_SKY_BLUE_3A = '\x1b[48;5;109m'
    LIGHT_SKY_BLUE_3B = '\x1b[48;5;110m'
    SKY_BLUE_2 = '\x1b[48;5;111m'
    CHARTREUSE_2B = '\x1b[48;5;112m'
    DARK_OLIVE_GREEN_3B = '\x1b[48;5;113m'
    PALE_GREEN_3B = '\x1b[48;5;114m'
    DARK_SEA_GREEN_3A = '\x1b[48;5;115m'
    DARK_SLATE_GRAY_3 = '\x1b[48;5;116m'
    SKY_BLUE_1 = '\x1b[48;5;117m'
    CHARTREUSE_1 = '\x1b[48;5;118m'
    LIGHT_GREEN_2 = '\x1b[48;5;119m'
    LIGHT_GREEN_3 = '\x1b[48;5;120m'
    PALE_GREEN_1A = '\x1b[48;5;121m'
    AQUAMARINE_1B = '\x1b[48;5;122m'
    DARK_SLATE_GRAY_1 = '\x1b[48;5;123m'
    RED_3A = '\x1b[48;5;124m'
    DEEP_PINK_4C = '\x1b[48;5;125m'
    MEDIUM_VIOLET_RED = '\x1b[48;5;126m'
    MAGENTA_3A = '\x1b[48;5;127m'
    DARK_VIOLET_1B = '\x1b[48;5;128m'
    PURPLE_1B = '\x1b[48;5;129m'
    DARK_ORANGE_3A = '\x1b[48;5;130m'
    INDIAN_RED_1A = '\x1b[48;5;131m'
    HOT_PINK_3A = '\x1b[48;5;132m'
    MEDIUM_ORCHID_3 = '\x1b[48;5;133m'
    MEDIUM_ORCHID = '\x1b[48;5;134m'
    MEDIUM_PURPLE_2A = '\x1b[48;5;135m'
    DARK_GOLDENROD = '\x1b[48;5;136m'
    LIGHT_SALMON_3A = '\x1b[48;5;137m'
    ROSY_BROWN = '\x1b[48;5;138m'
    GREY_63 = '\x1b[48;5;139m'
    MEDIUM_PURPLE_2B = '\x1b[48;5;140m'
    MEDIUM_PURPLE_1 = '\x1b[48;5;141m'
    GOLD_3A = '\x1b[48;5;142m'
    DARK_KHAKI = '\x1b[48;5;143m'
    NAVAJO_WHITE_3 = '\x1b[48;5;144m'
    GREY_69 = '\x1b[48;5;145m'
    LIGHT_STEEL_BLUE_3 = '\x1b[48;5;146m'
    LIGHT_STEEL_BLUE = '\x1b[48;5;147m'
    YELLOW_3A = '\x1b[48;5;148m'
    DARK_OLIVE_GREEN_3 = '\x1b[48;5;149m'
    DARK_SEA_GREEN_3B = '\x1b[48;5;150m'
    DARK_SEA_GREEN_2 = '\x1b[48;5;151m'
    LIGHT_CYAN_3 = '\x1b[48;5;152m'
    LIGHT_SKY_BLUE_1 = '\x1b[48;5;153m'
    GREEN_YELLOW = '\x1b[48;5;154m'
    DARK_OLIVE_GREEN_2 = '\x1b[48;5;155m'
    PALE_GREEN_1B = '\x1b[48;5;156m'
    DARK_SEA_GREEN_5B = '\x1b[48;5;157m'
    DARK_SEA_GREEN_5A = '\x1b[48;5;158m'
    PALE_TURQUOISE_1 = '\x1b[48;5;159m'
    RED_3B = '\x1b[48;5;160m'
    DEEP_PINK_3A = '\x1b[48;5;161m'
    DEEP_PINK_3B = '\x1b[48;5;162m'
    MAGENTA_3B = '\x1b[48;5;163m'
    MAGENTA_3C = '\x1b[48;5;164m'
    MAGENTA_2A = '\x1b[48;5;165m'
    DARK_ORANGE_3B = '\x1b[48;5;166m'
    INDIAN_RED_1B = '\x1b[48;5;167m'
    HOT_PINK_3B = '\x1b[48;5;168m'
    HOT_PINK_2 = '\x1b[48;5;169m'
    ORCHID = '\x1b[48;5;170m'
    MEDIUM_ORCHID_1A = '\x1b[48;5;171m'
    ORANGE_3 = '\x1b[48;5;172m'
    LIGHT_SALMON_3B = '\x1b[48;5;173m'
    LIGHT_PINK_3 = '\x1b[48;5;174m'
    PINK_3 = '\x1b[48;5;175m'
    PLUM_3 = '\x1b[48;5;176m'
    VIOLET = '\x1b[48;5;177m'
    GOLD_3B = '\x1b[48;5;178m'
    LIGHT_GOLDENROD_3 = '\x1b[48;5;179m'
    TAN = '\x1b[48;5;180m'
    MISTY_ROSE_3 = '\x1b[48;5;181m'
    THISTLE_3 = '\x1b[48;5;182m'
    PLUM_2 = '\x1b[48;5;183m'
    YELLOW_3B = '\x1b[48;5;184m'
    KHAKI_3 = '\x1b[48;5;185m'
    LIGHT_GOLDENROD_2A = '\x1b[48;5;186m'
    LIGHT_YELLOW_3 = '\x1b[48;5;187m'
    GREY_84 = '\x1b[48;5;188m'
    LIGHT_STEEL_BLUE_1 = '\x1b[48;5;189m'
    YELLOW_2 = '\x1b[48;5;190m'
    DARK_OLIVE_GREEN_1A = '\x1b[48;5;191m'
    DARK_OLIVE_GREEN_1B = '\x1b[48;5;192m'
    DARK_SEA_GREEN_1 = '\x1b[48;5;193m'
    HONEYDEW_2 = '\x1b[48;5;194m'
    LIGHT_CYAN_1 = '\x1b[48;5;195m'
    RED_1 = '\x1b[48;5;196m'
    DEEP_PINK_2 = '\x1b[48;5;197m'
    DEEP_PINK_1A = '\x1b[48;5;198m'
    DEEP_PINK_1B = '\x1b[48;5;199m'
    MAGENTA_2B = '\x1b[48;5;200m'
    MAGENTA_1 = '\x1b[48;5;201m'
    ORANGE_RED_1 = '\x1b[48;5;202m'
    INDIAN_RED_1C = '\x1b[48;5;203m'
    INDIAN_RED_1D = '\x1b[48;5;204m'
    HOT_PINK_1A = '\x1b[48;5;205m'
    HOT_PINK_1B = '\x1b[48;5;206m'
    MEDIUM_ORCHID_1B = '\x1b[48;5;207m'
    DARK_ORANGE = '\x1b[48;5;208m'
    SALMON_1 = '\x1b[48;5;209m'
    LIGHT_CORAL = '\x1b[48;5;210m'
    PALE_VIOLET_RED_1 = '\x1b[48;5;211m'
    ORCHID_2 = '\x1b[48;5;212m'
    ORCHID_1 = '\x1b[48;5;213m'
    ORANGE_1 = '\x1b[48;5;214m'
    SANDY_BROWN = '\x1b[48;5;215m'
    LIGHT_SALMON_1 = '\x1b[48;5;216m'
    LIGHT_PINK_1 = '\x1b[48;5;217m'
    PINK_1 = '\x1b[48;5;218m'
    PLUM_1 = '\x1b[48;5;219m'
    GOLD_1 = '\x1b[48;5;220m'
    LIGHT_GOLDENROD_2B = '\x1b[48;5;221m'
    LIGHT_GOLDENROD_2C = '\x1b[48;5;222m'
    NAVAJO_WHITE_1 = '\x1b[48;5;223m'
    MISTY_ROSE1 = '\x1b[48;5;224m'
    THISTLE_1 = '\x1b[48;5;225m'
    YELLOW_1 = '\x1b[48;5;226m'
    LIGHT_GOLDENROD_1 = '\x1b[48;5;227m'
    KHAKI_1 = '\x1b[48;5;228m'
    WHEAT_1 = '\x1b[48;5;229m'
    CORNSILK_1 = '\x1b[48;5;230m'
    GREY_100 = '\x1b[48;5;231m'
    GREY_3 = '\x1b[48;5;232m'
    GREY_7 = '\x1b[48;5;233m'
    GREY_11 = '\x1b[48;5;234m'
    GREY_15 = '\x1b[48;5;235m'
    GREY_19 = '\x1b[48;5;236m'
    GREY_23 = '\x1b[48;5;237m'
    GREY_27 = '\x1b[48;5;238m'
    GREY_30 = '\x1b[48;5;239m'
    GREY_35 = '\x1b[48;5;240m'
    GREY_39 = '\x1b[48;5;241m'
    GREY_42 = '\x1b[48;5;242m'
    GREY_46 = '\x1b[48;5;243m'
    GREY_50 = '\x1b[48;5;244m'
    GREY_54 = '\x1b[48;5;245m'
    GREY_58 = '\x1b[48;5;246m'
    GREY_62 = '\x1b[48;5;247m'
    GREY_66 = '\x1b[48;5;248m'
    GREY_70 = '\x1b[48;5;249m'
    GREY_74 = '\x1b[48;5;250m'
    GREY_78 = '\x1b[48;5;251m'
    GREY_82 = '\x1b[48;5;252m'
    GREY_85 = '\x1b[48;5;253m'
    GREY_89 = '\x1b[48;5;254m'
    GREY_93 = '\x1b[48;5;255m'

class style:
    BOLD = '\x1b[1m'
    DIM = '\x1b[2m'
    UNDERLINED = '\x1b[4m'
    BLINK = '\x1b[5m'
    REVERSE = '\x1b[7m'
    HIDDEN = '\x1b[8m'
    RESET = '\x1b[0m'
    RES_BOLD = '\x1b[21m'
    RES_DIM = '\x1b[22m'
    RES_UNDERLINED = '\x1b[24m'
    RES_BLINK = '\x1b[25m'
    RES_REVERSE = '\x1b[27m'
    RES_HIDDEN = '\x1b[28m'
    
def show_colors():
    for i, color in enumerate(colors):
        print(getattr(fore, color), i, color, style.RESET)
