import sys

if not sys.platform == "win32":
    raise Exception("cleanify is only available on Windows devices!")

import klembord

klembord.init()