# -*- coding: UTF-8 -*-
import os

def get_f_title(f_path, pre, next):
    ffi = open(f_path)
    f_data = ffi.read()
    ffi.close()
    xx = f_data.rsplit("***", 1)
    res = xx[0] + "***\n\n"
    res += '{{< prevnext prev="' + pre[0] + '" next="' + next[0] + '" >}}\n' + pre[1] + "\n<--->\n" + next[1] + "\n{{< /prevnext >}}\n"
    ffo = open(f_path, "w")
    ffo.write(res)
    ffo.close()

def deal_file(f_path, pre, next):
    f_a = "./content" + f_path
    f_b = f_a + "index.md"
    f_c = f_a[:-1] + ".md"
    if os.path.exists(f_b):
        return get_f_title(f_b, pre, next)
    else:
        return get_f_title(f_c, pre, next)


fi = open("./content/_index.md")
data = fi.read()
fi.close()

sps = data.split("\n")
lst = [("/", "主页")]

for line in sps:
    if not line.startswith("<->"):
        continue
    xx = line.split("<->")
    p = xx[1]
    t = xx[2].strip()
    lst.append((p, t))
lst.append(("/", "主页"))

i = 1
while i < len(lst) - 1:
    deal_file(lst[i][0], lst[i-1], lst[i+1])
    i += 1
