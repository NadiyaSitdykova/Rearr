import sys
lines = []
once = {}
twice = {}

if __name__ == '__main__':
    filename = sys.argv[1]
    threshold_length = int(sys.argv[2])
    threshold_identity = float(sys.argv[3])
    with open(filename, 'r') as file:
        for line in file.readlines():
            blocks = line.split()
            if len(blocks) > 0 and blocks[0] != "SW" and blocks[0] != "score":
                repeat_class = blocks[10].split("/")[0]
                repeat_length = int(blocks[6]) - int(blocks[5])
                repeat_identity = 100 - (float(blocks[1]) + float(blocks[2]) + float(blocks[3]))
                if repeat_class != "DNA" or repeat_length < threshold_length or repeat_identity < threshold_identity:
                    continue
                repeat = blocks[9]
                if repeat in once:
                    twice[repeat] = True
                else:
                    once[repeat] = True
            lines.append(line)

    with open("filtered_" + filename, 'w') as out:
        for line in lines:
            blocks = line.split()
            if len(blocks) > 0 and blocks[0] != "SW" and blocks[0] != "score":
                repeat = blocks[9]
                if repeat in twice:
                    out.write(line)




