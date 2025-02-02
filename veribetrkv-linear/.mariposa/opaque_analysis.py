dfy_files = open(".mariposa/unique_imports.txt").readlines()
import os

def filter_comments(file):
    in_comment = False
    new_lines = []
    for line in open(file).readlines():
        line = line.strip()
        if line.startswith("//"):
            continue
        elif "/*" in line:
            in_comment = True
        if "*/" in line:
            in_comment = False
        if in_comment:
            continue
        new_lines.append(line)
    return new_lines

def find_opaque_usage(file):
    count = 0
    defs = []
    for line in filter_comments(file):
        if "opaque" in line:
            defs.append(line.strip())
            count += 1
    if count > 0:
        print(os.path.realpath(file))
        for d in defs:
            print(d)
        print("")
    return count

PROC_KEYWORDS = ["function",
                 "function method",
                 "predicate", 
                 "predicate method",
                 "method", 
                 "lemma"]

def count_procs(file, defs, opaques):
    for line in filter_comments(file):
        changed = True
        while changed:
            changed = False
            for k in ["shared", "linear", "static", "inout"]:
                if line.startswith(k):
                    line = line.replace(k, "")
                    line = line.strip()
                    changed = True
        if line.startswith("function"):
            if "function method" in line:
                k = "function method"
            else:
                k = "function"
            k = "function"
            defs[k] += 1

            if "{:opaque}" in line:
                opaques[k] += 1
        elif line.startswith("method"):
            defs["method"] += 1
        elif line.startswith("predicate"):
            if "predicate method" in line:
                k = "predicate method"
            else:
                k = "predicate"       
            defs[k] += 1

            if "{:opaque}" in line:
                opaques[k] += 1
            defs["predicate"] += 1
        elif line.startswith("lemma"):
            defs["lemma"] += 1
        # else:
        #     for k in defs:
        #         if k in line:
        #             print(file)
        #             print(line)
    return defs

defs = {p: 0 for p in PROC_KEYWORDS}
opaques = {p: 0 for p in PROC_KEYWORDS}

for dfy_file in dfy_files:
    # print(dfy_file.strip())
    # count = find_opaque_usage(dfy_file.strip())
    defs = count_procs(dfy_file.strip(), defs, opaques)

from tabulate import tabulate

table = []

for cc in [defs, opaques]:
    cc["function total"] = cc["function"] + cc["function method"]
    cc["predicate total"] = cc["predicate"] + cc["predicate method"]

total = defs["function total"] + defs["predicate total"] + defs["method"] + defs["lemma"]
opaque_total = opaques["function total"] + opaques["predicate total"] + opaques["method"] + opaques["lemma"]

spec_total = defs["function total"] + defs["predicate total"]
spec_opaque_total = opaques["function total"] + opaques["predicate total"]

defs["spec total"] = spec_total
opaques["spec total"] = spec_opaque_total

for k in [
    "function total",
    "predicate total",
    "spec total",
    "method", 
    "lemma"]:

    pcounts = defs[k]
    ocounts = opaques[k]
    if k == "lemma" or k == "method":
        rate = "-"
        ocounts = "-"
    else:
        rate = "%.1f" % (ocounts * 100/pcounts) + "%"
        ocounts = '{:,}'.format(ocounts) 
    pcounts = '{:,}'.format(pcounts) 
    table.append([k, pcounts, ocounts, rate])

table.append(["Total", '{:,}'.format(total), opaque_total, "%.1f" % (opaque_total * 100/total) + "%"])

print(tabulate(table, headers=["Keyword", "Total", "Opaque", "Rate"], tablefmt="latex"))

