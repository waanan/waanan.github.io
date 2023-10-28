import os

def get_f_title(f_path):
    title = ""
    ffi = open(f_path)
    for line in ffi:
        if line.startswith("title:"):
            title = line.replace("title: ", "").replace('"', "").strip()
            break
    ffi.close()
    return title

def get_title(f_path):
    f_a = "./content" + f_path
    f_b = f_a + "index.md"
    f_c = f_a[:-1] + ".md"
    if os.path.exists(f_b):
        return get_f_title(f_b)
    else:
        return get_f_title(f_c)


fi = open("./content/_index.md")
data = fi.read()
fi.close()

sps = data.split("\n")

res = ""
for line in sps:
    if not line.startswith("<->"):
        res += line + "\n"
        continue
    xx = line.split("<->")
    p = xx[1]
    t = xx[2].strip().split(" ", 1)
    a = t[0]
    b = t[1]
    res += "<->{}<-> {} {}\n".format(p, a, get_title(p))
    
res = res[:-1]

fo = open("./content/_index.md", "w")
fo.write(res)
fo.close()