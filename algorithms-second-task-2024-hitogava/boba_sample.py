import sys
from avltree import *
from tokenizer import *


class TokenTypes(enum.Enum):
    BountyKeyword = 0
    RankKeyword = 1
    TopKeyword = 2
    RangeKeyword = 3
    CompletedKeyword = 4
    AddKeyword = 5


keywords_map = {
    "add": TokenTypes.AddKeyword,
    "bounty": TokenTypes.BountyKeyword,
    "rank": TokenTypes.RankKeyword,
    "range": TokenTypes.RangeKeyword,
    "completed": TokenTypes.CompletedKeyword,
    "top": TokenTypes.TopKeyword,
}


def add_bounty(ptree: AVLTree, ntree: AVLTree, name, price, out):
    def insert_pair(name, price):
        pnode = Node(key=price, value=name)
        nnode = Node(key=name, value=price)
        pnode.twin = nnode
        nnode.twin = pnode

        ptree.insert(pnode)
        ntree.insert(nnode)

    trgt_node = ntree.find(ntree.root, name)
    if not trgt_node:
        insert_pair(name, price)
    else:
        ptree.remove(trgt_node.twin)
        new = Node(key=trgt_node.value + price, value=name)
        new.twin = trgt_node
        trgt_node.twin = new
        trgt_node.value += price
        ptree.insert(new)
    #print_tree(ntree.root)
    out.write("Roger that\n")


def mark_as_completed(ptree: AVLTree, ntree: AVLTree, name, out):
    trgt = ntree.find(ntree.root, name)
    if trgt:
        ntree.remove(trgt)
        ptree.remove(trgt.twin)
        out.write("Roger that\n")


def get_bounty(ntree, name):
    trgt = ntree.find(ntree.root, name)
    return 0 if not trgt else trgt.value


def get_rank(ptree, ntree, name):
    trgt = ntree.find(ntree.root, name)
    return -1 if not trgt else ptree.rank(ptree.root, trgt.twin) + 1


def parse_and_exec(tokens: list[Token], ptree: AVLTree, ntree: AVLTree, out):
    cursor = 0
    tlen = len(tokens)

    def match_next(expected):
        nonlocal cursor, tlen, tokens
        return (
            False if cursor >= tlen - 1 or tokens[cursor + 1].type != expected else True
        )
    def read_name():
        nonlocal cursor, tlen, tokens
        name = ""
        while cursor < tlen and tokens[cursor].type == DefTokenTypes.IDENTIFIER:
            name += tokens[cursor].value
            if match_next(DefTokenTypes.IDENTIFIER):
                name += " "
            cursor += 1
        return name

    while cursor < tlen:
        if tokens[cursor].type == TokenTypes.AddKeyword and match_next(
            TokenTypes.BountyKeyword
        ):
            cursor += 2
            price = 0
            name = read_name()
            cursor += 1
            if cursor < tlen and tokens[cursor].type == DefTokenTypes.NUMBER:
                price = int(tokens[cursor].value)
            add_bounty(ptree, ntree, name, price, out)
        elif tokens[cursor].type == TokenTypes.CompletedKeyword and match_next(
            DefTokenTypes.IDENTIFIER
        ):
            cursor += 1
            name = read_name()
            mark_as_completed(ptree, ntree, name, out)

        elif tokens[cursor].type == TokenTypes.BountyKeyword and match_next(
            DefTokenTypes.IDENTIFIER
        ):
            cursor += 1
            name = read_name()
            out.write(f"Bounty for {name}: {get_bounty(ntree, name)}\n")
        elif tokens[cursor].type == TokenTypes.RankKeyword and match_next(
            DefTokenTypes.IDENTIFIER
        ):
            cursor += 1
            name = read_name()
            out.write(f"Rank of {name}: {get_rank(ptree, ntree, name)}\n")
        elif tokens[cursor].type == TokenTypes.TopKeyword and match_next(
            DefTokenTypes.NUMBER
        ):
            n = int(tokens[cursor + 1].value)
            topn = ptree.topn(n, ptree.root)
            for t in topn:
                out.write(f"{t.value}: {t.key}\n")
        elif tokens[cursor].type == TokenTypes.RangeKeyword:
            cursor += 2
            lower, upper = int(tokens[cursor].value), int(tokens[cursor + 2].value)
            range = ptree.range(ptree.root, lower, upper)
            for t in range:
                out.write(f"{t.value}: {t.key}\n")
        cursor += 1


def solution(data, out):
    ptree = AVLTree(None)
    ntree = AVLTree(None)
    data = data.split("\n")
    for s in data:
        tokenizer = Tokenizer(keywords_map, None, TokenTypes, s)
        tokens = tokenizer.tokenize()
        parse_and_exec(tokens, ptree, ntree, out)


def run():
    if len(sys.argv) <= 2:
        print("Wrong number of arguments: please specify input and output files.")
        return

    input_name, output_name = sys.argv[1], sys.argv[2]
    with open(input_name, "r") as inp:
        with open(output_name, "w") as out:
            data = inp.read()
            solution(data, out)


run()
