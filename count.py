#!/usr/bin/env python

import json
from pathlib import Path
from typing import List
import matplotlib.pyplot as plt
import maya
#  import modin.pandas as pd
import pandas as pd
import seaborn as sns


def json2doc(fpath):
    with fpath.open() as f:
        doc = json.load(f)
    pages = doc["pages"]
    texts: List[str] = ["".join(page["lines"]) for page in pages]
    return {
        "exported": maya.when(str(doc["exported"])).iso8601(),
        "pages": len(doc["pages"]),
        "volume[k]": len("".join(texts)) / 1e3,
    }


if __name__ == "__main__":
    json_iter = Path("dumps").glob("*.json")
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
