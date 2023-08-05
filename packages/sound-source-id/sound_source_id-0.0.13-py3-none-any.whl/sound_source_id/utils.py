# -*- coding: utf-8 -*-

import numpy as np

def deg2rad(v_deg):
    v_rad = (np.pi/180)*v_deg
    return v_rad

def rms_fun(vals):
    res = np.sqrt(np.mean(vals**2))
    return res
