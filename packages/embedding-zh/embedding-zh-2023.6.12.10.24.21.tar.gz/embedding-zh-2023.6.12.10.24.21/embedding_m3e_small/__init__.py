#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__
# @Time         : 2023/6/12 09:24
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from sentence_transformers import SentenceTransformer

model_name_or_path = get_resolve_path('m3e-small', __file__)
sentence_transformer = SentenceTransformer(model_name_or_path)
