# -*- coding: utf-8 -*-
# @Time    : 2023/5/7 12:14
# @Author  : LiZhen
# @FileName: prune.py
# @github  : https://github.com/Lizhen0628
# @Description:

import os
import torch


def prune_it(p, keep_only_ema=True):
    print(f"prunin' in path: {p}")
    size_initial = os.path.getsize(p)
    nsd = dict()
    sd = torch.load(p, map_location="cpu")
    print(sd.keys())
    #for k in sd.keys():
    #    if k != "optimizer_states":
    #        nsd[k] = sd[k]
    #else:
    #    print(f"removing optimizer states for path {p}")
    if "global_step" in sd:
        print(f"This is global step {sd['global_step']}.")
    if keep_only_ema:
        if "state_dict" in sd:
            sd = sd["state_dict"]
        # infer ema keys
        ema_keys = {k: "model_ema." + k[6:].replace(".", ".") for k in sd.keys() if k.startswith("model.")}
        new_sd = {"state_dict": {}}

        for k in sd:
            ema_k = "___"
            try:
                ema_k = "model_ema." + k[6:].replace(".", "")
            except:
                pass
            if ema_k in sd:
                new_sd[k] = sd[ema_k]#.half()
                print("ema: " + ema_k + " > " + k)
            elif not k.startswith("model_ema.") or k in ["model_ema.num_updates", "model_ema.decay"]:
                new_sd[k] = sd[k]#.half()
                print(k)
            else:
                print("skipped: " + k)
            if k in new_sd and isinstance(new_sd[k], torch.FloatTensor):
                new_sd[k] = new_sd[k]#.half()

        #assert len(new_sd) == len(sd) - len(ema_keys)
        nsd["state_dict"] = new_sd
    else:
        sd = nsd['state_dict'].copy()
        new_sd = dict()
        for k in sd:
            new_sd[k] = sd[k]#.half()
        nsd['state_dict'] = new_sd

    fn = f"{os.path.splitext(p)[0]}-pruned.ckpt" if not keep_only_ema else f"{os.path.splitext(p)[0]}-ema-pruned.ckpt"
    print(f"saving pruned checkpoint at: {fn}")
    torch.save(nsd, fn)
    newsize = os.path.getsize(fn)
    MSG = f"New ckpt size: {newsize*1e-9:.2f} GB. " + \
          f"Saved {(size_initial - newsize)*1e-9:.2f} GB by removing optimizer states"
    if keep_only_ema:
        MSG += " and non-EMA weights"
    print(MSG)


if __name__ == "__main__":
    #prune_it('anime700k-64bs-0.1ucg-penultimate-1epoch-clip-ema-continue-76000.pt')
    import sys
    prune_it(sys.argv[1])
