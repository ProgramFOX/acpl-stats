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

def acpl_white_black(pgn):
    cps = [annotation_to_cp(x) for x in re.findall(r"\[%eval (-?\d+\.\d+|#-?\d+)\]", pgn)]
    cps.insert(0, 10)
    losses = [i-j for i,j in zip(cps, cps[1:])]
    polarized = [x if i % 2 == 0 else -x for i, x in enumerate(losses)]
    losses_white = [max(0, x) for x in polarized[::2]]
    losses_black = [max(0, x) for x in polarized[1::2]]
    return (int(statistics.mean(losses_white)), int(statistics.mean(losses_black)))

def speed_from_event_line(line):
    line = line.lower()
    for t in ["ultrabullet", "bullet", "blitz", "rapid", "classical", "correspondence"]:
        if t in line:
            return t
    return "unknown"

def read_pgn_and_update_db(path):
    client = pymongo.MongoClient()
    db = client.get_database("acplstats")
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
            elif line.startswith("1. ") and "[%eval" in line and white_elo != -1 and black_elo != -1 and "3. " in line:
                acpl = acpl_white_black(line)
                collection.insert_one({ "_id": lichess_id + "-W",
                                        "rating": white_elo,
                                        "opponent_rating": black_elo,
                                        "speed": speed,
                                        "player": white_id,
                                        "acpl": acpl[0] })
                collection.insert_one({ "_id": lichess_id + "-B",
                                        "rating": black_elo,
                                        "opponent_rating": white_elo,
                                        "speed": speed,
                                        "player": black_id,
                                        "acpl": acpl[1] })
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