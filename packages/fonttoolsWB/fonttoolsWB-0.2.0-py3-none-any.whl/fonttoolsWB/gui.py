"""
gui
===============================================================================

FontTools WorkBench GUI Application
"""

import sys

import fonttoolsWB

app = fonttoolsWB.App(
    debug=0,
    iconName="FONTTOOLS",
)
del fonttoolsWB

def main():
    sys.exit(app.run())


if __name__ == "__main__":
    main()
