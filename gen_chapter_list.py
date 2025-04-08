# -*- coding: utf-8 -*-
import json

conf = [
    ("basic", "./content/_index.md"),
    ("lib", "./content/lib/_index.md")
]

obj = {}
for ch_pair in conf:
    ch = ch_pair[0]
    ch_path = ch_pair[1]
    obj[ch] = []
    fi = open(ch_path, "r", encoding='utf-8')
    data = fi.read()
    sps = data.split("{{< chapterlist>}}")
    for sp in sps:
        if "{{< /chapterlist >}}" not in sp:
            continue
        ch_obj = {}
        ch_sps = sp.split("<--->")
        dir_name = ch_sps[0].strip()
        ch_obj["dir_name"] = dir_name
        page_list = []
        p_list_sps = ch_sps[1].split("\n")
        for p_list_sp in p_list_sps:
            if not p_list_sp.startswith("<->"):
                continue
            doc_sps = p_list_sp.split("<->")
            page_obj = {}
            page_obj["page_path"] = doc_sps[1].strip()
            page_obj["page_name"] = doc_sps[2].strip()
            page_list.append(page_obj)
        first_page_path = page_list[0]["page_path"]
        page_path_sps = first_page_path.split("/")
        ch_obj["dir_path"] = page_path_sps[2]

        ch_obj["page_list"] = page_list
        obj[ch].append(ch_obj)

    fi.close()

fo = open("./data/chapters.json", "w", encoding='utf-8')
fo.write(json.dumps(obj, ensure_ascii=False, indent=4))
fo.close()
