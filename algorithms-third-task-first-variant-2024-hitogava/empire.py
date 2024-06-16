import sys
from hashtable import BucketTypes, HashTable


def solution(data: str, out):
    lines = data.split("\n")
    ht = HashTable(chlimit=10)
    for line in lines:
        if line.startswith("Located rebel base on "):
            name = line[len("Located rebel base on ") :]
            target = ht.find(name)
            if not target:
                ht.insert(name, 1)
            else:
                target.pair.value += 1
            out.write("Roger that\n")
        elif line.endswith("invaded"):
            name = line[: -len(" invaded")]
            trgt = ht.find(name)
            if trgt:
                trgt.pair.value -= 1
            out.write("Roger that\n")
        elif line.endswith("destroyed"):
            name = line[: -len(" destroyed")]
            ht.remove(name)
            out.write("Roger that\n")
        elif line.startswith("Rebel bases on"):
            name = line[len("Rebel bases on ") :]
            planet = ht.find(name)
            if not planet:
                out.write(f"Bases on {name}: 0\n")
            else:
                out.write(f"Bases on {name}: {planet.pair.value}\n")


def run():
    if len(sys.argv) <= 2:
        print("Wrong number of arguments: please specify input and output files.")
        return

    input_name, output_name = sys.argv[1], sys.argv[2]
    with open(input_name, "r") as inp:
        with open(output_name, "w") as out:
            data = inp.read()
            result = solution(data, out)


run()
