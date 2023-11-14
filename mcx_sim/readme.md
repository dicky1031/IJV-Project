How to execute MCX_sim
===


[![hackmd-github-sync-badge](https://hackmd.io/ygh1d2wOSeuPGTxB9IZHEQ/badge)](https://hackmd.io/ygh1d2wOSeuPGTxB9IZHEQ)

## Table of Contents
- [Executing Experiments](#Executing-Experiments)
- [Beginners Guide](#Beginners-Guide)
- [Details for setting](#Details-for-setting)

## Executing Experiments

Make sure you already have /bin/MCX in this directory.
If not, compiled from **MD703_edit_MCX_src_v2023/src** in advance.*


You should use **linux** environment to do the following commands.
If you want to execute in **Windows**, you need to fix two problems carefully:
1. Compile the **MD703_edit_MCX_src_v2023/src** in **Windows**, we use a user-define LED source pattern to make the simulation in consistent with the experiments.
2. Write your own shell script in Windows version. (bash can't work, use batch)

```shell=
bash Run_MCX_Sim.sh
```

please see **Run_MCX_Sim.sh** for details and understand the work flows.

## Beginners Guide

If you are a total beginner to this, start here!

1. Learn some syntax about shell script https://blog.techbridge.cc/2019/11/15/linux-shell-script-tutorial/
2. Read the document about MCX source code https://github.com/fangq/mcx

## Details for setting
[LED source]: 
1. in the folder **"input_template/share_files/model_input_related"** contains the CDF of LED source (multiplied by sin due to 3D).
2. we edited the source code, to view what we edited check this https://github.com/fangq/mcx/pull/194/files
3. more detail about LED source https://hackmd.io/@73X8klpNRmSsdgJzudHbgA/SyeF6nI9P#20210326---mcx_corecu-%E4%BF%AE%E6%94%B9%E6%96%B9%E6%B3%95%E8%A6%8F%E5%8A%83
4. Geometry model setting
https://hackmd.io/@73X8klpNRmSsdgJzudHbgA/Byo9D2iCO?fbclid=IwAR11h4vS-rScHVwF4zTrYSlFVayP8p63mHKPTCLOthZ6d3p3Kd0SmH1kyDI

[How we execute MCX]:
1. we use **mcx_ultrasound_opsbased.py** to access the executive file which is compiled from the source code



###### tags: `MCX` `Documentation`
