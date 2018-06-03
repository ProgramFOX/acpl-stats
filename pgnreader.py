import re
import math
import statistics

CEILING = 1000 # copied from lila

def annotation_to_cp(ann):
    if not ann.startswith("#"):
        cp = int(float(ann) * 100)
        if abs(cp) > CEILING:
            cp = math.copysign(CEILING, cp)
        return cp
    else:
        if "-" in ann:
            return -CEILING
        else:
            return CEILING

def acpl_white_black(pgn):
    cps = [annotation_to_cp(x) for x in re.findall(r"\[%eval (-?\d+\.\d+|#-?\d+)\]", pgn)]
    cps.insert(0, 10)
    losses = [i-j for i,j in zip(cps, cps[1:])]
    polarized = [x if i % 2 == 0 else -x for i, x in enumerate(losses)]
    losses_white = [max(0, x) for x in polarized[::2]]
    losses_black = [max(0, x) for x in polarized[1::2]]
    return (int(statistics.mean(losses_white)), int(statistics.mean(losses_black)))
