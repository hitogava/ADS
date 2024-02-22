def wrap(target: str, st="", end="") -> str:
    return st + target + end


def results_per_algo(algos: list, results: list[list]) -> list:
    res = []
    for i in range(len(algos)):
        curr = []
        for x in results:
            curr.append(x[i])
        res += [(algos[i], curr)]
    return res


b_label = "Benchmark"


def make_max_col_widths(benchmarks: list, algos: list, results: list[list]):
    max_bench_name_len = max(len(x) for x in benchmarks + [b_label])
    rpa = results_per_algo(algos, results)
    max_col_widths = {x[0]: max([len(str(r)) for r in x[1]] + [len(x[0])])
                      for x in rpa}
    max_col_widths[b_label] = max_bench_name_len
    return max_col_widths


def format_table(benchmarks: list, algos: list, results: list[list]):
    side_col_num = 2
    # max column widths
    mcw = make_max_col_widths(benchmarks, algos, results)

    # drawing table labels
    labels = (b_label + " ").ljust(mcw[b_label] + 1)
    for algo in algos:
        labels += wrap(algo.ljust(mcw[algo]), "| ", " ")
    labels = wrap(labels, "| ", "|")
    print(labels)

    # drawing dashes
    dashes = wrap("-" * (len(labels) - side_col_num), "|", "|")
    print(dashes)
    for item in list(zip(benchmarks, results)):
        row = item[0].ljust(mcw[b_label]) + " "
        zipped = list(zip(algos, [str(x) for x in item[1]]))
        for res in zipped:
            row += wrap(res[1].ljust(mcw[res[0]]), "| ", " ")
        row = wrap(row, "| ", "|")
        print(row)


# format_table(["best case", "the worst case", "the totally really\
# fully fcking chaotic bad case"],
#              ["quick super puper sort", "merge sort", "bubble sort"],
#              [['0.0000001231231274374327984324327843287432872348798732432',
#                1.56, 2.0], [3.3, 2.9, 3.9], [0, 0, 0]])
