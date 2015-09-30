import sys

ORIGINA_REPEATS_FILE = sys.argv[1]
THRESHOLD_LENGTH = int(sys.argv[2])
THRESHOLD_IDENTITY = float(sys.argv[3])
CLASSES = ["DNA", "LINE", "SINE"]

if __name__ == '__main__':
    once = {}
    twice = {}

    with open(ORIGINA_REPEATS_FILE, 'r') as file:
        for line in file.readlines():
            blocks = line.split()
            if len(blocks) > 0 and blocks[0] != "SW" and blocks[0] != "score":
                repeat_class = blocks[10].split("/")[0]
                repeat_length = int(blocks[6]) - int(blocks[5])
                repeat_identity = 100 - (float(blocks[1]) + float(blocks[2]) + float(blocks[3]))
                if repeat_class not in CLASSES or repeat_length < THRESHOLD_LENGTH or repeat_identity < THRESHOLD_IDENTITY:
                    continue
                repeat = blocks[9]
                if repeat in once:
                    twice[repeat] = True
                else:
                    once[repeat] = True

    with open(ORIGINA_REPEATS_FILE, 'r') as file:
        with open("filtered_" + filename, 'w') as out:
            for line in file.readlines():
                blocks = line.split()
                if len(blocks) > 0 and blocks[0] != "SW" and blocks[0] != "score":
                    repeat = blocks[9]
                    if repeat in twice:
                        out.write(line)



