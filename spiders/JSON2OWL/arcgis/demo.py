#!/home/houzw/.conda/envs/gkb/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/23 9:57
import os
import sys
sys.path.append('/home/houzw/.conda/envs/gkb/bin')
print(os.path)
from owlready2 import *

module_path = os.path.dirname(__file__)
open(module_path+'/arcgis.json','r')