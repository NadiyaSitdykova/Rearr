import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    threshold = int(sys.argv[2])
    with open(filename, 'r') as file:
        with open(str(threshold) + "_" + filename, 'w') as out:
            for line in file.readlines():
                blocks = line.split()
                if len(blocks) > 0 and blocks[0] != "SW" and blocks[0] != "score":
                    repeat_length = int(blocks[6]) - int(blocks[5])
                    if repeat_length <= threshold:
                        continue
                out.write(line)