#!/usr/bin/python3

import os
import pandas as pd

gp_dir = os.path.expanduser("~/.config/Gpredict")
sat_dir = os.path.join(gp_dir, "satdata")
trsp_dir = os.path.join(gp_dir, "trsp")

fns = os.listdir(sat_dir)
sat_fns = [i for i in fns if i.endswith('sat')]
fns = os.listdir(trsp_dir)
trsp_fns = [i for i in fns if i.endswith('trsp')]

# parse satellite index and name
sats = pd.DataFrame()
for i in sat_fns:
    sat_id = i.split('.')[0]
    with open(os.path.join(sat_dir, i)) as f:
        data = f.read()
        data_list = data.split('\n')
        sat_name = None
        for j in data_list:
            tmp = j.split("=")
            if tmp[0] == "NAME":
                sat_name = tmp[1]
        if sat_name:
            sats = sats.append({"id": sat_id, "name":sat_name}, ignore_index=True)
sats = sats.set_index("id")

# parse transponders
trsps = pd.DataFrame()
for i in trsp_fns:
    sat_id = i.split('.')[0]
    with open(os.path.join(trsp_dir, i)) as f:
        data = f.read()
        data_list = data.split('[')
        for t in data_list:
            if ']' in t:
                tmp = t.split(']')
                t_name = tmp[0]
                t_list = tmp[1].split('\n')
                t_dict = {"id": sat_id, "transponder": t_name}
                for j in t_list:
                    if "=" in j:
                        tmp = j.split("=")
                        val = tmp[1]
                        try:
                            val = int(val)
                        except:
                            pass
                        t_dict[tmp[0]] = val
                trsps = trsps.append(t_dict, ignore_index=True)
trsps = trsps.set_index("id")

sats = sats.join(trsps)

print(sats)


