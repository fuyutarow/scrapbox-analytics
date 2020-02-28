#!/usr/bin/env python
# coding: utf-8

import json
from pathlib import Path
import matplotlib.pyplot as plt
import maya
#  import modin.pandas as pd
import pandas as pd


def json2doc(fpath):
    with fpath.open() as f:
        doc = json.load(f)
    return {
        "exported": maya.when(str(doc["exported"])).iso8601(),
        "pages": len(doc["pages"])
    }


json_iter = Path("scrapbox.sairilab").glob("*.json")
docs = [json2doc(f) for f in json_iter]

df = pd.DataFrame(docs)
df = df.set_index("exported")
df.index = pd.to_datetime(df.index)
df = df.sort_index()
df.to_csv("ok.csv")
df.plot()
plt.savefig("n_pages.png")

df.diff().rolling(3).mean().plot()
plt.savefig("dn3_pages.png")

df.diff().rolling(7).mean().plot()
plt.savefig("dn_pages.png")
