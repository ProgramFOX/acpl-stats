import re
import math
import statistics
import pymongo
import os

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

def qop_white_black(pgn):
    cps = [annotation_to_cp(x) for x in re.findall(r"\[%eval (-?\d+\.\d+|#-?\d+)\]", pgn)]
    cps = cps[21:]
    if len(cps) < 3:
        return None
    zipped = list(zip(cps, cps[1:]))
    white = filter(lambda x: abs(x[0]) <= 200 and abs(x[1]) <= 200, zipped[::2])
    black = filter(lambda x: abs(x[0]) <= 200 and abs(x[1]) <= 200, zipped[1::2])
    white_losses = list(map(lambda x: min(300, max(0, x[0] - x[1])), white))
    black_losses = list(map(lambda x: min(300, max(0, x[1] - x[0])), black))
    if len(white_losses) > 0:
        wq = int(100 - statistics.mean(white_losses))
    else:
        wq = None
    if len(black_losses) > 0:
        bq = int(100 - statistics.mean(black_losses))
    else:
        bq = None
    return (wq, bq)

def speed_from_event_line(line):
    line = line.lower()
    for t in ["ultrabullet", "bullet", "blitz", "rapid", "classical", "correspondence"]:
        if t in line:
            return t
    return "unknown"

def read_pgn_and_update_db(path):
    client = pymongo.MongoClient()
    db = client.get_database("qopstats")
    collection = db.get_collection("entries")
    with open(path) as f:
        white_id = ""
        black_id = ""
        white_elo = -1
        black_elo = -1
        speed = ""
        lichess_id = ""

        for line in f:
            line = line.strip()
            if line == "": continue
            if line.startswith("[Event "):
                speed = speed_from_event_line(line)
            elif line.startswith("[White "):
                white_id = line.split("\"")[1].lower()
            elif line.startswith("[Black "):
                black_id = line.split("\"")[1].lower()
            elif line.startswith("[WhiteElo ") and not "?" in line:
                white_elo = int(line.split("\"")[1])
            elif line.startswith("[BlackElo ") and not "?" in line:
                black_elo = int(line.split("\"")[1])
            elif line.startswith("[Site "):
                lichess_id = line.split("\"")[1].split("/")[-1]
            elif line.startswith("1. ") and "[%eval" in line and white_elo != -1 and black_elo != -1 and "12. " in line:
                qop = qop_white_black(line)
                if qop is not None:
                    if qop[0] is not None:
                        collection.insert_one({ "_id": lichess_id + "-W",
                                                "rating": white_elo,
                                                "opponent_rating": black_elo,
                                                "speed": speed,
                                                "player": white_id,
                                                "qop": qop[0] })
                    if qop[1] is not None:
                        collection.insert_one({ "_id": lichess_id + "-B",
                                                "rating": black_elo,
                                                "opponent_rating": white_elo,
                                                "speed": speed,
                                                "player": black_id,
                                                "qop": qop[1] })
                white_elo = -1
                black_elo = -1
        
    client.close()

if __name__ == "__main__":
    directory = input("Directory: ")
    for fn in os.listdir(directory):
        if fn.endswith(".pgn"):
            fp = os.path.join(directory, fn)
            print("Entering " + fp)
            read_pgn_and_update_db(fp)
    print("Done.")