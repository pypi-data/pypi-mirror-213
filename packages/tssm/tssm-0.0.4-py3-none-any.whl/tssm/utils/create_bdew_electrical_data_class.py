from os import system
from os.path import dirname, realpath
from pathlib import Path

import numpy as np
import pandas as pd

from tssm.utils.BDEW_day import BDEWDAY
from tssm.utils.seasons import Season

FOLDER = dirname(realpath(__file__))


def main():
    
    data = pd.read_csv(Path(FOLDER).parent.parent.joinpath("data/BDEW_data.csv"))
    
    header = "from __future__ import annotations\n" \
             "from tssm.utils.seasons import Season\n"
    header += "from tssm.utils.BDEW_day import BDEWDAY\n"
    header += "class BDEWElectrical:\n"
    header += "\tdef __init__(self):\n"
    
    for name in data.columns[3:]:
        val_dict = {}
        for season in Season:
            val_dict[season] = {}
            for day in BDEWDAY:
                value = data[name].to_numpy()[np.where((data["season"] == season.value) & (data["day"] == day.value))]
                val_dict[season][day] = dict(enumerate(value))

        header += f"\n\t\tself.{name}: dict[Season, dict[BDEWDAY, dict[int, float]]] = {val_dict}"
    
    for season in Season:
        header = header.replace(f"{season.__repr__()}", f"{season}")
    for day in BDEWDAY:
        header = header.replace(f"{day.__repr__()}", f"{day}")
    
    with open(Path(FOLDER).joinpath("BDEW_class.py"), "w") as f:
        f.write(header)

    system(f'py -m black --line-length 160 {Path(FOLDER).joinpath("BDEW_class.py")}')
        

if __name__ == "__main__":
    main()
