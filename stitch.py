#!/usr/bin/env python3

"""
Stitch website screenshots into a single preview image for archive.org
"""

if __name__ == '__main__':
    import sys, math
    from PIL import Image

    destsize = (1000, 1000)
    out = Image.new ('RGB', destsize)

    yoff = 0
    paths = [p.strip() for p in sys.stdin]
    if not paths:
        sys.exit (1)
    yoffTab = int (destsize[1]/len (paths))
    for path in paths:
        with open (path, 'rb') as fd:
            try:
                img = Image.open (fd)
            except OSError:
                # ignore broken images
                continue
            newh = int (math.floor (destsize[0]/img.width*img.height))
            img = img.resize ((destsize[0], newh), Image.LANCZOS)
            out.paste (img, (0, yoff))
            yoff += yoffTab

    out.save (sys.argv[1], 'JPEG', quality=90)

