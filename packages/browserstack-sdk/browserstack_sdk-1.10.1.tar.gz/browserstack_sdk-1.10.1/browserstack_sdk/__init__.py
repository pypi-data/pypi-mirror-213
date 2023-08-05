# coding: UTF-8
import sys
bstack1l1_opy_ = sys.version_info [0] == 2
bstack1l1l_opy_ = 2048
bstack111_opy_ = 7
def bstack1l_opy_ (bstack11_opy_):
    global bstack11l_opy_
    stringNr = ord (bstack11_opy_ [-1])
    bstack1_opy_ = bstack11_opy_ [:-1]
    bstack1lll_opy_ = stringNr % len (bstack1_opy_)
    bstack1ll1_opy_ = bstack1_opy_ [:bstack1lll_opy_] + bstack1_opy_ [bstack1lll_opy_:]
    if bstack1l1_opy_:
        bstackl_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l_opy_ - (bstack1ll_opy_ + stringNr) % bstack111_opy_) for bstack1ll_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstackl_opy_ = str () .join ([chr (ord (char) - bstack1l1l_opy_ - (bstack1ll_opy_ + stringNr) % bstack111_opy_) for bstack1ll_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstackl_opy_)
import atexit
import os
import signal
import sys
import time
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
from multiprocessing import Pool
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack1l1l111ll_opy_ = {
	bstack1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧࠁ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪࠂ"),
  bstack1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪࠃ"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫࠄ"),
  bstack1l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬࠅ"): bstack1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࠆ"),
  bstack1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫࠇ"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬࠈ"),
  bstack1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࠉ"): bstack1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨࠊ"),
  bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࠋ"): bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨࠌ"),
  bstack1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࠍ"): bstack1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩࠎ"),
  bstack1l_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࠏ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫࠐ"),
  bstack1l_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬࠑ"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨࠒ"),
  bstack1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠓ"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠔ"),
  bstack1l_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠕ"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠖ"),
  bstack1l_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬࠗ"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬ࠘"),
  bstack1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ࠙"): bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠚ"),
  bstack1l_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠛ"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠜ"),
  bstack1l_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠝ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠞ"),
  bstack1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠟ"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠠ"),
  bstack1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࠡ"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࠢ"),
  bstack1l_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠣ"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠤ"),
  bstack1l_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠥ"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠦ"),
  bstack1l_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠧ"): bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠨ"),
  bstack1l_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬࠩ"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬࠪ"),
  bstack1l_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠫ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠬ"),
  bstack1l_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭࠭"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭࠮"),
  bstack1l_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪ࠯"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪ࠰"),
  bstack1l_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠱"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠲"),
  bstack1l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠳"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠴"),
  bstack1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ࠵"): bstack1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ࠶"),
  bstack1l_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ࠷"): bstack1l_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩ࠸"),
  bstack1l_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ࠹"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࠺"),
  bstack1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠻"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠼"),
  bstack1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠽"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠾"),
  bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࠿"): bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ࡀ"),
  bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡁ"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡂ"),
  bstack1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨࡃ"): bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨࡄ"),
  bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡅ"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡆ"),
  bstack1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡇ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡈ"),
}
bstack111l1l1_opy_ = [
  bstack1l_opy_ (u"ࠧࡰࡵࠪࡉ"),
  bstack1l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࡊ"),
  bstack1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࡋ"),
  bstack1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࡌ"),
  bstack1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨࡍ"),
  bstack1l_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩࡎ"),
  bstack1l_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࡏ"),
]
bstack111l1l11_opy_ = {
  bstack1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩࡐ"): [bstack1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩࡑ"), bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡎࡂࡏࡈࠫࡒ")],
  bstack1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࡓ"): bstack1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧࡔ"),
  bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨࡕ"): bstack1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩࡖ"),
  bstack1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬࡗ"): bstack1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊ࠭ࡘ"),
  bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࡙ࠫ"): bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࡚ࠬ"),
  bstack1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰ࡛ࠫ"): bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑ࡙࡟ࡑࡇࡕࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭࡜"),
  bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ࡝"): bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ࡞"),
  bstack1l_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ࡟"): bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ࡠ"),
  bstack1l_opy_ (u"ࠪࡥࡵࡶࠧࡡ"): bstack1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧࡢ"),
  bstack1l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࡣ"): bstack1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࡤࡊࡅࡃࡗࡊࠫࡤ"),
  bstack1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫࡥ"): bstack1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫࡦ")
}
bstack1lllll11l_opy_ = {
  bstack1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࡧ"): [bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬࡨ"), bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࡩ")],
  bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࡪ"): [bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ࡫"), bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࡬")],
  bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡭"): bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡮"),
  bstack1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࡯"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨࡰ"),
  bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡱ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡲ"),
  bstack1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧࡳ"): [bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫࡴ"), bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࡵ")],
  bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࡶ"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩࡷ"),
  bstack1l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡸ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡹ"),
  bstack1l_opy_ (u"ࠧࡢࡲࡳࠫࡺ"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫࡻ"),
  bstack1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡼ"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡽ"),
  bstack1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡾ"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡿ")
}
bstack1l1111111_opy_ = {
  bstack1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢀ"): bstack1l_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫࢁ"),
  bstack1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢂ"): [bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࢃ"), bstack1l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࢄ")],
  bstack1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢅ"): bstack1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢆ"),
  bstack1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪࢇ"): bstack1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ࢈"),
  bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ࢉ"): [bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪࢊ"), bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩࢋ")],
  bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢌ"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢍ"),
  bstack1l_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࢎ"): bstack1l_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬ࢏"),
  bstack1l_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࢐"): [bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࢑"), bstack1l_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ࢒")],
  bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࢓"): [bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭࢔"), bstack1l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭࢕")]
}
bstack111l1l_opy_ = [
  bstack1l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭࢖"),
  bstack1l_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫࢗ"),
  bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ࢘"),
  bstack1l_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶ࢙ࠪ"),
  bstack1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࢚࠭"),
  bstack1l_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻ࢛ࠪ"),
  bstack1l_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ࢜"),
  bstack1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ࢝"),
  bstack1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭࢞"),
  bstack1l_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ࢟"),
  bstack1l_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢠ"),
  bstack1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬࢡ"),
]
bstack11l11l1l_opy_ = [
  bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢢ"),
  bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢣ"),
  bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢤ"),
  bstack1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࢥ"),
  bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢦ"),
  bstack1l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢧ"),
  bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧࢨ"),
  bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩࢩ"),
  bstack1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩࢪ"),
  bstack1l_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬࢫ")
]
bstack1ll1l111l_opy_ = [
  bstack1l_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ࢬ"),
  bstack1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࢭ"),
  bstack1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࢮ"),
  bstack1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢯ"),
  bstack1l_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫࢰ"),
  bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩࢱ"),
  bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩࢲ"),
  bstack1l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ࢳ"),
  bstack1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࢴ"),
  bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࢵ"),
  bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢶ"),
  bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫࢷ"),
  bstack1l_opy_ (u"࠭࡯ࡴࠩࢸ"),
  bstack1l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࢹ"),
  bstack1l_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧࢺ"),
  bstack1l_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫࢻ"),
  bstack1l_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪࢼ"),
  bstack1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ࢽ"),
  bstack1l_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭ࢾ"),
  bstack1l_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪࢿ"),
  bstack1l_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬࣀ"),
  bstack1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬࣁ"),
  bstack1l_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨࣂ"),
  bstack1l_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧࣃ"),
  bstack1l_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬࣄ"),
  bstack1l_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࣅ"),
  bstack1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪࣆ"),
  bstack1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨࣇ"),
  bstack1l_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬࣈ"),
  bstack1l_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭ࣉ"),
  bstack1l_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬ࣊"),
  bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋"),
  bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬ࣌"),
  bstack1l_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬ࣍"),
  bstack1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࣎"),
  bstack1l_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࣏"),
  bstack1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࣐࠭"),
  bstack1l_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪ࣑ࠫ"),
  bstack1l_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵ࣒ࠪ"),
  bstack1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴ࣓ࠩ"),
  bstack1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨࣔ"),
  bstack1l_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩࣕ"),
  bstack1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧࣖ"),
  bstack1l_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧࣗ"),
  bstack1l_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨࣘ"),
  bstack1l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣙ"),
  bstack1l_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪࣚ"),
  bstack1l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ࣛ"),
  bstack1l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫࣜ"),
  bstack1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪࣝ"),
  bstack1l_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪࣞ"),
  bstack1l_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫࣟ"),
  bstack1l_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬ࣠"),
  bstack1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࣡"),
  bstack1l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫ࣢"),
  bstack1l_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࣣࠧ"),
  bstack1l_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪࣤ"),
  bstack1l_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧࣥ"),
  bstack1l_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨࣦ"),
  bstack1l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬࣧ"),
  bstack1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬࣨ"),
  bstack1l_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࣩࠧ"),
  bstack1l_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧ࣪"),
  bstack1l_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨ࣫"),
  bstack1l_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨ࣬"),
  bstack1l_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪ࣭ࠪ"),
  bstack1l_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸ࣮ࠬ"),
  bstack1l_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࣯"),
  bstack1l_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࣰࠪ"),
  bstack1l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸࣱ࠭"),
  bstack1l_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࣲࠫ"),
  bstack1l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ࣳ"),
  bstack1l_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪࣴ"),
  bstack1l_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬࣵ"),
  bstack1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࣶࠬ"),
  bstack1l_opy_ (u"࠭ࡩࡦࠩࣷ"),
  bstack1l_opy_ (u"ࠧࡦࡦࡪࡩࠬࣸ"),
  bstack1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨࣹ"),
  bstack1l_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨࣺ"),
  bstack1l_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬࣻ"),
  bstack1l_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬࣼ"),
  bstack1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫࣽ"),
  bstack1l_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩࣾ"),
  bstack1l_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪࣿ"),
  bstack1l_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬऀ"),
  bstack1l_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩँ"),
  bstack1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪं"),
  bstack1l_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ः"),
  bstack1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ऄ"),
  bstack1l_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩअ"),
  bstack1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧआ"),
  bstack1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩइ"),
  bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪई"),
  bstack1l_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨउ"),
  bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ऊ"),
  bstack1l_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩऋ"),
  bstack1l_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬऌ"),
  bstack1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫऍ"),
  bstack1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫऎ"),
  bstack1l_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ए"),
  bstack1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨऐ"),
  bstack1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ऑ"),
  bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ"),
  bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨओ"),
  bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭औ"),
  bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪक"),
  bstack1l_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬख"),
  bstack1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩग"),
  bstack1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭घ"),
  bstack1l_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨङ")
]
bstack1l11l1ll1_opy_ = {
  bstack1l_opy_ (u"࠭ࡶࠨच"): bstack1l_opy_ (u"ࠧࡷࠩछ"),
  bstack1l_opy_ (u"ࠨࡨࠪज"): bstack1l_opy_ (u"ࠩࡩࠫझ"),
  bstack1l_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩञ"): bstack1l_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪट"),
  bstack1l_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫठ"): bstack1l_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬड"),
  bstack1l_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫढ"): bstack1l_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬण"),
  bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬत"): bstack1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭थ"),
  bstack1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧद"): bstack1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨध"),
  bstack1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩन"): bstack1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऩ"),
  bstack1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫप"): bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬफ"),
  bstack1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫब"): bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬभ"),
  bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭म"): bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧय"),
  bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨर"): bstack1l_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऱ"),
  bstack1l_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫल"): bstack1l_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬळ"),
  bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬऴ"): bstack1l_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧव"),
  bstack1l_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨश"): bstack1l_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩष"),
  bstack1l_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬस"): bstack1l_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ह"),
  bstack1l_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫऺ"): bstack1l_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧऻ"),
  bstack1l_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫़ࠧ"): bstack1l_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩऽ"),
  bstack1l_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪा"): bstack1l_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫि"),
  bstack1l_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪी"): bstack1l_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫु"),
  bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू"): bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧृ"),
}
bstack1l11l1l_opy_ = bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧॄ")
bstack1l11l11_opy_ = bstack1l_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪॅ")
bstack1l1l1ll11_opy_ = bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬॆ")
bstack1l11l11ll_opy_ = {
  bstack1l_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫे"): 50,
  bstack1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩै"): 40,
  bstack1l_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬॉ"): 30,
  bstack1l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪॊ"): 20,
  bstack1l_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬो"): 10
}
bstack1lll1l11l_opy_ = bstack1l11l11ll_opy_[bstack1l_opy_ (u"ࠧࡪࡰࡩࡳࠬौ")]
bstack1lll1ll1l_opy_ = bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵्ࠧ")
bstack1l1l11111_opy_ = bstack1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧॎ")
bstack1l1llllll_opy_ = bstack1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩॏ")
bstack1ll1ll11_opy_ = bstack1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪॐ")
bstack11111lll_opy_ = [bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭॑"), bstack1l_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ॒࠭")]
bstack1ll1l11_opy_ = [bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॓"), bstack1l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॔")]
bstack1ll1lll1l_opy_ = [
  bstack1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪॕ"),
  bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬॖ"),
  bstack1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨॗ"),
  bstack1l_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩक़"),
  bstack1l_opy_ (u"࠭ࡡࡱࡲࠪख़"),
  bstack1l_opy_ (u"ࠧࡶࡦ࡬ࡨࠬग़"),
  bstack1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪज़"),
  bstack1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩड़"),
  bstack1l_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨढ़"),
  bstack1l_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩफ़"),
  bstack1l_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭य़"), bstack1l_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩॠ"),
  bstack1l_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪॡ"),
  bstack1l_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧॢ"),
  bstack1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ॣ"),
  bstack1l_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭।"),
  bstack1l_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬ॥"),
  bstack1l_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ०"), bstack1l_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪ१"), bstack1l_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ२"), bstack1l_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩ३"), bstack1l_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫ४"),
  bstack1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨ५"),
  bstack1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨ६"),
  bstack1l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧ७"), bstack1l_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪ८"),
  bstack1l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬ९"),
  bstack1l_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩ॰"),
  bstack1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨॱ"),
  bstack1l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫॲ"),
  bstack1l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩॳ"),
  bstack1l_opy_ (u"ࠬࡧࡶࡥࠩॴ"), bstack1l_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩॵ"), bstack1l_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩॶ"), bstack1l_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩॷ"),
  bstack1l_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧॸ"), bstack1l_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩॹ"), bstack1l_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧॺ"),
  bstack1l_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧॻ"), bstack1l_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫॼ"),
  bstack1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩॽ"), bstack1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫॾ"), bstack1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧॿ"), bstack1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬঀ"), bstack1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨঁ"),
  bstack1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨং"), bstack1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪঃ"),
  bstack1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩ঄"),
  bstack1l_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭অ"),
  bstack1l_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨআ"), bstack1l_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫই"), bstack1l_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩঈ"), bstack1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨউ"),
  bstack1l_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫঊ"),
  bstack1l_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩঋ"), bstack1l_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨঌ"),
  bstack1l_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩ঍"),
  bstack1l_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬ঎"),
  bstack1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭এ"),
  bstack1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঐ"),
  bstack1l_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧ঑"),
  bstack1l_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭঒"),
  bstack1l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩও"),
  bstack1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨঔ"),
  bstack1l_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧক"),
  bstack1l_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨখ"),
  bstack1l_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭গ"),
  bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬঘ"),
  bstack1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫঙ"),
  bstack1l_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨচ"),
  bstack1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧছ"),
  bstack1l_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧজ"),
  bstack1l_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫঝ"),
  bstack1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩঞ"), bstack1l_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪট"), bstack1l_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪঠ"),
  bstack1l_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬড"),
  bstack1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ঢ"),
  bstack1l_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬণ"),
  bstack1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭ত"),
  bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩথ"),
  bstack1l_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪদ"),
  bstack1l_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪধ"), bstack1l_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧন"), bstack1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬ঩"),
  bstack1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪপ"),
  bstack1l_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬফ"),
  bstack1l_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧব"),
  bstack1l_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ভ"),
  bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪম"), bstack1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧয"),
  bstack1l_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬর"), bstack1l_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧ঱"),
  bstack1l_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫল"),
  bstack1l_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫ঳"),
  bstack1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩ঴"), bstack1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫ঵"), bstack1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬশ"), bstack1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩষ"),
  bstack1l_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪস"),
  bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬহ"),
  bstack1l_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ঺"),
  bstack1l_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭঻"),
  bstack1l_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪ়ࠫ"),
  bstack1l_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪঽ"),
  bstack1l_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪা"), bstack1l_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫি"),
  bstack1l_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧী"),
  bstack1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬু"),
  bstack1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧূ"),
  bstack1l_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৃ"),
  bstack1l_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪৄ"),
  bstack1l_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬ৅"),
  bstack1l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫ৆"),
  bstack1l_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬে"),
  bstack1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬৈ"),
  bstack1l_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫ৉"),
  bstack1l_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬ৊"),
  bstack1l_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧো"),
  bstack1l_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨৌ"),
  bstack1l_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩ্ࠬ"),
  bstack1l_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭ৎ"),
  bstack1l_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨ৏"),
  bstack1l_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧ৐"),
  bstack1l_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨ৑"),
  bstack1l_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬ৒"),
  bstack1l_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨ৓"),
  bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭৔"),
  bstack1l_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ৕"), bstack1l_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬ৖"),
  bstack1l_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪৗ"), bstack1l_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨ৘"),
  bstack1l_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭৙"),
  bstack1l_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬ৚"),
  bstack1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬ৛"),
  bstack1l_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨড়"), bstack1l_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨঢ়"),
  bstack1l_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ৞"),
  bstack1l_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬয়"),
  bstack1l_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨৠ"),
  bstack1l_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪৡ"),
  bstack1l_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬৢ"),
  bstack1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧৣ"),
  bstack1l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪ৤"),
  bstack1l_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬ৥"),
  bstack1l_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩ০"),
  bstack1l_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧ১"), bstack1l_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭২"),
  bstack1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪ৩")
]
bstack111l1ll1_opy_ = bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ৪")
bstack1ll1l1l1l_opy_ = [bstack1l_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ৫"), bstack1l_opy_ (u"࠭࠮ࡢࡣࡥࠫ৬"), bstack1l_opy_ (u"ࠧ࠯࡫ࡳࡥࠬ৭")]
bstack1l11111l_opy_ = [bstack1l_opy_ (u"ࠨ࡫ࡧࠫ৮"), bstack1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৯"), bstack1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ৰ"), bstack1l_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪৱ")]
bstack1ll1lll11_opy_ = {
  bstack1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ৲"): bstack1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৳"),
  bstack1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ৴"): bstack1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭৵"),
  bstack1l_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৶"): bstack1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৷"),
  bstack1l_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৸"): bstack1l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৹"),
  bstack1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭৺"): bstack1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ৻")
}
bstack1l1l1ll1l_opy_ = [
  bstack1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ৼ"),
  bstack1l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ৽"),
  bstack1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৾"),
  bstack1l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ৿"),
  bstack1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭਀"),
]
bstack1ll1l111_opy_ = bstack11l11l1l_opy_ + bstack1ll1l111l_opy_ + bstack1ll1lll1l_opy_
bstack1lllll11_opy_ = [
  bstack1l_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫਁ"),
  bstack1l_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨਂ"),
  bstack1l_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧਃ"),
  bstack1l_opy_ (u"ࠩࡡ࠵࠵࠴ࠧ਄"),
  bstack1l_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩਅ"),
  bstack1l_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪਆ"),
  bstack1l_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫਇ"),
  bstack1l_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩਈ")
]
bstack11ll11ll_opy_ = bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀࠫਉ")
bstack1l11ll1l_opy_ = bstack1l_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧਊ")
bstack1llll1_opy_ = [ bstack1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ਋") ]
bstack1lll11l1l_opy_ = [ bstack1l_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ਌") ]
bstack11ll11_opy_ = [ bstack1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ਍") ]
bstack11llll1ll_opy_ = bstack1l_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧ਎")
bstack1l11ll_opy_ = bstack1l_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩਏ")
bstack1l11ll11_opy_ = bstack1l_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫਐ")
bstack11l1l1_opy_ = bstack1l_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ਑")
bstack1l1llll11_opy_ = [
  bstack1l_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭਒"),
  bstack1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪਓ"),
  bstack1l_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬਔ"),
  bstack1l_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫਕ"),
  bstack1l_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪਖ"),
  bstack1l_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨਗ"),
  bstack1l_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨਘ"),
  bstack1l_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫਙ"),
  bstack1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬਚ"),
  bstack1l_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਛ"),
  bstack1l_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ਜ"),
  bstack1l_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬਝ"),
  bstack1l_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪਞ"),
  bstack1l_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩਟ"),
  bstack1l_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ਠ"),
  bstack1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪਡ"),
  bstack1l_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧਢ"),
  bstack1l_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਣ"),
  bstack1l_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧਤ"),
  bstack1l_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ਥ"),
  bstack1l_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧਦ"),
]
def bstack1ll1lll1_opy_():
  global CONFIG
  headers = {
        bstack1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨਧ"): bstack1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ਨ"),
      }
  proxy = bstack1111lll1_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ਩")) or CONFIG.get(bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩਪ")):
    proxies = {
      bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬਫ"): proxy
    }
  try:
    response = requests.get(bstack1l1l1ll11_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1ll1l1lll_opy_ = response.json()[bstack1l_opy_ (u"ࠧࡩࡷࡥࡷࠬਬ")]
      logger.debug(bstack1l1ll1111_opy_.format(response.json()))
      return bstack1ll1l1lll_opy_
    else:
      logger.debug(bstack1l11lll11_opy_.format(bstack1l_opy_ (u"ࠣࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡎࡘࡕࡎࠡࡲࡤࡶࡸ࡫ࠠࡦࡴࡵࡳࡷࠦࠢਭ")))
  except Exception as e:
    logger.debug(bstack1l11lll11_opy_.format(e))
def bstack1l1llll_opy_(hub_url):
  global CONFIG
  url = bstack1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦਮ")+  hub_url + bstack1l_opy_ (u"ࠥ࠳ࡨ࡮ࡥࡤ࡭ࠥਯ")
  headers = {
        bstack1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪਰ"): bstack1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ਱"),
      }
  proxy = bstack1111lll1_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩਲ")) or CONFIG.get(bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫਲ਼")):
    proxies = {
      bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ਴"): proxy
    }
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l1lll1l1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l1l1lll1_opy_.format(hub_url, e))
def bstack1lllll_opy_():
  try:
    global bstack1ll11l_opy_
    bstack1ll1l1lll_opy_ = bstack1ll1lll1_opy_()
    with Pool() as pool:
      results = pool.map(bstack1l1llll_opy_, bstack1ll1l1lll_opy_)
    bstack1l111lll1_opy_ = {}
    for item in results:
      hub_url = item[bstack1l_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪਵ")]
      latency = item[bstack1l_opy_ (u"ࠪࡰࡦࡺࡥ࡯ࡥࡼࠫਸ਼")]
      bstack1l111lll1_opy_[hub_url] = latency
    bstack1ll1l1ll_opy_ = min(bstack1l111lll1_opy_, key= lambda x: bstack1l111lll1_opy_[x])
    bstack1ll11l_opy_ = bstack1ll1l1ll_opy_
    logger.debug(bstack1llllll1_opy_.format(bstack1ll1l1ll_opy_))
  except Exception as e:
    logger.debug(bstack1ll11l1l1_opy_.format(e))
bstack11l11l1_opy_ = bstack1l_opy_ (u"ࠫࡘ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠰ࠥࡻࡳࡪࡰࡪࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠺ࠡࡽࢀࠫ਷")
bstack1lll1ll11_opy_ = bstack1l_opy_ (u"ࠬࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡵࡨࡸࡺࡶࠡࠨਸ")
bstack1l1l11l1_opy_ = bstack1l_opy_ (u"࠭ࡐࡢࡴࡶࡩࡩࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠨਹ")
bstack1l111llll_opy_ = bstack1l_opy_ (u"ࠧࡔࡣࡱ࡭ࡹ࡯ࡺࡦࡦࠣࡧࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠬ਺")
bstack111l_opy_ = bstack1l_opy_ (u"ࠨࡗࡶ࡭ࡳ࡭ࠠࡩࡷࡥࠤࡺࡸ࡬࠻ࠢࡾࢁࠬ਻")
bstack111l11ll_opy_ = bstack1l_opy_ (u"ࠩࡖࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࡻࡾ਼ࠩ")
bstack1lll1l1l1_opy_ = bstack1l_opy_ (u"ࠪࡖࡪࡩࡥࡪࡸࡨࡨࠥ࡯࡮ࡵࡧࡵࡶࡺࡶࡴ࠭ࠢࡨࡼ࡮ࡺࡩ࡯ࡩࠪ਽")
bstack1llllllll_opy_ = bstack1l_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡡࠩਾ")
bstack1lll1111_opy_ = bstack1l_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡡ࡯ࡦࠣࡴࡾࡺࡥࡴࡶ࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡢࠪਿ")
bstack111111_opy_ = bstack1l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡳࡱࡥࡳࡹ࠲ࠠࡱࡣࡥࡳࡹࠦࡡ࡯ࡦࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࡱ࡯ࡢࡳࡣࡵࡽࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹࠠࡵࡱࠣࡶࡺࡴࠠࡳࡱࡥࡳࡹࠦࡴࡦࡵࡷࡷࠥ࡯࡮ࠡࡲࡤࡶࡦࡲ࡬ࡦ࡮࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠲ࡶࡡࡣࡱࡷࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡬ࡪࡤࡵࡥࡷࡿࡠࠨੀ")
bstack1lllll1_opy_ = bstack1l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡤࡨ࡬ࡦࡼࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡣࡧ࡫ࡥࡻ࡫ࡠࠨੁ")
bstack1llll_opy_ = bstack1l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡤࡴࡵ࡯ࡵ࡮࠯ࡦࡰ࡮࡫࡮ࡵࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡃࡳࡴ࡮ࡻ࡭࠮ࡒࡼࡸ࡭ࡵ࡮࠮ࡅ࡯࡭ࡪࡴࡴࡡࠩੂ")
bstack1ll111111_opy_ = bstack1l_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡣࠫ੃")
bstack1l1ll1lll_opy_ = bstack1l_opy_ (u"ࠪࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡦࡪࡰࡧࠤࡪ࡯ࡴࡩࡧࡵࠤࡘ࡫࡬ࡦࡰ࡬ࡹࡲࠦ࡯ࡳࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡶࡤࡰࡱࠦࡴࡩࡧࠣࡶࡪࡲࡥࡷࡣࡱࡸࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹࠠࡶࡵ࡬ࡲ࡬ࠦࡰࡪࡲࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠪ੄")
bstack1lllll1l_opy_ = bstack1l_opy_ (u"ࠫࡍࡧ࡮ࡥ࡮࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤ࡮ࡲࡷࡪ࠭੅")
bstack1llllll_opy_ = bstack1l_opy_ (u"ࠬࡇ࡬࡭ࠢࡧࡳࡳ࡫ࠡࠨ੆")
bstack1llll1ll_opy_ = bstack1l_opy_ (u"࠭ࡃࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࠥࡧࡴࠡࡣࡱࡽࠥࡶࡡࡳࡧࡱࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡱࡩࠤࠧࢁࡽࠣ࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡩ࡬ࡶࡦࡨࠤࡦࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭࠱ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡤࡱࡱࠦࡦࡪ࡮ࡨࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨࡲࡶࠥࡺࡥࡴࡶࡶ࠲ࠬੇ")
bstack1l1l1llll_opy_ = bstack1l_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤࡳࡵࡴࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡦࡪࡤࠡࡶ࡫ࡩࡲࠦࡩ࡯ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧࠣࡥࡸࠦࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤࠣࡥࡳࡪࠠࠣࡣࡦࡧࡪࡹࡳࡌࡧࡼࠦࠥࡵࡲࠡࡵࡨࡸࠥࡺࡨࡦ࡯ࠣࡥࡸࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࡹ࠺ࠡࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠥࠤࡦࡴࡤࠡࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠧ࠭ੈ")
bstack1l1l1l11_opy_ = bstack1l_opy_ (u"ࠨࡏࡤࡰ࡫ࡵࡲ࡮ࡧࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠼ࠥࡿࢂࠨࠧ੉")
bstack1lllll111_opy_ = bstack1l_opy_ (u"ࠩࡈࡲࡨࡵࡵ࡯ࡶࡨࡶࡪࡪࠠࡦࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡱࠢ࠰ࠤࢀࢃࠧ੊")
bstack1ll111_opy_ = bstack1l_opy_ (u"ࠪࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡑࡵࡣࡢ࡮ࠪੋ")
bstack1l1111l1l_opy_ = bstack1l_opy_ (u"ࠫࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯ࠫੌ")
bstack11l1ll1l_opy_ = bstack1l_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡑࡵࡣࡢ࡮ࠣ࡭ࡸࠦ࡮ࡰࡹࠣࡶࡺࡴ࡮ࡪࡰࡪ੍ࠥࠬ")
bstack1l1ll1_opy_ = bstack1l_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡶࡸࡦࡸࡴࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱࡀࠠࡼࡿࠪ੎")
bstack1l1l1ll_opy_ = bstack1l_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡯࡮ࡨࠢ࡯ࡳࡨࡧ࡬ࠡࡤ࡬ࡲࡦࡸࡹࠡࡹ࡬ࡸ࡭ࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࡽࢀࠫ੏")
bstack1l11111_opy_ = bstack1l_opy_ (u"ࠨࡗࡳࡨࡦࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠩ੐")
bstack1l1111ll_opy_ = bstack1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠨੑ")
bstack1llll1l1l_opy_ = bstack1l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣࡴࡷࡵࡶࡪࡦࡨࠤࡦࡴࠠࡢࡲࡳࡶࡴࡶࡲࡪࡣࡷࡩࠥࡌࡗࠡࠪࡵࡳࡧࡵࡴ࠰ࡲࡤࡦࡴࡺࠩࠡ࡫ࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠮ࠣࡷࡰ࡯ࡰࠡࡶ࡫ࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡭ࡨࡽࠥ࡯࡮ࠡࡥࡲࡲ࡫࡯ࡧࠡ࡫ࡩࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡹࡩ࡮ࡲ࡯ࡩࠥࡶࡹࡵࡪࡲࡲࠥࡹࡣࡳ࡫ࡳࡸࠥࡽࡩࡵࡪࡲࡹࡹࠦࡡ࡯ࡻࠣࡊ࡜࠴ࠧ੒")
bstack1l1ll1l_opy_ = bstack1l_opy_ (u"ࠫࡘ࡫ࡴࡵ࡫ࡱ࡫ࠥ࡮ࡴࡵࡲࡓࡶࡴࡾࡹ࠰ࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡱࡱࠤࡨࡻࡲࡳࡧࡱࡸࡱࡿࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠣࡺࡪࡸࡳࡪࡱࡱࠤࡴ࡬ࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࠫࡿࢂ࠯ࠬࠡࡲ࡯ࡩࡦࡹࡥࠡࡷࡳ࡫ࡷࡧࡤࡦࠢࡷࡳ࡙ࠥࡥ࡭ࡧࡱ࡭ࡺࡳ࠾࠾࠶࠱࠴࠳࠶ࠠࡰࡴࠣࡶࡪ࡬ࡥࡳࠢࡷࡳࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠰ࡴࡸࡲ࠲ࡺࡥࡴࡶࡶ࠱ࡧ࡫ࡨࡪࡰࡧ࠱ࡵࡸ࡯ࡹࡻࠦࡴࡾࡺࡨࡰࡰࠣࡪࡴࡸࠠࡢࠢࡺࡳࡷࡱࡡࡳࡱࡸࡲࡩ࠴ࠧ੓")
bstack1l11llll_opy_ = bstack1l_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡻࡰࡰࠥ࡬ࡩ࡭ࡧ࠱࠲ࠬ੔")
bstack1111ll11_opy_ = bstack1l_opy_ (u"࠭ࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡶ࡫ࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠤࠫ੕")
bstack11ll1l1l_opy_ = bstack1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪ࠴ࠠࡼࡿࠪ੖")
bstack11lllll11_opy_ = bstack1l_opy_ (u"ࠨࡇࡻࡴࡪࡩࡴࡦࡦࠣࡥࡹࠦ࡬ࡦࡣࡶࡸࠥ࠷ࠠࡪࡰࡳࡹࡹ࠲ࠠࡳࡧࡦࡩ࡮ࡼࡥࡥࠢ࠳ࠫ੗")
bstack1ll1llll1_opy_ = bstack1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡦࡸࡶ࡮ࡴࡧࠡࡃࡳࡴࠥࡻࡰ࡭ࡱࡤࡨ࠳ࠦࡻࡾࠩ੘")
bstack1l1lll_opy_ = bstack1l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱ࡮ࡲࡥࡩࠦࡁࡱࡲ࠱ࠤࡎࡴࡶࡢ࡮࡬ࡨࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡿࢂ࠴ࠧਖ਼")
bstack111l1l1l_opy_ = bstack1l_opy_ (u"ࠫࡐ࡫ࡹࡴࠢࡦࡥࡳࡴ࡯ࡵࠢࡦࡳ࠲࡫ࡸࡪࡵࡷࠤࡦࡹࠠࡢࡲࡳࠤࡻࡧ࡬ࡶࡧࡶ࠰ࠥࡻࡳࡦࠢࡤࡲࡾࠦ࡯࡯ࡧࠣࡴࡷࡵࡰࡦࡴࡷࡽࠥ࡬ࡲࡰ࡯ࠣࡿ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡳࡥࡹ࡮࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡴࡪࡤࡶࡪࡧࡢ࡭ࡧࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࡽ࠭ࠢࡲࡲࡱࡿࠠࠣࡲࡤࡸ࡭ࠨࠠࡢࡰࡧࠤࠧࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠣࠢࡦࡥࡳࠦࡣࡰ࠯ࡨࡼ࡮ࡹࡴࠡࡶࡲ࡫ࡪࡺࡨࡦࡴ࠱ࠫਗ਼")
bstack1lll11l1_opy_ = bstack1l_opy_ (u"ࠬࡡࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡢࡲࡳࠤࡵࡸ࡯ࡱࡧࡵࡸࡾࡣࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠠࡢࡴࡨࠤࢀ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡴࡦࡺࡨ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡵ࡫ࡥࡷ࡫ࡡࡣ࡮ࡨࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾ࡾ࠰ࠣࡊࡴࡸࠠ࡮ࡱࡵࡩࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡰ࡭ࡧࡤࡷࡪࠦࡶࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵࡶࡩࡶ࡯࠲ࡷࡪࡺ࠭ࡶࡲ࠰ࡸࡪࡹࡴࡴ࠱ࡶࡴࡪࡩࡩࡧࡻ࠰ࡥࡵࡶࠧਜ਼")
bstack1l11l1l11_opy_ = bstack1l_opy_ (u"࡛࠭ࡊࡰࡹࡥࡱ࡯ࡤࠡࡣࡳࡴࠥࡶࡲࡰࡲࡨࡶࡹࡿ࡝ࠡࡕࡸࡴࡵࡵࡲࡵࡧࡧࠤࡻࡧ࡬ࡶࡧࡶࠤࡴ࡬ࠠࡢࡲࡳࠤࡦࡸࡥࠡࡱࡩࠤࢀ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡴࡦࡺࡨ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡵ࡫ࡥࡷ࡫ࡡࡣ࡮ࡨࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾ࡾ࠰ࠣࡊࡴࡸࠠ࡮ࡱࡵࡩࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡰ࡭ࡧࡤࡷࡪࠦࡶࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵࡶࡩࡶ࡯࠲ࡷࡪࡺ࠭ࡶࡲ࠰ࡸࡪࡹࡴࡴ࠱ࡶࡴࡪࡩࡩࡧࡻ࠰ࡥࡵࡶࠧੜ")
bstack1l111l11_opy_ = bstack1l_opy_ (u"ࠧࡖࡵ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡣࡳࡴࠥ࡯ࡤࠡࡽࢀࠤ࡫ࡵࡲࠡࡪࡤࡷ࡭ࠦ࠺ࠡࡽࢀ࠲ࠬ੝")
bstack1l11ll1ll_opy_ = bstack1l_opy_ (u"ࠨࡃࡳࡴ࡛ࠥࡰ࡭ࡱࡤࡨࡪࡪࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾ࠴ࠠࡊࡆࠣ࠾ࠥࢁࡽࠨਫ਼")
bstack1lll11_opy_ = bstack1l_opy_ (u"ࠩࡘࡷ࡮ࡴࡧࠡࡃࡳࡴࠥࡀࠠࡼࡿ࠱ࠫ੟")
bstack1l11ll111_opy_ = bstack1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡰࡴࠣࡺࡦࡴࡩ࡭࡮ࡤࠤࡵࡿࡴࡩࡱࡱࠤࡹ࡫ࡳࡵࡵ࠯ࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡽࡩࡵࡪࠣࡴࡦࡸࡡ࡭࡮ࡨࡰࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡀࠤ࠶࠭੠")
bstack1ll1ll1ll_opy_ = bstack1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࠽ࠤࢀࢃࠧ੡")
bstack111l11l1_opy_ = bstack1l_opy_ (u"ࠬࡉ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡥ࡯ࡳࡸ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲ࠻ࠢࡾࢁࠬ੢")
bstack1ll11l11l_opy_ = bstack1l_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡪࡩࡹࠦࡲࡦࡣࡶࡳࡳࠦࡦࡰࡴࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡪࡧࡴࡶࡴࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩ࠳ࠦࡻࡾࠩ੣")
bstack1ll1l1_opy_ = bstack1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡨࡵࡳࡲࠦࡡࡱ࡫ࠣࡧࡦࡲ࡬࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ੤")
bstack1l1l1111l_opy_ = bstack1l_opy_ (u"ࠨࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡮࡯ࡸࠢࡥࡹ࡮ࡲࡤࠡࡗࡕࡐ࠱ࠦࡡࡴࠢࡥࡹ࡮ࡲࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠥ࡯ࡳࠡࡰࡲࡸࠥࡻࡳࡦࡦ࠱ࠫ੥")
bstack11l11111_opy_ = bstack1l_opy_ (u"ࠩࡖࡩࡷࡼࡥࡳࠢࡶ࡭ࡩ࡫ࠠࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠫࡿࢂ࠯ࠠࡪࡵࠣࡲࡴࡺࠠࡴࡣࡰࡩࠥࡧࡳࠡࡥ࡯࡭ࡪࡴࡴࠡࡵ࡬ࡨࡪࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠪࡾࢁ࠮࠭੦")
bstack111lllll_opy_ = bstack1l_opy_ (u"࡚ࠪ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡰࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡧࡥࡸ࡮ࡢࡰࡣࡵࡨ࠿ࠦࡻࡾࠩ੧")
bstack11111l1_opy_ = bstack1l_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡢࡥࡦࡩࡸࡹࠠࡢࠢࡳࡶ࡮ࡼࡡࡵࡧࠣࡨࡴࡳࡡࡪࡰ࠽ࠤࢀࢃࠠ࠯ࠢࡖࡩࡹࠦࡴࡩࡧࠣࡪࡴࡲ࡬ࡰࡹ࡬ࡲ࡬ࠦࡣࡰࡰࡩ࡭࡬ࠦࡩ࡯ࠢࡼࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥ࠻ࠢ࡟ࡲ࠲࠳࠭࠮࠯࠰࠱࠲࠳࠭࠮ࠢ࡟ࡲࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭࠼ࠣࡸࡷࡻࡥࠡ࡞ࡱ࠱࠲࠳࠭࠮࠯࠰࠱࠲࠳࠭ࠨ੨")
bstack1lllll1ll_opy_ = bstack1l_opy_ (u"࡙ࠬ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࡡࡨࡶࡷࡵࡲࠡ࠼ࠣࡿࢂ࠭੩")
bstack1l111111l_opy_ = bstack1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡲࡩࡥࡡ࡮ࡲ࡯࡭ࡹࡻࡤࡦࡡࡨࡺࡪࡴࡴࠡࡨࡲࡶ࡙ࠥࡄࡌࡕࡨࡸࡺࡶࠠࡼࡿࠥ੪")
bstack11l1l11_opy_ = bstack1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡳࡪ࡟ࡢ࡯ࡳࡰ࡮ࡺࡵࡥࡧࡢࡩࡻ࡫࡮ࡵࠢࡩࡳࡷࠦࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠢࡾࢁࠧ੫")
bstack1l1l11lll_opy_ = bstack1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠࡣࡰࡴࡱ࡯ࡴࡶࡦࡨࡣࡪࡼࡥ࡯ࡶࠣࡪࡴࡸࠠࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠤࢀࢃࠢ੬")
bstack111lll_opy_ = bstack1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡫࡯ࡲࡦࡡࡵࡩࡶࡻࡥࡴࡶࠣࡿࢂࠨ੭")
bstack1l1ll11_opy_ = bstack1l_opy_ (u"ࠥࡔࡔ࡙ࡔࠡࡇࡹࡩࡳࡺࠠࡼࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥࡀࠠࡼࡿࠥ੮")
bstack111lll1_opy_ = bstack1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࠣࡴࡷࡵࡸࡺࠢࡶࡩࡹࡺࡩ࡯ࡩࡶ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ੯")
bstack1l1ll1111_opy_ = bstack1l_opy_ (u"ࠬࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥ࠵࡮ࡦࡺࡷࡣ࡭ࡻࡢࡴࠢࡾࢁࠬੰ")
bstack1l11lll11_opy_ = bstack1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢ࠲ࡲࡪࡾࡴࡠࡪࡸࡦࡸࡀࠠࡼࡿࠪੱ")
bstack1llllll1_opy_ = bstack1l_opy_ (u"ࠧࡏࡧࡤࡶࡪࡹࡴࠡࡪࡸࡦࠥࡧ࡬࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡶ࠾ࠥࢁࡽࠨੲ")
bstack1l1ll_opy_ = bstack1l_opy_ (u"ࠨࡇࡕࡖࡔࡘࠠࡊࡐࠣࡅࡑࡒࡏࡄࡃࡗࡉࠥࡎࡕࡃࠢࡾࢁࠬੳ")
bstack1l1lll1l1_opy_ = bstack1l_opy_ (u"ࠩࡏࡥࡹ࡫࡮ࡤࡻࠣࡳ࡫ࠦࡨࡶࡤ࠽ࠤࢀࢃࠠࡪࡵ࠽ࠤࢀࢃࠧੴ")
bstack1l1l1lll1_opy_ = bstack1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦ࡬ࡢࡶࡨࡲࡨࡿࠠࡧࡱࡵࠤࢀࢃࠠࡩࡷࡥ࠾ࠥࢁࡽࠨੵ")
bstack11l11l_opy_ = bstack1l_opy_ (u"ࠫࡍࡻࡢࠡࡷࡵࡰࠥࡩࡨࡢࡰࡪࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥ࠾ࠥࢁࡽࠨ੶")
bstack1ll111l11_opy_ = bstack1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡹ࡮ࡥࠡࡱࡳࡸ࡮ࡳࡡ࡭ࠢ࡫ࡹࡧࠦࡵࡳ࡮࠽ࠤࢀࢃࠧ੷")
bstack1l11_opy_ = bstack1l_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭੸")
bstack1l1l11l11_opy_ = bstack1l_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭੹")
from ._version import __version__
bstack111l1lll_opy_ = None
CONFIG = {}
bstack1ll11l111_opy_ = {}
bstack1llll1ll1_opy_ = {}
bstack1llll111l_opy_ = None
bstack1l1ll11l1_opy_ = None
bstack11lll11l_opy_ = None
bstack1lll1l11_opy_ = -1
bstack1ll11ll11_opy_ = bstack1lll1l11l_opy_
bstack1l111ll1l_opy_ = 1
bstack1lllll1l1_opy_ = False
bstack11ll1l11_opy_ = bstack1l_opy_ (u"ࠨࠩ੺")
bstack1ll11111l_opy_ = bstack1l_opy_ (u"ࠩࠪ੻")
bstack11ll1lll_opy_ = False
bstack1ll111lll_opy_ = True
bstack1l1l1lll_opy_ = bstack1l_opy_ (u"ࠪࠫ੼")
bstack1ll111ll1_opy_ = []
bstack1ll11l_opy_ = bstack1l_opy_ (u"ࠫࠬ੽")
bstack11ll1111_opy_ = False
bstack1ll11_opy_ = False
bstack111111l1_opy_ = None
bstack111llll_opy_ = None
bstack1111111l_opy_ = None
bstack111111l_opy_ = None
bstack1ll11l1l_opy_ = None
bstack11ll111l_opy_ = None
bstack1l11l111_opy_ = None
bstack11ll_opy_ = None
bstack1111l1ll_opy_ = None
bstack1ll1111l_opy_ = None
bstack1l1111l1_opy_ = None
bstack111ll1l1_opy_ = None
bstack1lll1l_opy_ = bstack1l_opy_ (u"ࠧࠨ੾")
class bstack1ll11lll_opy_(threading.Thread):
  def run(self):
    self.exc = None
    try:
      self.ret = self._target(*self._args, **self._kwargs)
    except Exception as e:
      self.exc = e
  def join(self, timeout=None):
    super(bstack1ll11lll_opy_, self).join(timeout)
    if self.exc:
      raise self.exc
    return self.ret
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1ll11ll11_opy_,
                    format=bstack1l_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫ੿"),
                    datefmt=bstack1l_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ઀"))
def bstack1ll1ll11l_opy_():
  global CONFIG
  global bstack1ll11ll11_opy_
  if bstack1l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪઁ") in CONFIG:
    bstack1ll11ll11_opy_ = bstack1l11l11ll_opy_[CONFIG[bstack1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫં")]]
    logging.getLogger().setLevel(bstack1ll11ll11_opy_)
def bstack1ll1111l1_opy_():
  global CONFIG
  global bstack1ll11_opy_
  bstack1l1l11l_opy_ = bstack11l11ll_opy_(CONFIG)
  if(bstack1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬઃ") in bstack1l1l11l_opy_ and str(bstack1l1l11l_opy_[bstack1l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭઄")]).lower() == bstack1l_opy_ (u"ࠬࡺࡲࡶࡧࠪઅ")):
    bstack1ll11_opy_ = True
def bstack1111l1l1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll1l1111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll11llll_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1l_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡣࡰࡰࡩ࡭࡬࡬ࡩ࡭ࡧࠥઆ") == args[i].lower() or bstack1l_opy_ (u"ࠢ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡲ࡫࡯ࡧࠣઇ") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1l1lll_opy_
      bstack1l1l1lll_opy_ += bstack1l_opy_ (u"ࠨ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡅࡲࡲ࡫࡯ࡧࡇ࡫࡯ࡩࠥ࠭ઈ") + path
      return path
  return None
def bstack1ll1l1ll1_opy_():
  bstack1l111l1_opy_ = bstack1ll11llll_opy_()
  if bstack1l111l1_opy_ and os.path.exists(os.path.abspath(bstack1l111l1_opy_)):
    fileName = bstack1l111l1_opy_
  if bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭ઉ") in os.environ and os.path.exists(os.path.abspath(os.environ[bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧઊ")])) and not bstack1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࠭ઋ") in locals():
    fileName = os.environ[bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆࠩઌ")]
  if bstack1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨઍ") in locals():
    bstack1l1lll11l_opy_ = os.path.abspath(fileName)
  else:
    bstack1l1lll11l_opy_ = bstack1l_opy_ (u"ࠧࠨ઎")
  bstack1ll11111_opy_ = os.getcwd()
  bstack11l11lll_opy_ = bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫએ")
  bstack1l11ll1_opy_ = bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡤࡱࡱ࠭ઐ")
  while (not os.path.exists(bstack1l1lll11l_opy_)) and bstack1ll11111_opy_ != bstack1l_opy_ (u"ࠥࠦઑ"):
    bstack1l1lll11l_opy_ = os.path.join(bstack1ll11111_opy_, bstack11l11lll_opy_)
    if not os.path.exists(bstack1l1lll11l_opy_):
      bstack1l1lll11l_opy_ = os.path.join(bstack1ll11111_opy_, bstack1l11ll1_opy_)
    if bstack1ll11111_opy_ != os.path.dirname(bstack1ll11111_opy_):
      bstack1ll11111_opy_ = os.path.dirname(bstack1ll11111_opy_)
    else:
      bstack1ll11111_opy_ = bstack1l_opy_ (u"ࠦࠧ઒")
  if not os.path.exists(bstack1l1lll11l_opy_):
    bstack1l1lll1ll_opy_(
      bstack1llll1ll_opy_.format(os.getcwd()))
  with open(bstack1l1lll11l_opy_, bstack1l_opy_ (u"ࠬࡸࠧઓ")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack1l1lll1ll_opy_(bstack1l1l1l11_opy_.format(str(exc)))
def bstack11lllllll_opy_(config):
  bstack111111ll_opy_ = bstack1l1111l11_opy_(config)
  for option in list(bstack111111ll_opy_):
    if option.lower() in bstack1l11l1ll1_opy_ and option != bstack1l11l1ll1_opy_[option.lower()]:
      bstack111111ll_opy_[bstack1l11l1ll1_opy_[option.lower()]] = bstack111111ll_opy_[option]
      del bstack111111ll_opy_[option]
  return config
def bstack1111l11l_opy_():
  global bstack1llll1ll1_opy_
  for key, bstack1ll11l1ll_opy_ in bstack111l1l11_opy_.items():
    if isinstance(bstack1ll11l1ll_opy_, list):
      for var in bstack1ll11l1ll_opy_:
        if var in os.environ:
          bstack1llll1ll1_opy_[key] = os.environ[var]
          break
    elif bstack1ll11l1ll_opy_ in os.environ:
      bstack1llll1ll1_opy_[key] = os.environ[bstack1ll11l1ll_opy_]
  if bstack1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨઔ") in os.environ:
    bstack1llll1ll1_opy_[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫક")] = {}
    bstack1llll1ll1_opy_[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬખ")][bstack1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫગ")] = os.environ[bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬઘ")]
def bstack11l1l1ll_opy_():
  global bstack1ll11l111_opy_
  global bstack1l1l1lll_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstack1l_opy_ (u"ࠫ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧઙ").lower() == val.lower():
      bstack1ll11l111_opy_[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩચ")] = {}
      bstack1ll11l111_opy_[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪછ")][bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩજ")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack111l1_opy_ in bstack1lllll11l_opy_.items():
    if isinstance(bstack111l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack111l1_opy_:
          if idx<len(sys.argv) and bstack1l_opy_ (u"ࠨ࠯࠰ࠫઝ") + var.lower() == val.lower() and not key in bstack1ll11l111_opy_:
            bstack1ll11l111_opy_[key] = sys.argv[idx+1]
            bstack1l1l1lll_opy_ += bstack1l_opy_ (u"ࠩࠣ࠱࠲࠭ઞ") + var + bstack1l_opy_ (u"ࠪࠤࠬટ") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstack1l_opy_ (u"ࠫ࠲࠳ࠧઠ") + bstack111l1_opy_.lower() == val.lower() and not key in bstack1ll11l111_opy_:
          bstack1ll11l111_opy_[key] = sys.argv[idx+1]
          bstack1l1l1lll_opy_ += bstack1l_opy_ (u"ࠬࠦ࠭࠮ࠩડ") + bstack111l1_opy_ + bstack1l_opy_ (u"࠭ࠠࠨઢ") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack1l111_opy_(config):
  bstack1ll1l11l_opy_ = config.keys()
  for bstack1ll111l_opy_, bstack11l1lll1_opy_ in bstack1l1l111ll_opy_.items():
    if bstack11l1lll1_opy_ in bstack1ll1l11l_opy_:
      config[bstack1ll111l_opy_] = config[bstack11l1lll1_opy_]
      del config[bstack11l1lll1_opy_]
  for bstack1ll111l_opy_, bstack11l1lll1_opy_ in bstack1l1111111_opy_.items():
    if isinstance(bstack11l1lll1_opy_, list):
      for bstack11lllll1l_opy_ in bstack11l1lll1_opy_:
        if bstack11lllll1l_opy_ in bstack1ll1l11l_opy_:
          config[bstack1ll111l_opy_] = config[bstack11lllll1l_opy_]
          del config[bstack11lllll1l_opy_]
          break
    elif bstack11l1lll1_opy_ in bstack1ll1l11l_opy_:
        config[bstack1ll111l_opy_] = config[bstack11l1lll1_opy_]
        del config[bstack11l1lll1_opy_]
  for bstack11lllll1l_opy_ in list(config):
    for bstack11lll1l_opy_ in bstack1ll1l111_opy_:
      if bstack11lllll1l_opy_.lower() == bstack11lll1l_opy_.lower() and bstack11lllll1l_opy_ != bstack11lll1l_opy_:
        config[bstack11lll1l_opy_] = config[bstack11lllll1l_opy_]
        del config[bstack11lllll1l_opy_]
  bstack1l11l_opy_ = []
  if bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪણ") in config:
    bstack1l11l_opy_ = config[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫત")]
  for platform in bstack1l11l_opy_:
    for bstack11lllll1l_opy_ in list(platform):
      for bstack11lll1l_opy_ in bstack1ll1l111_opy_:
        if bstack11lllll1l_opy_.lower() == bstack11lll1l_opy_.lower() and bstack11lllll1l_opy_ != bstack11lll1l_opy_:
          platform[bstack11lll1l_opy_] = platform[bstack11lllll1l_opy_]
          del platform[bstack11lllll1l_opy_]
  for bstack1ll111l_opy_, bstack11l1lll1_opy_ in bstack1l1111111_opy_.items():
    for platform in bstack1l11l_opy_:
      if isinstance(bstack11l1lll1_opy_, list):
        for bstack11lllll1l_opy_ in bstack11l1lll1_opy_:
          if bstack11lllll1l_opy_ in platform:
            platform[bstack1ll111l_opy_] = platform[bstack11lllll1l_opy_]
            del platform[bstack11lllll1l_opy_]
            break
      elif bstack11l1lll1_opy_ in platform:
        platform[bstack1ll111l_opy_] = platform[bstack11l1lll1_opy_]
        del platform[bstack11l1lll1_opy_]
  for bstack1l1l11ll_opy_ in bstack1ll1lll11_opy_:
    if bstack1l1l11ll_opy_ in config:
      if not bstack1ll1lll11_opy_[bstack1l1l11ll_opy_] in config:
        config[bstack1ll1lll11_opy_[bstack1l1l11ll_opy_]] = {}
      config[bstack1ll1lll11_opy_[bstack1l1l11ll_opy_]].update(config[bstack1l1l11ll_opy_])
      del config[bstack1l1l11ll_opy_]
  for platform in bstack1l11l_opy_:
    for bstack1l1l11ll_opy_ in bstack1ll1lll11_opy_:
      if bstack1l1l11ll_opy_ in list(platform):
        if not bstack1ll1lll11_opy_[bstack1l1l11ll_opy_] in platform:
          platform[bstack1ll1lll11_opy_[bstack1l1l11ll_opy_]] = {}
        platform[bstack1ll1lll11_opy_[bstack1l1l11ll_opy_]].update(platform[bstack1l1l11ll_opy_])
        del platform[bstack1l1l11ll_opy_]
  config = bstack11lllllll_opy_(config)
  return config
def bstack1l11l1ll_opy_(config):
  global bstack1ll11111l_opy_
  if bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭થ") in config and str(config[bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧદ")]).lower() != bstack1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪધ"):
    if not bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩન") in config:
      config[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ઩")] = {}
    if not bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩપ") in config[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬફ")]:
      bstack1lll11ll_opy_ = datetime.datetime.now()
      bstack1llll11l_opy_ = bstack1lll11ll_opy_.strftime(bstack1l_opy_ (u"ࠩࠨࡨࡤࠫࡢࡠࠧࡋࠩࡒ࠭બ"))
      hostname = socket.gethostname()
      bstack1l11lll1l_opy_ = bstack1l_opy_ (u"ࠪࠫભ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l_opy_ (u"ࠫࢀࢃ࡟ࡼࡿࡢࡿࢂ࠭મ").format(bstack1llll11l_opy_, hostname, bstack1l11lll1l_opy_)
      config[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩય")][bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨર")] = identifier
    bstack1ll11111l_opy_ = config[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ઱")][bstack1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪલ")]
  return config
def bstack1ll11l11_opy_():
  if (
    isinstance(os.getenv(bstack1l_opy_ (u"ࠩࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠧળ")), str) and len(os.getenv(bstack1l_opy_ (u"ࠪࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠨ઴"))) > 0
  ) or (
    isinstance(os.getenv(bstack1l_opy_ (u"ࠫࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠪવ")), str) and len(os.getenv(bstack1l_opy_ (u"ࠬࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠫશ"))) > 0
  ):
    return os.getenv(bstack1l_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬષ"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠧࡄࡋࠪસ"))).lower() == bstack1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭હ") and str(os.getenv(bstack1l_opy_ (u"ࠩࡆࡍࡗࡉࡌࡆࡅࡌࠫ઺"))).lower() == bstack1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ઻"):
    return os.getenv(bstack1l_opy_ (u"ࠫࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓ઼ࠧ"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠬࡉࡉࠨઽ"))).lower() == bstack1l_opy_ (u"࠭ࡴࡳࡷࡨࠫા") and str(os.getenv(bstack1l_opy_ (u"ࠧࡕࡔࡄ࡚ࡎ࡙ࠧિ"))).lower() == bstack1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ી"):
    return os.getenv(bstack1l_opy_ (u"ࠩࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨુ"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠪࡇࡎ࠭ૂ"))).lower() == bstack1l_opy_ (u"ࠫࡹࡸࡵࡦࠩૃ") and str(os.getenv(bstack1l_opy_ (u"ࠬࡉࡉࡠࡐࡄࡑࡊ࠭ૄ"))).lower() == bstack1l_opy_ (u"࠭ࡣࡰࡦࡨࡷ࡭࡯ࡰࠨૅ"):
    return 0 # bstack1ll1ll_opy_ bstack11l1111_opy_ not set build number env
  if os.getenv(bstack1l_opy_ (u"ࠧࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠪ૆")) and os.getenv(bstack1l_opy_ (u"ࠨࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠫે")):
    return os.getenv(bstack1l_opy_ (u"ࠩࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫૈ"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠪࡇࡎ࠭ૉ"))).lower() == bstack1l_opy_ (u"ࠫࡹࡸࡵࡦࠩ૊") and str(os.getenv(bstack1l_opy_ (u"ࠬࡊࡒࡐࡐࡈࠫો"))).lower() == bstack1l_opy_ (u"࠭ࡴࡳࡷࡨࠫૌ"):
    return os.getenv(bstack1l_opy_ (u"ࠧࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖ્ࠬ"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠨࡅࡌࠫ૎"))).lower() == bstack1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ૏") and str(os.getenv(bstack1l_opy_ (u"ࠪࡗࡊࡓࡁࡑࡊࡒࡖࡊ࠭ૐ"))).lower() == bstack1l_opy_ (u"ࠫࡹࡸࡵࡦࠩ૑"):
    return os.getenv(bstack1l_opy_ (u"࡙ࠬࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠨ૒"), 0)
  if str(os.getenv(bstack1l_opy_ (u"࠭ࡃࡊࠩ૓"))).lower() == bstack1l_opy_ (u"ࠧࡵࡴࡸࡩࠬ૔") and str(os.getenv(bstack1l_opy_ (u"ࠨࡉࡌࡘࡑࡇࡂࡠࡅࡌࠫ૕"))).lower() == bstack1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ૖"):
    return os.getenv(bstack1l_opy_ (u"ࠪࡇࡎࡥࡊࡐࡄࡢࡍࡉ࠭૗"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠫࡈࡏࠧ૘"))).lower() == bstack1l_opy_ (u"ࠬࡺࡲࡶࡧࠪ૙") and str(os.getenv(bstack1l_opy_ (u"࠭ࡂࡖࡋࡏࡈࡐࡏࡔࡆࠩ૚"))).lower() == bstack1l_opy_ (u"ࠧࡵࡴࡸࡩࠬ૛"):
    return os.getenv(bstack1l_opy_ (u"ࠨࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠪ૜"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠩࡗࡊࡤࡈࡕࡊࡎࡇࠫ૝"))).lower() == bstack1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ૞"):
    return os.getenv(bstack1l_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠫ૟"), 0)
  return -1
def bstack1ll1l1l11_opy_(bstack1l11l1l1_opy_):
  global CONFIG
  if not bstack1l_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧૠ") in CONFIG[bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨૡ")]:
    return
  CONFIG[bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩૢ")] = CONFIG[bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪૣ")].replace(
    bstack1l_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫ૤"),
    str(bstack1l11l1l1_opy_)
  )
def bstack1l1lll1_opy_():
  global CONFIG
  if not bstack1l_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩ૥") in CONFIG[bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૦")]:
    return
  bstack1lll11ll_opy_ = datetime.datetime.now()
  bstack1llll11l_opy_ = bstack1lll11ll_opy_.strftime(bstack1l_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪ૧"))
  CONFIG[bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૨")] = CONFIG[bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૩")].replace(
    bstack1l_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧ૪"),
    bstack1llll11l_opy_
  )
def bstack1lll1ll1_opy_():
  global CONFIG
  if bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૫") in CONFIG and not bool(CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૬")]):
    del CONFIG[bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૭")]
    return
  if not bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૮") in CONFIG:
    CONFIG[bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૯")] = bstack1l_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪ૰")
  if bstack1l_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧ૱") in CONFIG[bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૲")]:
    bstack1l1lll1_opy_()
    os.environ[bstack1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧ૳")] = CONFIG[bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૴")]
  if not bstack1l_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧ૵") in CONFIG[bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૶")]:
    return
  bstack1l11l1l1_opy_ = bstack1l_opy_ (u"ࠧࠨ૷")
  bstack1l1111lll_opy_ = bstack1ll11l11_opy_()
  if bstack1l1111lll_opy_ != -1:
    bstack1l11l1l1_opy_ = bstack1l_opy_ (u"ࠨࡅࡌࠤࠬ૸") + str(bstack1l1111lll_opy_)
  if bstack1l11l1l1_opy_ == bstack1l_opy_ (u"ࠩࠪૹ"):
    bstack11lll111_opy_ = bstack1l1l111_opy_(CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ૺ")])
    if bstack11lll111_opy_ != -1:
      bstack1l11l1l1_opy_ = str(bstack11lll111_opy_)
  if bstack1l11l1l1_opy_:
    bstack1ll1l1l11_opy_(bstack1l11l1l1_opy_)
    os.environ[bstack1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨૻ")] = CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧૼ")]
def bstack1llll1lll_opy_(bstack1111llll_opy_, bstack1l1l1l1ll_opy_, path):
  bstack11111111_opy_ = {
    bstack1l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૽"): bstack1l1l1l1ll_opy_
  }
  if os.path.exists(path):
    bstack11l1lll_opy_ = json.load(open(path, bstack1l_opy_ (u"ࠧࡳࡤࠪ૾")))
  else:
    bstack11l1lll_opy_ = {}
  bstack11l1lll_opy_[bstack1111llll_opy_] = bstack11111111_opy_
  with open(path, bstack1l_opy_ (u"ࠣࡹ࠮ࠦ૿")) as outfile:
    json.dump(bstack11l1lll_opy_, outfile)
def bstack1l1l111_opy_(bstack1111llll_opy_):
  bstack1111llll_opy_ = str(bstack1111llll_opy_)
  bstack11ll1ll1_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠩࢁࠫ଀")), bstack1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪଁ"))
  try:
    if not os.path.exists(bstack11ll1ll1_opy_):
      os.makedirs(bstack11ll1ll1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠫࢃ࠭ଂ")), bstack1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬଃ"), bstack1l_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨ଄"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l_opy_ (u"ࠧࡸࠩଅ")):
        pass
      with open(file_path, bstack1l_opy_ (u"ࠣࡹ࠮ࠦଆ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l_opy_ (u"ࠩࡵࠫଇ")) as bstack11llllll1_opy_:
      bstack11llll1l_opy_ = json.load(bstack11llllll1_opy_)
    if bstack1111llll_opy_ in bstack11llll1l_opy_:
      bstack11l1l11l_opy_ = bstack11llll1l_opy_[bstack1111llll_opy_][bstack1l_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧଈ")]
      bstack11111ll_opy_ = int(bstack11l1l11l_opy_) + 1
      bstack1llll1lll_opy_(bstack1111llll_opy_, bstack11111ll_opy_, file_path)
      return bstack11111ll_opy_
    else:
      bstack1llll1lll_opy_(bstack1111llll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1ll1ll1ll_opy_.format(str(e)))
    return -1
def bstack1l111ll1_opy_(config):
  if not config[bstack1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ଉ")] or not config[bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨଊ")]:
    return True
  else:
    return False
def bstack11111l_opy_(config):
  if bstack1l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬଋ") in config:
    del(config[bstack1l_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ଌ")])
    return False
  if bstack1ll1l1111_opy_() < version.parse(bstack1l_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧ଍")):
    return False
  if bstack1ll1l1111_opy_() >= version.parse(bstack1l_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨ଎")):
    return True
  if bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪଏ") in config and config[bstack1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫଐ")] == False:
    return False
  else:
    return True
def bstack1l111ll_opy_(config, index = 0):
  global bstack11ll1lll_opy_
  bstack1lll11l_opy_ = {}
  caps = bstack11l11l1l_opy_ + bstack111l1l_opy_
  if bstack11ll1lll_opy_:
    caps += bstack1ll1lll1l_opy_
  for key in config:
    if key in caps + [bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ଑")]:
      continue
    bstack1lll11l_opy_[key] = config[key]
  if bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ଒") in config:
    for bstack1ll1l11l1_opy_ in config[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଓ")][index]:
      if bstack1ll1l11l1_opy_ in caps + [bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ଔ"), bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪକ")]:
        continue
      bstack1lll11l_opy_[bstack1ll1l11l1_opy_] = config[bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଖ")][index][bstack1ll1l11l1_opy_]
  bstack1lll11l_opy_[bstack1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ଗ")] = socket.gethostname()
  if bstack1l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ଘ") in bstack1lll11l_opy_:
    del(bstack1lll11l_opy_[bstack1l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧଙ")])
  return bstack1lll11l_opy_
def bstack11lll_opy_(config):
  global bstack11ll1lll_opy_
  bstack1lll1_opy_ = {}
  caps = bstack111l1l_opy_
  if bstack11ll1lll_opy_:
    caps+= bstack1ll1lll1l_opy_
  for key in caps:
    if key in config:
      bstack1lll1_opy_[key] = config[key]
  return bstack1lll1_opy_
def bstack1l1lll1l_opy_(bstack1lll11l_opy_, bstack1lll1_opy_):
  bstack1l1lllll_opy_ = {}
  for key in bstack1lll11l_opy_.keys():
    if key in bstack1l1l111ll_opy_:
      bstack1l1lllll_opy_[bstack1l1l111ll_opy_[key]] = bstack1lll11l_opy_[key]
    else:
      bstack1l1lllll_opy_[key] = bstack1lll11l_opy_[key]
  for key in bstack1lll1_opy_:
    if key in bstack1l1l111ll_opy_:
      bstack1l1lllll_opy_[bstack1l1l111ll_opy_[key]] = bstack1lll1_opy_[key]
    else:
      bstack1l1lllll_opy_[key] = bstack1lll1_opy_[key]
  return bstack1l1lllll_opy_
def bstack11l111ll_opy_(config, index = 0):
  global bstack11ll1lll_opy_
  caps = {}
  bstack1lll1_opy_ = bstack11lll_opy_(config)
  bstack1ll111l1_opy_ = bstack111l1l_opy_
  bstack1ll111l1_opy_ += bstack1l1l1ll1l_opy_
  if bstack11ll1lll_opy_:
    bstack1ll111l1_opy_ += bstack1ll1lll1l_opy_
  if bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଚ") in config:
    if bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ଛ") in config[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଜ")][index]:
      caps[bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଝ")] = config[bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଞ")][index][bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪଟ")]
    if bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧଠ") in config[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଡ")][index]:
      caps[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩଢ")] = str(config[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଣ")][index][bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫତ")])
    bstack11l11_opy_ = {}
    for bstack11lll1_opy_ in bstack1ll111l1_opy_:
      if bstack11lll1_opy_ in config[bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଥ")][index]:
        if bstack11lll1_opy_ == bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧଦ"):
          bstack11l11_opy_[bstack11lll1_opy_] = str(config[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଧ")][index][bstack11lll1_opy_] * 1.0)
        else:
          bstack11l11_opy_[bstack11lll1_opy_] = config[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪନ")][index][bstack11lll1_opy_]
        del(config[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ଩")][index][bstack11lll1_opy_])
    bstack1lll1_opy_ = update(bstack1lll1_opy_, bstack11l11_opy_)
  bstack1lll11l_opy_ = bstack1l111ll_opy_(config, index)
  for bstack11lllll1l_opy_ in bstack111l1l_opy_ + [bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧପ"), bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫଫ")]:
    if bstack11lllll1l_opy_ in bstack1lll11l_opy_:
      bstack1lll1_opy_[bstack11lllll1l_opy_] = bstack1lll11l_opy_[bstack11lllll1l_opy_]
      del(bstack1lll11l_opy_[bstack11lllll1l_opy_])
  if bstack11111l_opy_(config):
    bstack1lll11l_opy_[bstack1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫବ")] = True
    caps.update(bstack1lll1_opy_)
    caps[bstack1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ଭ")] = bstack1lll11l_opy_
  else:
    bstack1lll11l_opy_[bstack1l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ମ")] = False
    caps.update(bstack1l1lll1l_opy_(bstack1lll11l_opy_, bstack1lll1_opy_))
    if bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬଯ") in caps:
      caps[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩର")] = caps[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ଱")]
      del(caps[bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଲ")])
    if bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬଳ") in caps:
      caps[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ଴")] = caps[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧଵ")]
      del(caps[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨଶ")])
  return caps
def bstack1l1llll1l_opy_():
  global bstack1ll11l_opy_
  if bstack1ll1l1111_opy_() <= version.parse(bstack1l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨଷ")):
    if bstack1ll11l_opy_ != bstack1l_opy_ (u"ࠩࠪସ"):
      return bstack1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦହ") + bstack1ll11l_opy_ + bstack1l_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ଺")
    return bstack1l11l11_opy_
  if  bstack1ll11l_opy_ != bstack1l_opy_ (u"ࠬ࠭଻"):
    return bstack1l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯଼ࠣ") + bstack1ll11l_opy_ + bstack1l_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣଽ")
  return bstack1l11l1l_opy_
def bstack1l1l1ll1_opy_(options):
  return hasattr(options, bstack1l_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩା"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1lll1lll_opy_(options, bstack1l1lllll1_opy_):
  for bstack1l11l1111_opy_ in bstack1l1lllll1_opy_:
    if bstack1l11l1111_opy_ in [bstack1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧି"), bstack1l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧୀ")]:
      next
    if bstack1l11l1111_opy_ in options._experimental_options:
      options._experimental_options[bstack1l11l1111_opy_]= update(options._experimental_options[bstack1l11l1111_opy_], bstack1l1lllll1_opy_[bstack1l11l1111_opy_])
    else:
      options.add_experimental_option(bstack1l11l1111_opy_, bstack1l1lllll1_opy_[bstack1l11l1111_opy_])
  if bstack1l_opy_ (u"ࠫࡦࡸࡧࡴࠩୁ") in bstack1l1lllll1_opy_:
    for arg in bstack1l1lllll1_opy_[bstack1l_opy_ (u"ࠬࡧࡲࡨࡵࠪୂ")]:
      options.add_argument(arg)
    del(bstack1l1lllll1_opy_[bstack1l_opy_ (u"࠭ࡡࡳࡩࡶࠫୃ")])
  if bstack1l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫୄ") in bstack1l1lllll1_opy_:
    for ext in bstack1l1lllll1_opy_[bstack1l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ୅")]:
      options.add_extension(ext)
    del(bstack1l1lllll1_opy_[bstack1l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭୆")])
def bstack1lllllll1_opy_(options, bstack1ll111ll_opy_):
  if bstack1l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩେ") in bstack1ll111ll_opy_:
    for bstack1111ll1_opy_ in bstack1ll111ll_opy_[bstack1l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪୈ")]:
      if bstack1111ll1_opy_ in options._preferences:
        options._preferences[bstack1111ll1_opy_] = update(options._preferences[bstack1111ll1_opy_], bstack1ll111ll_opy_[bstack1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ୉")][bstack1111ll1_opy_])
      else:
        options.set_preference(bstack1111ll1_opy_, bstack1ll111ll_opy_[bstack1l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ୊")][bstack1111ll1_opy_])
  if bstack1l_opy_ (u"ࠧࡢࡴࡪࡷࠬୋ") in bstack1ll111ll_opy_:
    for arg in bstack1ll111ll_opy_[bstack1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ୌ")]:
      options.add_argument(arg)
def bstack111l11_opy_(options, bstack11111l1l_opy_):
  if bstack1l_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹ୍ࠪ") in bstack11111l1l_opy_:
    options.use_webview(bool(bstack11111l1l_opy_[bstack1l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫ୎")]))
  bstack1lll1lll_opy_(options, bstack11111l1l_opy_)
def bstack1l1l111l_opy_(options, bstack111ll11_opy_):
  for bstack1111l1_opy_ in bstack111ll11_opy_:
    if bstack1111l1_opy_ in [bstack1l_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨ୏"), bstack1l_opy_ (u"ࠬࡧࡲࡨࡵࠪ୐")]:
      next
    options.set_capability(bstack1111l1_opy_, bstack111ll11_opy_[bstack1111l1_opy_])
  if bstack1l_opy_ (u"࠭ࡡࡳࡩࡶࠫ୑") in bstack111ll11_opy_:
    for arg in bstack111ll11_opy_[bstack1l_opy_ (u"ࠧࡢࡴࡪࡷࠬ୒")]:
      options.add_argument(arg)
  if bstack1l_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬ୓") in bstack111ll11_opy_:
    options.use_technology_preview(bool(bstack111ll11_opy_[bstack1l_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭୔")]))
def bstack11l1ll_opy_(options, bstack11ll1l_opy_):
  for bstack11l111l_opy_ in bstack11ll1l_opy_:
    if bstack11l111l_opy_ in [bstack1l_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ୕"), bstack1l_opy_ (u"ࠫࡦࡸࡧࡴࠩୖ")]:
      next
    options._options[bstack11l111l_opy_] = bstack11ll1l_opy_[bstack11l111l_opy_]
  if bstack1l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩୗ") in bstack11ll1l_opy_:
    for bstack1l1ll1l1l_opy_ in bstack11ll1l_opy_[bstack1l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ୘")]:
      options.add_additional_option(
          bstack1l1ll1l1l_opy_, bstack11ll1l_opy_[bstack1l_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ୙")][bstack1l1ll1l1l_opy_])
  if bstack1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୚") in bstack11ll1l_opy_:
    for arg in bstack11ll1l_opy_[bstack1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ୛")]:
      options.add_argument(arg)
def bstack1l1l1l1_opy_(options, caps):
  if not hasattr(options, bstack1l_opy_ (u"ࠪࡏࡊ࡟ࠧଡ଼")):
    return
  if options.KEY == bstack1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩଢ଼") and options.KEY in caps:
    bstack1lll1lll_opy_(options, caps[bstack1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ୞")])
  elif options.KEY == bstack1l_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫୟ") and options.KEY in caps:
    bstack1lllllll1_opy_(options, caps[bstack1l_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬୠ")])
  elif options.KEY == bstack1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩୡ") and options.KEY in caps:
    bstack1l1l111l_opy_(options, caps[bstack1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪୢ")])
  elif options.KEY == bstack1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫୣ") and options.KEY in caps:
    bstack111l11_opy_(options, caps[bstack1l_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬ୤")])
  elif options.KEY == bstack1l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ୥") and options.KEY in caps:
    bstack11l1ll_opy_(options, caps[bstack1l_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ୦")])
def bstack1lll11ll1_opy_(caps):
  global bstack11ll1lll_opy_
  if bstack11ll1lll_opy_:
    if bstack1111l1l1_opy_() < version.parse(bstack1l_opy_ (u"ࠧ࠳࠰࠶࠲࠵࠭୧")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ୨")
    if bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ୩") in caps:
      browser = caps[bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ୪")]
    elif bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ୫") in caps:
      browser = caps[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭୬")]
    browser = str(browser).lower()
    if browser == bstack1l_opy_ (u"࠭ࡩࡱࡪࡲࡲࡪ࠭୭") or browser == bstack1l_opy_ (u"ࠧࡪࡲࡤࡨࠬ୮"):
      browser = bstack1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ୯")
    if browser == bstack1l_opy_ (u"ࠩࡶࡥࡲࡹࡵ࡯ࡩࠪ୰"):
      browser = bstack1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪୱ")
    if browser not in [bstack1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ୲"), bstack1l_opy_ (u"ࠬ࡫ࡤࡨࡧࠪ୳"), bstack1l_opy_ (u"࠭ࡩࡦࠩ୴"), bstack1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧ୵"), bstack1l_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩ୶")]:
      return None
    try:
      package = bstack1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡼࡿ࠱ࡳࡵࡺࡩࡰࡰࡶࠫ୷").format(browser)
      name = bstack1l_opy_ (u"ࠪࡓࡵࡺࡩࡰࡰࡶࠫ୸")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1l1ll1_opy_(options):
        return None
      for bstack11lllll1l_opy_ in caps.keys():
        options.set_capability(bstack11lllll1l_opy_, caps[bstack11lllll1l_opy_])
      bstack1l1l1l1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1l1l11l_opy_(options, bstack11l111_opy_):
  if not bstack1l1l1ll1_opy_(options):
    return
  for bstack11lllll1l_opy_ in bstack11l111_opy_.keys():
    if bstack11lllll1l_opy_ in bstack1l1l1ll1l_opy_:
      next
    if bstack11lllll1l_opy_ in options._caps and type(options._caps[bstack11lllll1l_opy_]) in [dict, list]:
      options._caps[bstack11lllll1l_opy_] = update(options._caps[bstack11lllll1l_opy_], bstack11l111_opy_[bstack11lllll1l_opy_])
    else:
      options.set_capability(bstack11lllll1l_opy_, bstack11l111_opy_[bstack11lllll1l_opy_])
  bstack1l1l1l1_opy_(options, bstack11l111_opy_)
  if bstack1l_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪ୹") in options._caps:
    if options._caps[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ୺")] and options._caps[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ୻")].lower() != bstack1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨ୼"):
      del options._caps[bstack1l_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧ୽")]
def bstack11lll11_opy_(proxy_config):
  if bstack1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭୾") in proxy_config:
    proxy_config[bstack1l_opy_ (u"ࠪࡷࡸࡲࡐࡳࡱࡻࡽࠬ୿")] = proxy_config[bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ஀")]
    del(proxy_config[bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ஁")])
  if bstack1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩஂ") in proxy_config and proxy_config[bstack1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪஃ")].lower() != bstack1l_opy_ (u"ࠨࡦ࡬ࡶࡪࡩࡴࠨ஄"):
    proxy_config[bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬஅ")] = bstack1l_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࠪஆ")
  if bstack1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡄࡹࡹࡵࡣࡰࡰࡩ࡭࡬࡛ࡲ࡭ࠩஇ") in proxy_config:
    proxy_config[bstack1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨஈ")] = bstack1l_opy_ (u"࠭ࡰࡢࡥࠪஉ")
  return proxy_config
def bstack11l1111l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ஊ") in config:
    return proxy
  config[bstack1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ஋")] = bstack11lll11_opy_(config[bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ஌")])
  if proxy == None:
    proxy = Proxy(config[bstack1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ஍")])
  return proxy
def bstack1l1lll111_opy_(self):
  global CONFIG
  global bstack11ll_opy_
  if bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧஎ") in CONFIG:
    return CONFIG[bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨஏ")]
  elif bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪஐ") in CONFIG:
    return CONFIG[bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ஑")]
  else:
    return bstack11ll_opy_(self)
def bstack1l111111_opy_():
  global CONFIG
  return bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫஒ") in CONFIG or bstack1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ஓ") in CONFIG
def bstack1111lll1_opy_(config):
  if not bstack1l111111_opy_():
    return
  if config.get(bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ஔ")):
    return config.get(bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧக"))
  if config.get(bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ஖")):
    return config.get(bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ஗"))
def bstack1l11l11l1_opy_():
  return bstack1l111111_opy_() and bstack1ll1l1111_opy_() >= version.parse(bstack11l1l1_opy_)
def bstack1l1111l11_opy_(config):
  if bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ஘") in config:
    return config[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬங")]
  if bstack1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨச") in config:
    return config[bstack1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ஛")]
  return {}
def bstack11l11ll_opy_(config):
  if bstack1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩஜ") in config:
    return config[bstack1l_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ஝")]
  return {}
def bstack11lll1l1_opy_(caps):
  global bstack1ll11111l_opy_
  if bstack1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧஞ") in caps:
    caps[bstack1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨட")][bstack1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ஠")] = True
    if bstack1ll11111l_opy_:
      caps[bstack1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ஡")][bstack1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ஢")] = bstack1ll11111l_opy_
  else:
    caps[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩண")] = True
    if bstack1ll11111l_opy_:
      caps[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭த")] = bstack1ll11111l_opy_
def bstack1llll11ll_opy_():
  global CONFIG
  if bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ஥") in CONFIG and CONFIG[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ஦")]:
    bstack111111ll_opy_ = bstack1l1111l11_opy_(CONFIG)
    bstack1lll1llll_opy_(CONFIG[bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ஧")], bstack111111ll_opy_)
def bstack1lll1llll_opy_(key, bstack111111ll_opy_):
  global bstack111l1lll_opy_
  logger.info(bstack1ll111_opy_)
  try:
    bstack111l1lll_opy_ = Local()
    bstack1llll1l1_opy_ = {bstack1l_opy_ (u"ࠩ࡮ࡩࡾ࠭ந"): key}
    bstack1llll1l1_opy_.update(bstack111111ll_opy_)
    logger.debug(bstack1l1l1ll_opy_.format(str(bstack1llll1l1_opy_)))
    bstack111l1lll_opy_.start(**bstack1llll1l1_opy_)
    if bstack111l1lll_opy_.isRunning():
      logger.info(bstack11l1ll1l_opy_)
  except Exception as e:
    bstack1l1lll1ll_opy_(bstack1l1ll1_opy_.format(str(e)))
def bstack1lll111l1_opy_():
  global bstack111l1lll_opy_
  if bstack111l1lll_opy_.isRunning():
    logger.info(bstack1l1111l1l_opy_)
    bstack111l1lll_opy_.stop()
  bstack111l1lll_opy_ = None
def bstack1l1l11ll1_opy_():
  global bstack1lll1l_opy_
  global bstack1ll111ll1_opy_
  if bstack1lll1l_opy_:
    logger.warning(bstack11111l1_opy_.format(str(bstack1lll1l_opy_)))
  logger.info(bstack1lllll1l_opy_)
  global bstack111l1lll_opy_
  if bstack111l1lll_opy_:
    bstack1lll111l1_opy_()
  try:
    for driver in bstack1ll111ll1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1llllll_opy_)
  bstack1ll11ll1l_opy_()
def bstack1l11l1_opy_(self, *args):
  logger.error(bstack1lll1l1l1_opy_)
  bstack1l1l11ll1_opy_()
  sys.exit(1)
def bstack1l1lll1ll_opy_(err):
  logger.critical(bstack1lllll111_opy_.format(str(err)))
  bstack1ll11ll1l_opy_(bstack1lllll111_opy_.format(str(err)))
  atexit.unregister(bstack1l1l11ll1_opy_)
  sys.exit(1)
def bstack111ll1ll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1ll11ll1l_opy_(message)
  atexit.unregister(bstack1l1l11ll1_opy_)
  sys.exit(1)
def bstack1l111l1l_opy_():
  global CONFIG
  global bstack1ll11l111_opy_
  global bstack1llll1ll1_opy_
  global bstack1ll111lll_opy_
  CONFIG = bstack1ll1l1ll1_opy_()
  bstack1111l11l_opy_()
  bstack11l1l1ll_opy_()
  CONFIG = bstack1l111_opy_(CONFIG)
  update(CONFIG, bstack1llll1ll1_opy_)
  update(CONFIG, bstack1ll11l111_opy_)
  CONFIG = bstack1l11l1ll_opy_(CONFIG)
  if bstack1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧன") in CONFIG and str(CONFIG[bstack1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨப")]).lower() == bstack1l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ஫"):
    bstack1ll111lll_opy_ = False
  if (bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ஬") in CONFIG and bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ஭") in bstack1ll11l111_opy_) or (bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫம") in CONFIG and bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬய") not in bstack1llll1ll1_opy_):
    if os.getenv(bstack1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧர")):
      CONFIG[bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ற")] = os.getenv(bstack1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩல"))
    else:
      bstack1lll1ll1_opy_()
  elif (bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩள") not in CONFIG and bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩழ") in CONFIG) or (bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫவ") in bstack1llll1ll1_opy_ and bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬஶ") not in bstack1ll11l111_opy_):
    del(CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬஷ")])
  if bstack1l111ll1_opy_(CONFIG):
    bstack1l1lll1ll_opy_(bstack1l1l1llll_opy_)
  bstack1ll1l11ll_opy_()
  bstack111l111_opy_()
  if bstack11ll1lll_opy_:
    CONFIG[bstack1l_opy_ (u"ࠫࡦࡶࡰࠨஸ")] = bstack11l111l1_opy_(CONFIG)
    logger.info(bstack1lll11_opy_.format(CONFIG[bstack1l_opy_ (u"ࠬࡧࡰࡱࠩஹ")]))
def bstack111l111_opy_():
  global CONFIG
  global bstack11ll1lll_opy_
  if bstack1l_opy_ (u"࠭ࡡࡱࡲࠪ஺") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack111ll1ll_opy_(e, bstack1llll_opy_)
    bstack11ll1lll_opy_ = True
def bstack11l111l1_opy_(config):
  bstack1ll1lllll_opy_ = bstack1l_opy_ (u"ࠧࠨ஻")
  app = config[bstack1l_opy_ (u"ࠨࡣࡳࡴࠬ஼")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1ll1l1l1l_opy_:
      if os.path.exists(app):
        bstack1ll1lllll_opy_ = bstack1ll1ll1l1_opy_(config, app)
      elif bstack1l1ll111_opy_(app):
        bstack1ll1lllll_opy_ = app
      else:
        bstack1l1lll1ll_opy_(bstack1l1lll_opy_.format(app))
    else:
      if bstack1l1ll111_opy_(app):
        bstack1ll1lllll_opy_ = app
      elif os.path.exists(app):
        bstack1ll1lllll_opy_ = bstack1ll1ll1l1_opy_(app)
      else:
        bstack1l1lll1ll_opy_(bstack1l11l1l11_opy_)
  else:
    if len(app) > 2:
      bstack1l1lll1ll_opy_(bstack111l1l1l_opy_)
    elif len(app) == 2:
      if bstack1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ஽") in app and bstack1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ா") in app:
        if os.path.exists(app[bstack1l_opy_ (u"ࠫࡵࡧࡴࡩࠩி")]):
          bstack1ll1lllll_opy_ = bstack1ll1ll1l1_opy_(config, app[bstack1l_opy_ (u"ࠬࡶࡡࡵࡪࠪீ")], app[bstack1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩு")])
        else:
          bstack1l1lll1ll_opy_(bstack1l1lll_opy_.format(app))
      else:
        bstack1l1lll1ll_opy_(bstack111l1l1l_opy_)
    else:
      for key in app:
        if key in bstack1l11111l_opy_:
          if key == bstack1l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬூ"):
            if os.path.exists(app[key]):
              bstack1ll1lllll_opy_ = bstack1ll1ll1l1_opy_(config, app[key])
            else:
              bstack1l1lll1ll_opy_(bstack1l1lll_opy_.format(app))
          else:
            bstack1ll1lllll_opy_ = app[key]
        else:
          bstack1l1lll1ll_opy_(bstack1lll11l1_opy_)
  return bstack1ll1lllll_opy_
def bstack1l1ll111_opy_(bstack1ll1lllll_opy_):
  import re
  bstack1l11l1l1l_opy_ = re.compile(bstack1l_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣ௃"))
  bstack1lllllll_opy_ = re.compile(bstack1l_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪ࠰࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮ࠩࠨ௄"))
  if bstack1l_opy_ (u"ࠪࡦࡸࡀ࠯࠰ࠩ௅") in bstack1ll1lllll_opy_ or re.fullmatch(bstack1l11l1l1l_opy_, bstack1ll1lllll_opy_) or re.fullmatch(bstack1lllllll_opy_, bstack1ll1lllll_opy_):
    return True
  else:
    return False
def bstack1ll1ll1l1_opy_(config, path, bstack111l1ll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l_opy_ (u"ࠫࡷࡨࠧெ")).read()).hexdigest()
  bstack1lll1l1ll_opy_ = bstack1l1l1l1l1_opy_(md5_hash)
  bstack1ll1lllll_opy_ = None
  if bstack1lll1l1ll_opy_:
    logger.info(bstack1l111l11_opy_.format(bstack1lll1l1ll_opy_, md5_hash))
    return bstack1lll1l1ll_opy_
  bstack11l1ll1_opy_ = MultipartEncoder(
    fields={
        bstack1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࠪே"): (os.path.basename(path), open(os.path.abspath(path), bstack1l_opy_ (u"࠭ࡲࡣࠩை")), bstack1l_opy_ (u"ࠧࡵࡧࡻࡸ࠴ࡶ࡬ࡢ࡫ࡱࠫ௉")),
        bstack1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫொ"): bstack111l1ll_opy_
    }
  )
  response = requests.post(bstack111l1ll1_opy_, data=bstack11l1ll1_opy_,
                         headers={bstack1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨோ"): bstack11l1ll1_opy_.content_type}, auth=(config[bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬௌ")], config[bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿ்ࠧ")]))
  try:
    res = json.loads(response.text)
    bstack1ll1lllll_opy_ = res[bstack1l_opy_ (u"ࠬࡧࡰࡱࡡࡸࡶࡱ࠭௎")]
    logger.info(bstack1l11ll1ll_opy_.format(bstack1ll1lllll_opy_))
    bstack1111ll1l_opy_(md5_hash, bstack1ll1lllll_opy_)
  except ValueError as err:
    bstack1l1lll1ll_opy_(bstack1ll1llll1_opy_.format(str(err)))
  return bstack1ll1lllll_opy_
def bstack1ll1l11ll_opy_():
  global CONFIG
  global bstack1l111ll1l_opy_
  bstack1111l1l_opy_ = 0
  bstack1l11l111l_opy_ = 1
  if bstack1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭௏") in CONFIG:
    bstack1l11l111l_opy_ = CONFIG[bstack1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧௐ")]
  if bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௑") in CONFIG:
    bstack1111l1l_opy_ = len(CONFIG[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௒")])
  bstack1l111ll1l_opy_ = int(bstack1l11l111l_opy_) * int(bstack1111l1l_opy_)
def bstack1l1l1l1l1_opy_(md5_hash):
  bstack1l11lll1_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠪࢂࠬ௓")), bstack1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ௔"), bstack1l_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭௕"))
  if os.path.exists(bstack1l11lll1_opy_):
    bstack1l1ll11ll_opy_ = json.load(open(bstack1l11lll1_opy_,bstack1l_opy_ (u"࠭ࡲࡣࠩ௖")))
    if md5_hash in bstack1l1ll11ll_opy_:
      bstack1llllll1l_opy_ = bstack1l1ll11ll_opy_[md5_hash]
      bstack1ll1ll1_opy_ = datetime.datetime.now()
      bstack11ll1_opy_ = datetime.datetime.strptime(bstack1llllll1l_opy_[bstack1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪௗ")], bstack1l_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ௘"))
      if (bstack1ll1ll1_opy_ - bstack11ll1_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1llllll1l_opy_[bstack1l_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ௙")]):
        return None
      return bstack1llllll1l_opy_[bstack1l_opy_ (u"ࠪ࡭ࡩ࠭௚")]
  else:
    return None
def bstack1111ll1l_opy_(md5_hash, bstack1ll1lllll_opy_):
  bstack11ll1ll1_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠫࢃ࠭௛")), bstack1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ௜"))
  if not os.path.exists(bstack11ll1ll1_opy_):
    os.makedirs(bstack11ll1ll1_opy_)
  bstack1l11lll1_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"࠭ࡾࠨ௝")), bstack1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ௞"), bstack1l_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩ௟"))
  bstack1111l11_opy_ = {
    bstack1l_opy_ (u"ࠩ࡬ࡨࠬ௠"): bstack1ll1lllll_opy_,
    bstack1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭௡"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ௢")),
    bstack1l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ௣"): str(__version__)
  }
  if os.path.exists(bstack1l11lll1_opy_):
    bstack1l1ll11ll_opy_ = json.load(open(bstack1l11lll1_opy_,bstack1l_opy_ (u"࠭ࡲࡣࠩ௤")))
  else:
    bstack1l1ll11ll_opy_ = {}
  bstack1l1ll11ll_opy_[md5_hash] = bstack1111l11_opy_
  with open(bstack1l11lll1_opy_, bstack1l_opy_ (u"ࠢࡸ࠭ࠥ௥")) as outfile:
    json.dump(bstack1l1ll11ll_opy_, outfile)
def bstack11l1ll11_opy_(self):
  return
def bstack1lll11lll_opy_(self):
  return
def bstack1l111l1l1_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1l1l1l111_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1llll111l_opy_
  global bstack1lll1l11_opy_
  global bstack11lll11l_opy_
  global bstack1lllll1l1_opy_
  global bstack11ll1l11_opy_
  global bstack111111l1_opy_
  global bstack1ll111ll1_opy_
  CONFIG[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ௦")] = str(bstack11ll1l11_opy_) + str(__version__)
  command_executor = bstack1l1llll1l_opy_()
  logger.debug(bstack111l_opy_.format(command_executor))
  proxy = bstack11l1111l_opy_(CONFIG, proxy)
  bstack1ll1ll1l_opy_ = 0 if bstack1lll1l11_opy_ < 0 else bstack1lll1l11_opy_
  if bstack1lllll1l1_opy_ is True:
    bstack1ll1ll1l_opy_ = int(threading.current_thread().getName())
  bstack11l111_opy_ = bstack11l111ll_opy_(CONFIG, bstack1ll1ll1l_opy_)
  logger.debug(bstack1l1l11l1_opy_.format(str(bstack11l111_opy_)))
  if bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭௧") in CONFIG and CONFIG[bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ௨")]:
    bstack11lll1l1_opy_(bstack11l111_opy_)
  if desired_capabilities:
    bstack11l1l1l1_opy_ = bstack1l111_opy_(desired_capabilities)
    bstack11l1l1l1_opy_[bstack1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ௩")] = bstack11111l_opy_(CONFIG)
    bstack1l11ll11l_opy_ = bstack11l111ll_opy_(bstack11l1l1l1_opy_)
    if bstack1l11ll11l_opy_:
      bstack11l111_opy_ = update(bstack1l11ll11l_opy_, bstack11l111_opy_)
    desired_capabilities = None
  if options:
    bstack1l1l1l11l_opy_(options, bstack11l111_opy_)
  if not options:
    options = bstack1lll11ll1_opy_(bstack11l111_opy_)
  if options and bstack1ll1l1111_opy_() >= version.parse(bstack1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ௪")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack1ll1l1111_opy_() < version.parse(bstack1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ௫")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11l111_opy_)
  logger.info(bstack1lll1ll11_opy_)
  if bstack1ll1l1111_opy_() >= version.parse(bstack1l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭௬")):
    bstack111111l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll1l1111_opy_() >= version.parse(bstack1l_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨ௭")):
    bstack111111l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack111111l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  try:
    bstack1lll1lll1_opy_ = bstack1l_opy_ (u"ࠩࠪ௮")
    if bstack1ll1l1111_opy_() >= version.parse(bstack1l_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫ௯")):
      bstack1lll1lll1_opy_ = self.caps.get(bstack1l_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ௰"))
    else:
      bstack1lll1lll1_opy_ = self.capabilities.get(bstack1l_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ௱"))
    if bstack1lll1lll1_opy_:
      if bstack1ll1l1111_opy_() <= version.parse(bstack1l_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭௲")):
        self.command_executor._url = bstack1l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ௳") + bstack1ll11l_opy_ + bstack1l_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ௴")
      else:
        self.command_executor._url = bstack1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ௵") + bstack1lll1lll1_opy_ + bstack1l_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ௶")
      logger.debug(bstack11l11l_opy_.format(bstack1lll1lll1_opy_))
    else:
      logger.debug(bstack1ll111l11_opy_.format(bstack1l_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧ௷")))
  except Exception as e:
    logger.debug(bstack1ll111l11_opy_.format(e))
  bstack1llll111l_opy_ = self.session_id
  bstack1ll111ll1_opy_.append(self)
  if bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௸") in CONFIG and bstack1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ௹") in CONFIG[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ௺")][bstack1ll1ll1l_opy_]:
    bstack11lll11l_opy_ = CONFIG[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௻")][bstack1ll1ll1l_opy_][bstack1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ௼")]
  logger.debug(bstack111l11ll_opy_.format(bstack1llll111l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1lll11l11_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11ll1111_opy_
      if(bstack1l_opy_ (u"ࠥ࡭ࡳࡪࡥࡹ࠰࡭ࡷࠧ௽") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠫࢃ࠭௾")), bstack1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ௿"), bstack1l_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨఀ")), bstack1l_opy_ (u"ࠧࡸࠩఁ")) as fp:
          fp.write(bstack1l_opy_ (u"ࠣࠤం"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦః")))):
          with open(args[1], bstack1l_opy_ (u"ࠪࡶࠬఄ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l_opy_ (u"ࠫࡦࡹࡹ࡯ࡥࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡥ࡮ࡦࡹࡓࡥ࡬࡫ࠨࡤࡱࡱࡸࡪࡾࡴ࠭ࠢࡳࡥ࡬࡫ࠠ࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠪఅ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l11_opy_)
            lines.insert(1, bstack1l1l11l11_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢఆ")), bstack1l_opy_ (u"࠭ࡷࠨఇ")) as bstack1llll11l1_opy_:
              bstack1llll11l1_opy_.writelines(lines)
        CONFIG[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩఈ")] = str(bstack11ll1l11_opy_) + str(__version__)
        bstack1ll1ll1l_opy_ = 0 if bstack1lll1l11_opy_ < 0 else bstack1lll1l11_opy_
        if bstack1lllll1l1_opy_ is True:
          bstack1ll1ll1l_opy_ = int(threading.current_thread().getName())
        CONFIG[bstack1l_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣఉ")] = False
        CONFIG[bstack1l_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣఊ")] = True
        bstack11l111_opy_ = bstack11l111ll_opy_(CONFIG, bstack1ll1ll1l_opy_)
        logger.debug(bstack1l1l11l1_opy_.format(str(bstack11l111_opy_)))
        if CONFIG[bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧఋ")]:
          bstack11lll1l1_opy_(bstack11l111_opy_)
        if bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧఌ") in CONFIG and bstack1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ఍") in CONFIG[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩఎ")][bstack1ll1ll1l_opy_]:
          bstack11lll11l_opy_ = CONFIG[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪఏ")][bstack1ll1ll1l_opy_][bstack1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ఐ")]
        args.append(os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠩࢁࠫ఑")), bstack1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪఒ"), bstack1l_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ఓ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11l111_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢఔ"))
      bstack11ll1111_opy_ = True
      return bstack1l1111l1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l1l1111_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1llll111l_opy_
    global bstack1lll1l11_opy_
    global bstack11lll11l_opy_
    global bstack1lllll1l1_opy_
    global bstack11ll1l11_opy_
    global bstack111111l1_opy_
    CONFIG[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨక")] = str(bstack11ll1l11_opy_) + str(__version__)
    bstack1ll1ll1l_opy_ = 0 if bstack1lll1l11_opy_ < 0 else bstack1lll1l11_opy_
    if bstack1lllll1l1_opy_ is True:
      bstack1ll1ll1l_opy_ = int(threading.current_thread().getName())
    CONFIG[bstack1l_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨఖ")] = True
    bstack11l111_opy_ = bstack11l111ll_opy_(CONFIG, bstack1ll1ll1l_opy_)
    logger.debug(bstack1l1l11l1_opy_.format(str(bstack11l111_opy_)))
    if CONFIG[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬగ")]:
      bstack11lll1l1_opy_(bstack11l111_opy_)
    if bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬఘ") in CONFIG and bstack1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨఙ") in CONFIG[bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧచ")][bstack1ll1ll1l_opy_]:
      bstack11lll11l_opy_ = CONFIG[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨఛ")][bstack1ll1ll1l_opy_][bstack1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫజ")]
    import urllib
    import json
    bstack1111l_opy_ = bstack1l_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩఝ") + urllib.parse.quote(json.dumps(bstack11l111_opy_))
    browser = self.connect(bstack1111l_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1ll111l_opy_():
    global bstack11ll1111_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l1l1111_opy_
        bstack11ll1111_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1lll11l11_opy_
      bstack11ll1111_opy_ = True
    except Exception as e:
      pass
def bstack1l1ll1ll1_opy_(context, bstack1lll1111l_opy_):
  try:
    context.page.evaluate(bstack1l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤఞ"), bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ట")+ json.dumps(bstack1lll1111l_opy_) + bstack1l_opy_ (u"ࠥࢁࢂࠨఠ"))
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤడ"), e)
def bstack1l11ll1l1_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨఢ"), bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫణ") + json.dumps(message) + bstack1l_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪత") + json.dumps(level) + bstack1l_opy_ (u"ࠨࡿࢀࠫథ"))
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧద"), e)
def bstack11llll11_opy_(context, status, message = bstack1l_opy_ (u"ࠥࠦధ")):
  try:
    if(status == bstack1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦన")):
      context.page.evaluate(bstack1l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ఩"), bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡸࡥࡢࡵࡲࡲࠧࡀࠧప") + json.dumps(bstack1l_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡࠤఫ") + str(message)) + bstack1l_opy_ (u"ࠨ࠮ࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠬబ") + json.dumps(status) + bstack1l_opy_ (u"ࠤࢀࢁࠧభ"))
    else:
      context.page.evaluate(bstack1l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦమ"), bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠬయ") + json.dumps(status) + bstack1l_opy_ (u"ࠧࢃࡽࠣర"))
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠥఱ"), e)
def bstack111l11l_opy_(self, url):
  global bstack1ll1111l_opy_
  try:
    bstack1ll1llll_opy_(url)
  except Exception as err:
    logger.debug(bstack1lllll1ll_opy_.format(str(err)))
  try:
    bstack1ll1111l_opy_(self, url)
  except Exception as e:
    try:
      bstack11ll1ll_opy_ = str(e)
      if any(err_msg in bstack11ll1ll_opy_ for err_msg in bstack1l1llll11_opy_):
        bstack1ll1llll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1lllll1ll_opy_.format(str(err)))
    raise e
def bstack11llll1_opy_(self, test):
  global CONFIG
  global bstack1llll111l_opy_
  global bstack1l1ll11l1_opy_
  global bstack11lll11l_opy_
  global bstack111llll_opy_
  try:
    if not bstack1llll111l_opy_:
      with open(os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠧࡿࠩల")), bstack1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨళ"), bstack1l_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫఴ"))) as f:
        bstack11l11l11_opy_ = json.loads(bstack1l_opy_ (u"ࠥࡿࠧవ") + f.read().strip() + bstack1l_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭శ") + bstack1l_opy_ (u"ࠧࢃࠢష"))
        bstack1llll111l_opy_ = bstack11l11l11_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1llll111l_opy_:
    try:
      data = {}
      bstack11ll11l1_opy_ = None
      if test:
        bstack11ll11l1_opy_ = str(test.data)
      if not bstack1ll11_opy_ and bstack11ll11l1_opy_:
        data[bstack1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫస")] = bstack11ll11l1_opy_
      if bstack1l1ll11l1_opy_:
        if bstack1l1ll11l1_opy_.status == bstack1l_opy_ (u"ࠧࡑࡃࡖࡗࠬహ"):
          data[bstack1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ఺")] = bstack1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ఻")
        elif bstack1l1ll11l1_opy_.status == bstack1l_opy_ (u"ࠪࡊࡆࡏࡌࠨ఼"):
          data[bstack1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫఽ")] = bstack1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬా")
          if bstack1l1ll11l1_opy_.message:
            data[bstack1l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ి")] = str(bstack1l1ll11l1_opy_.message)
      user = CONFIG[bstack1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩీ")]
      key = CONFIG[bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫు")]
      url = bstack1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧూ").format(user, key, bstack1llll111l_opy_)
      headers = {
        bstack1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩృ"): bstack1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧౄ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l1111ll_opy_.format(str(e)))
  bstack111llll_opy_(self, test)
def bstack11l1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1111111l_opy_
  bstack1111111l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l1ll11l1_opy_
  bstack1l1ll11l1_opy_ = self._test
def bstack1111ll_opy_(outs_dir, options, tests_root_name, stats, copied_artifacts, outputfile=None):
  from pabot import pabot
  outputfile = outputfile or options.get(bstack1l_opy_ (u"ࠧࡵࡵࡵࡲࡸࡸࠧ౅"), bstack1l_opy_ (u"ࠨ࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠥె"))
  output_path = os.path.abspath(
    os.path.join(options.get(bstack1l_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࡤࡪࡴࠥే"), bstack1l_opy_ (u"ࠣ࠰ࠥై")), outputfile)
  )
  files = sorted(pabot.glob(os.path.join(pabot._glob_escape(outs_dir), bstack1l_opy_ (u"ࠤ࠭࠲ࡽࡳ࡬ࠣ౉"))))
  if not files:
    pabot._write(bstack1l_opy_ (u"࡛ࠪࡆࡘࡎ࠻ࠢࡑࡳࠥࡵࡵࡵࡲࡸࡸࠥ࡬ࡩ࡭ࡧࡶࠤ࡮ࡴࠠࠣࠧࡶࠦࠬొ") % outs_dir, pabot.Color.YELLOW)
    return bstack1l_opy_ (u"ࠦࠧో")
  def invalid_xml_callback():
    global _ABNORMAL_EXIT_HAPPENED
    _ABNORMAL_EXIT_HAPPENED = True
  resu = pabot.merge(
    files, options, tests_root_name, copied_artifacts, invalid_xml_callback
  )
  pabot._update_stats(resu, stats)
  resu.save(output_path)
  return output_path
def bstack1ll1lll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstack1l_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤౌ") in options:
    del options[bstack1l_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪ్ࠥ")]
  if ROBOT_VERSION < bstack1l_opy_ (u"ࠢ࠵࠰࠳ࠦ౎"):
    stats = {
      bstack1l_opy_ (u"ࠣࡥࡵ࡭ࡹ࡯ࡣࡢ࡮ࠥ౏"): {bstack1l_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࠣ౐"): 0, bstack1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ౑"): 0, bstack1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ౒"): 0},
      bstack1l_opy_ (u"ࠧࡧ࡬࡭ࠤ౓"): {bstack1l_opy_ (u"ࠨࡴࡰࡶࡤࡰࠧ౔"): 0, bstack1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪౕࠢ"): 0, bstack1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤౖࠣ"): 0},
    }
  else:
    stats = {
      bstack1l_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࠣ౗"): 0,
      bstack1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥౘ"): 0,
      bstack1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦౙ"): 0,
      bstack1l_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨౚ"): 0,
    }
  if pabot_args[bstack1l_opy_ (u"ࠨࡂࡔࡖࡄࡇࡐࡥࡐࡂࡔࡄࡐࡑࡋࡌࡠࡔࡘࡒࠧ౛")]:
    outputs = []
    for index, _ in enumerate(pabot_args[bstack1l_opy_ (u"ࠢࡃࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡡࡕ࡙ࡓࠨ౜")]):
      copied_artifacts = pabot._copy_output_artifacts(
        options, pabot_args[bstack1l_opy_ (u"ࠣࡣࡵࡸ࡮࡬ࡡࡤࡶࡶࠦౝ")], pabot_args[bstack1l_opy_ (u"ࠤࡤࡶࡹ࡯ࡦࡢࡥࡷࡷ࡮ࡴࡳࡶࡤࡩࡳࡱࡪࡥࡳࡵࠥ౞")]
      )
      outputs += [
        bstack1111ll_opy_(
          os.path.join(outs_dir, str(index)+ bstack1l_opy_ (u"ࠥ࠳ࠧ౟")),
          options,
          tests_root_name,
          stats,
          copied_artifacts,
          outputfile=os.path.join(bstack1l_opy_ (u"ࠦࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠦౠ"), bstack1l_opy_ (u"ࠧࡵࡵࡵࡲࡸࡸࠪࡹ࠮ࡹ࡯࡯ࠦౡ") % index),
        )
      ]
    if bstack1l_opy_ (u"ࠨ࡯ࡶࡶࡳࡹࡹࠨౢ") not in options:
      options[bstack1l_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠢౣ")] = bstack1l_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠧ౤")
    pabot._write_stats(stats)
    return rebot(*outputs, **pabot._options_for_rebot(options, start_time_string, pabot._now()))
  else:
    return pabot._report_results(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1lll1l1l_opy_(self, ff_profile_dir):
  global bstack111111l_opy_
  if not ff_profile_dir:
    return None
  return bstack111111l_opy_(self, ff_profile_dir)
def bstack1llll11_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll11111l_opy_
  bstack1l1l1l_opy_ = []
  if bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౥") in CONFIG:
    bstack1l1l1l_opy_ = CONFIG[bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౦")]
  bstack11l11ll1_opy_ = len(suite_group) * len(pabot_args[bstack1l_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹ࡬ࡩ࡭ࡧࡶࠦ౧")] or [(bstack1l_opy_ (u"ࠧࠨ౨"), None)]) * len(bstack1l1l1l_opy_)
  pabot_args[bstack1l_opy_ (u"ࠨࡂࡔࡖࡄࡇࡐࡥࡐࡂࡔࡄࡐࡑࡋࡌࡠࡔࡘࡒࠧ౩")] = []
  for q in range(bstack11l11ll1_opy_):
    pabot_args[bstack1l_opy_ (u"ࠢࡃࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡡࡕ࡙ࡓࠨ౪")].append(str(q))
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤ౫")],
      pabot_args[bstack1l_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥ౬")],
      argfile,
      pabot_args.get(bstack1l_opy_ (u"ࠥ࡬࡮ࡼࡥࠣ౭")),
      pabot_args[bstack1l_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢ౮")],
      platform[0],
      bstack1ll11111l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧ౯")] or [(bstack1l_opy_ (u"ࠨࠢ౰"), None)]
    for platform in enumerate(bstack1l1l1l_opy_)
  ]
def bstack1l1l1l1l_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack1111l111_opy_=bstack1l_opy_ (u"ࠧࠨ౱")):
  global bstack11ll111l_opy_
  self.platform_index = platform_index
  self.bstack111ll1_opy_ = bstack1111l111_opy_
  bstack11ll111l_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack111ll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l11l111_opy_
  global bstack1l1l1lll_opy_
  if not bstack1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ౲") in item.options:
    item.options[bstack1l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ౳")] = []
  for v in item.options[bstack1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ౴")]:
    if bstack1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪ౵") in v:
      item.options[bstack1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ౶")].remove(v)
    if bstack1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭౷") in v:
      item.options[bstack1l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ౸")].remove(v)
  item.options[bstack1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ౹")].insert(0, bstack1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫ౺").format(item.platform_index))
  item.options[bstack1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ౻")].insert(0, bstack1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫ౼").format(item.bstack111ll1_opy_))
  if bstack1l1l1lll_opy_:
    item.options[bstack1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ౽")].insert(0, bstack1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩ౾").format(bstack1l1l1lll_opy_))
  return bstack1l11l111_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1l11lllll_opy_(command):
  global bstack1l1l1lll_opy_
  if bstack1l1l1lll_opy_:
    command[0] = command[0].replace(bstack1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭౿"), bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠭ಀ") + bstack1l1l1lll_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨಁ"), bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧಂ"), 1)
def bstack111lll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1ll11l1l_opy_
  bstack1l11lllll_opy_(command)
  return bstack1ll11l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1lll1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1ll11l1l_opy_
  bstack1l11lllll_opy_(command)
  return bstack1ll11l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l111l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1ll11l1l_opy_
  bstack1l11lllll_opy_(command)
  return bstack1ll11l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1l1lll11_opy_(self, runner, quiet=False, capture=True):
  global bstack1lll111_opy_
  bstack11111_opy_ = bstack1lll111_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1l_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫಃ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳࠩ಄")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11111_opy_
def bstack1l1l11l1l_opy_(self, name, context, *args):
  global bstack1l1111_opy_
  if name in [bstack1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧಅ"), bstack1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩಆ")]:
    bstack1l1111_opy_(self, name, context, *args)
  if name == bstack1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩಇ"):
    try:
      if(not bstack1ll11_opy_):
        bstack1lll1111l_opy_ = str(self.feature.name)
        bstack1l1ll1ll1_opy_(context, bstack1lll1111l_opy_)
        context.browser.execute_script(bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧಈ") + json.dumps(bstack1lll1111l_opy_) + bstack1l_opy_ (u"ࠪࢁࢂ࠭ಉ"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫಊ").format(str(e)))
  if name == bstack1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧಋ"):
    try:
      if not hasattr(self, bstack1l_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨಌ")):
        self.driver_before_scenario = True
      if(not bstack1ll11_opy_):
        bstack1llll1111_opy_ = args[0].name
        bstack11l1l111_opy_ = bstack1lll1111l_opy_ = str(self.feature.name)
        bstack1lll1111l_opy_ = bstack11l1l111_opy_ + bstack1l_opy_ (u"ࠧࠡ࠯ࠣࠫ಍") + bstack1llll1111_opy_
        if self.driver_before_scenario:
          bstack1l1ll1ll1_opy_(context, bstack1lll1111l_opy_)
          context.browser.execute_script(bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ಎ") + json.dumps(bstack1lll1111l_opy_) + bstack1l_opy_ (u"ࠩࢀࢁࠬಏ"))
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫಐ").format(str(e)))
  if name == bstack1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ಑"):
    try:
      bstack1lll1ll_opy_ = args[0].status.name
      if str(bstack1lll1ll_opy_).lower() == bstack1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬಒ"):
        bstack1ll11l1_opy_ = bstack1l_opy_ (u"࠭ࠧಓ")
        bstack111ll111_opy_ = bstack1l_opy_ (u"ࠧࠨಔ")
        bstack1ll1111ll_opy_ = bstack1l_opy_ (u"ࠨࠩಕ")
        try:
          import traceback
          bstack1ll11l1_opy_ = self.exception.__class__.__name__
          bstack1llll1l11_opy_ = traceback.format_tb(self.exc_traceback)
          bstack111ll111_opy_ = bstack1l_opy_ (u"ࠩࠣࠫಖ").join(bstack1llll1l11_opy_)
          bstack1ll1111ll_opy_ = bstack1llll1l11_opy_[-1]
        except Exception as e:
          logger.debug(bstack1ll11l11l_opy_.format(str(e)))
        bstack1ll11l1_opy_ += bstack1ll1111ll_opy_
        bstack1l11ll1l1_opy_(context, json.dumps(str(args[0].name) + bstack1l_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤಗ") + str(bstack111ll111_opy_)), bstack1l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥಘ"))
        if self.driver_before_scenario:
          bstack11llll11_opy_(context, bstack1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧಙ"), bstack1ll11l1_opy_)
        context.browser.execute_script(bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫಚ") + json.dumps(str(args[0].name) + bstack1l_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨಛ") + str(bstack111ll111_opy_)) + bstack1l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨಜ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩಝ") + json.dumps(bstack1l_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢಞ") + str(bstack1ll11l1_opy_)) + bstack1l_opy_ (u"ࠫࢂࢃࠧಟ"))
      else:
        bstack1l11ll1l1_opy_(context, bstack1l_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨಠ"), bstack1l_opy_ (u"ࠨࡩ࡯ࡨࡲࠦಡ"))
        if self.driver_before_scenario:
          bstack11llll11_opy_(context, bstack1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢಢ"))
        context.browser.execute_script(bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ಣ") + json.dumps(str(args[0].name) + bstack1l_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨತ")) + bstack1l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩಥ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧࡶࡡࡴࡵࡨࡨࠧࢃࡽࠨದ"))
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧಧ").format(str(e)))
  if name == bstack1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ನ"):
    try:
      if context.failed is True:
        bstack1l11lll_opy_ = []
        bstack1ll1l1l_opy_ = []
        bstack1111_opy_ = []
        bstack1ll1l_opy_ = bstack1l_opy_ (u"ࠧࠨ಩")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1l11lll_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1llll1l11_opy_ = traceback.format_tb(exc_tb)
            bstack1l1ll1ll_opy_ = bstack1l_opy_ (u"ࠨࠢࠪಪ").join(bstack1llll1l11_opy_)
            bstack1ll1l1l_opy_.append(bstack1l1ll1ll_opy_)
            bstack1111_opy_.append(bstack1llll1l11_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll11l11l_opy_.format(str(e)))
        bstack1ll11l1_opy_ = bstack1l_opy_ (u"ࠩࠪಫ")
        for i in range(len(bstack1l11lll_opy_)):
          bstack1ll11l1_opy_ += bstack1l11lll_opy_[i] + bstack1111_opy_[i] + bstack1l_opy_ (u"ࠪࡠࡳ࠭ಬ")
        bstack1ll1l_opy_ = bstack1l_opy_ (u"ࠫࠥ࠭ಭ").join(bstack1ll1l1l_opy_)
        if not self.driver_before_scenario:
          bstack1l11ll1l1_opy_(context, bstack1ll1l_opy_, bstack1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦಮ"))
          bstack11llll11_opy_(context, bstack1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨಯ"), bstack1ll11l1_opy_)
          context.browser.execute_script(bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬರ") + json.dumps(bstack1ll1l_opy_) + bstack1l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨಱ"))
          context.browser.execute_script(bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩಲ") + json.dumps(bstack1l_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣಳ") + str(bstack1ll11l1_opy_)) + bstack1l_opy_ (u"ࠫࢂࢃࠧ಴"))
      else:
        if not self.driver_before_scenario:
          bstack1l11ll1l1_opy_(context, bstack1l_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣವ") + str(self.feature.name) + bstack1l_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣಶ"), bstack1l_opy_ (u"ࠢࡪࡰࡩࡳࠧಷ"))
          bstack11llll11_opy_(context, bstack1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣಸ"))
          context.browser.execute_script(bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧಹ") + json.dumps(bstack1l_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨ಺") + str(self.feature.name) + bstack1l_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨ಻")) + bstack1l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀ಼ࠫ"))
          context.browser.execute_script(bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࡾࡿࠪಽ"))
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩಾ").format(str(e)))
  if name in [bstack1l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨಿ"), bstack1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪೀ")]:
    bstack1l1111_opy_(self, name, context, *args)
    if (name == bstack1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫು") and self.driver_before_scenario) or (name == bstack1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫೂ") and not self.driver_before_scenario):
      try:
        context.browser.quit()
      except Exception:
        pass
def bstack11lll1ll_opy_(config, startdir):
  return bstack1l_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥೃ").format(bstack1l_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧೄ"))
class Notset:
  def __repr__(self):
    return bstack1l_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤ೅")
notset = Notset()
def bstack11lllll1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack111ll1l1_opy_
  if str(name).lower() == bstack1l_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨೆ"):
    return bstack1l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣೇ")
  else:
    return bstack111ll1l1_opy_(self, name, default, skip)
def bstack1lll1l111_opy_(bstack1l111l_opy_):
  global bstack11ll1l11_opy_
  global bstack11ll1111_opy_
  bstack11ll1l11_opy_ = bstack1l111l_opy_
  logger.info(bstack11l11l1_opy_.format(bstack11ll1l11_opy_.split(bstack1l_opy_ (u"ࠪ࠱ࠬೈ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    Service.start = bstack11l1ll11_opy_
    Service.stop = bstack1lll11lll_opy_
    webdriver.Remote.__init__ = bstack1l1l1l111_opy_
    webdriver.Remote.get = bstack111l11l_opy_
    WebDriver.close = bstack1l111l1l1_opy_
    bstack11ll1111_opy_ = True
  except Exception as e:
    pass
  bstack1l1ll111l_opy_()
  if not bstack11ll1111_opy_:
    bstack111ll1ll_opy_(bstack1l_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨ೉"), bstack1l1ll1lll_opy_)
  if bstack1l11l11l1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l1lll111_opy_
    except Exception as e:
      logger.error(bstack111lll1_opy_.format(str(e)))
  if (bstack1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫೊ") in str(bstack1l111l_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1lll1l1l_opy_
      except Exception as e:
        logger.warn(bstack111111_opy_ + str(e))
    except Exception as e:
      bstack111ll1ll_opy_(e, bstack111111_opy_)
    Output.end_test = bstack11llll1_opy_
    TestStatus.__init__ = bstack11l1_opy_
    QueueItem.__init__ = bstack1l1l1l1l_opy_
    pabot._create_items = bstack1llll11_opy_
    try:
      from pabot import __version__ as bstack111lll11_opy_
      if version.parse(bstack111lll11_opy_) >= version.parse(bstack1l_opy_ (u"࠭࠲࠯࠳࠸࠲࠵࠭ೋ")):
        pabot._run = bstack1l111l111_opy_
      elif version.parse(bstack111lll11_opy_) >= version.parse(bstack1l_opy_ (u"ࠧ࠳࠰࠴࠷࠳࠶ࠧೌ")):
        pabot._run = bstack1lll1l1_opy_
      else:
        pabot._run = bstack111lll1l_opy_
    except Exception as e:
      pabot._run = bstack111lll1l_opy_
    pabot._create_command_for_execution = bstack111ll_opy_
    pabot._report_results = bstack1ll1lll_opy_
  if bstack1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ್") in str(bstack1l111l_opy_).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack111ll1ll_opy_(e, bstack1lllll1_opy_)
    Runner.run_hook = bstack1l1l11l1l_opy_
    Step.run = bstack1l1lll11_opy_
  if bstack1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ೎") in str(bstack1l111l_opy_).lower():
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11lll1ll_opy_
      Config.getoption = bstack11lllll1_opy_
    except Exception as e:
      pass
def bstack1lll111ll_opy_():
  global CONFIG
  if bstack1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ೏") in CONFIG and int(CONFIG[bstack1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ೐")]) > 1:
    logger.warn(bstack1l11ll111_opy_)
def bstack1111lll_opy_(bstack1l1111l_opy_, index):
  bstack1lll1l111_opy_(bstack1lll1ll1l_opy_)
  exec(open(bstack1l1111l_opy_).read())
def bstack1l111ll11_opy_(arg):
  global CONFIG
  bstack1lll1l111_opy_(bstack1ll1ll11_opy_)
  os.environ[bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭೑")] = CONFIG[bstack1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ೒")]
  os.environ[bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ೓")] = CONFIG[bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ೔")]
  from _pytest.config import main as bstack11l1llll_opy_
  bstack11l1llll_opy_(arg)
def bstack111llll1_opy_(arg):
  bstack1lll1l111_opy_(bstack1l1llllll_opy_)
  from behave.__main__ import main as bstack11lllll_opy_
  bstack11lllll_opy_(arg)
def bstack1111111_opy_():
  logger.info(bstack1l11llll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨೕ"), help=bstack1l_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫೖ"))
  parser.add_argument(bstack1l_opy_ (u"ࠫ࠲ࡻࠧ೗"), bstack1l_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ೘"), help=bstack1l_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬ೙"))
  parser.add_argument(bstack1l_opy_ (u"ࠧ࠮࡭ࠪ೚"), bstack1l_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧ೛"), help=bstack1l_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪ೜"))
  parser.add_argument(bstack1l_opy_ (u"ࠪ࠱࡫࠭ೝ"), bstack1l_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩೞ"), help=bstack1l_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ೟"))
  bstack1lll11111_opy_ = parser.parse_args()
  try:
    bstack111l1111_opy_ = bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪೠ")
    if bstack1lll11111_opy_.framework and bstack1lll11111_opy_.framework not in (bstack1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧೡ"), bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩೢ")):
      bstack111l1111_opy_ = bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨೣ")
    bstack11ll111_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l1111_opy_)
    bstack11llllll_opy_ = open(bstack11ll111_opy_, bstack1l_opy_ (u"ࠪࡶࠬ೤"))
    bstack11111ll1_opy_ = bstack11llllll_opy_.read()
    bstack11llllll_opy_.close()
    if bstack1lll11111_opy_.username:
      bstack11111ll1_opy_ = bstack11111ll1_opy_.replace(bstack1l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ೥"), bstack1lll11111_opy_.username)
    if bstack1lll11111_opy_.key:
      bstack11111ll1_opy_ = bstack11111ll1_opy_.replace(bstack1l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ೦"), bstack1lll11111_opy_.key)
    if bstack1lll11111_opy_.framework:
      bstack11111ll1_opy_ = bstack11111ll1_opy_.replace(bstack1l_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ೧"), bstack1lll11111_opy_.framework)
    file_name = bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ೨")
    file_path = os.path.abspath(file_name)
    bstack1lll111l_opy_ = open(file_path, bstack1l_opy_ (u"ࠨࡹࠪ೩"))
    bstack1lll111l_opy_.write(bstack11111ll1_opy_)
    bstack1lll111l_opy_.close()
    logger.info(bstack1111ll11_opy_)
    try:
      os.environ[bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ೪")] = bstack1lll11111_opy_.framework if bstack1lll11111_opy_.framework != None else bstack1l_opy_ (u"ࠥࠦ೫")
      config = yaml.safe_load(bstack11111ll1_opy_)
      config[bstack1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ೬")] = bstack1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫ೭")
      bstack1l11l1lll_opy_(bstack11llll1ll_opy_, config)
    except Exception as e:
      logger.debug(bstack1l111111l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11ll1l1l_opy_.format(str(e)))
def bstack1l11l1lll_opy_(bstack1l1l11_opy_, config, bstack1ll11ll1_opy_ = {}):
  global bstack1ll111lll_opy_
  if not config:
    return
  bstack11ll1l1_opy_ = bstack11ll11_opy_ if not bstack1ll111lll_opy_ else ( bstack1lll11l1l_opy_ if bstack1l_opy_ (u"࠭ࡡࡱࡲࠪ೮") in config else bstack1llll1_opy_ )
  data = {
    bstack1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ೯"): config[bstack1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ೰")],
    bstack1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬೱ"): config[bstack1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ೲ")],
    bstack1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨೳ"): bstack1l1l11_opy_,
    bstack1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ೴"): {
      bstack1l_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ೵"): str(config[bstack1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ೶")]) if bstack1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ೷") in config else bstack1l_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥ೸"),
      bstack1l_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬ೹"): bstack111ll1l_opy_(os.getenv(bstack1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨ೺"), bstack1l_opy_ (u"ࠧࠨ೻"))),
      bstack1l_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨ೼"): bstack1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ೽"),
      bstack1l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ೾"): bstack11ll1l1_opy_,
      bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ೿"): config[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ഀ")]if config[bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧഁ")] else bstack1l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨം"),
      bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨഃ"): str(config[bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩഄ")]) if bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪഅ") in config else bstack1l_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥആ"),
      bstack1l_opy_ (u"ࠪࡳࡸ࠭ഇ"): sys.platform,
      bstack1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ഈ"): socket.gethostname()
    }
  }
  update(data[bstack1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨഉ")], bstack1ll11ll1_opy_)
  try:
    response = bstack1l111lll_opy_(bstack1l_opy_ (u"࠭ࡐࡐࡕࡗࠫഊ"), bstack1l11ll1l_opy_, data, config)
    if response:
      logger.debug(bstack1l1ll11_opy_.format(bstack1l1l11_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack111lll_opy_.format(str(e)))
def bstack1l111lll_opy_(type, url, data, config):
  bstack11l1l_opy_ = bstack11ll11ll_opy_.format(url)
  proxy = bstack1111lll1_opy_(config)
  proxies = {}
  response = {}
  if config.get(bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪഋ")) or config.get(bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬഌ")):
    proxies = {
      bstack1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ഍"): proxy
    }
  if type == bstack1l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨഎ"):
    response = requests.post(bstack11l1l_opy_, json=data,
                    headers={bstack1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪഏ"): bstack1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨഐ")}, auth=(config[bstack1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ഑")], config[bstack1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪഒ")]), proxies=proxies)
  return response
def bstack111ll1l_opy_(framework):
  return bstack1l_opy_ (u"ࠣࡽࢀ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧഓ").format(str(framework), __version__) if framework else bstack1l_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥഔ").format(__version__)
def bstack1llll1l_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1l111l1l_opy_()
    logger.debug(bstack1l111llll_opy_.format(str(CONFIG)))
    bstack1ll1ll11l_opy_()
    bstack1ll1111l1_opy_()
  except Exception as e:
    logger.error(bstack1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴ࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢക") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1llllll11_opy_
  atexit.register(bstack1l1l11ll1_opy_)
  signal.signal(signal.SIGINT, bstack1l11l1_opy_)
  signal.signal(signal.SIGTERM, bstack1l11l1_opy_)
def bstack1llllll11_opy_(exctype, value, traceback):
  global bstack1ll111ll1_opy_
  try:
    for driver in bstack1ll111ll1_opy_:
      driver.execute_script(
        bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠣࠫഖ") + json.dumps(bstack1l_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣഗ") + str(value)) + bstack1l_opy_ (u"࠭ࡽࡾࠩഘ"))
  except Exception:
    pass
  bstack1ll11ll1l_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1ll11ll1l_opy_(message = bstack1l_opy_ (u"ࠧࠨങ")):
  global CONFIG
  try:
    if message:
      bstack1ll11ll1_opy_ = {
        bstack1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧച"): str(message)
      }
      bstack1l11l1lll_opy_(bstack1l11ll11_opy_, CONFIG, bstack1ll11ll1_opy_)
    else:
      bstack1l11l1lll_opy_(bstack1l11ll11_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l1l11lll_opy_.format(str(e)))
def bstack1ll1111_opy_(bstack1l1llll1_opy_, size):
  bstack1l11111l1_opy_ = []
  while len(bstack1l1llll1_opy_) > size:
    bstack1l11llll1_opy_ = bstack1l1llll1_opy_[:size]
    bstack1l11111l1_opy_.append(bstack1l11llll1_opy_)
    bstack1l1llll1_opy_   = bstack1l1llll1_opy_[size:]
  bstack1l11111l1_opy_.append(bstack1l1llll1_opy_)
  return bstack1l11111l1_opy_
def run_on_browserstack():
  if len(sys.argv) <= 1:
    logger.critical(bstack11lllll11_opy_)
    return
  if sys.argv[1] == bstack1l_opy_ (u"ࠩ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬഛ")  or sys.argv[1] == bstack1l_opy_ (u"ࠪ࠱ࡻ࠭ജ"):
    logger.info(bstack1l_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠠࡷࡽࢀࠫഝ").format(__version__))
    return
  if sys.argv[1] == bstack1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫഞ"):
    bstack1111111_opy_()
    return
  args = sys.argv
  bstack1llll1l_opy_()
  global CONFIG
  global bstack1l111ll1l_opy_
  global bstack1lllll1l1_opy_
  global bstack1lll1l11_opy_
  global bstack1ll11111l_opy_
  global bstack1l1l1lll_opy_
  bstack1ll11ll_opy_ = bstack1l_opy_ (u"࠭ࠧട")
  if args[1] == bstack1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧഠ") or args[1] == bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩഡ"):
    bstack1ll11ll_opy_ = bstack1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩഢ")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩണ"):
    bstack1ll11ll_opy_ = bstack1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪത")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫഥ"):
    bstack1ll11ll_opy_ = bstack1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬദ")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨധ"):
    bstack1ll11ll_opy_ = bstack1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩന")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩഩ"):
    bstack1ll11ll_opy_ = bstack1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪപ")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫഫ"):
    bstack1ll11ll_opy_ = bstack1l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬബ")
    args = args[2:]
  else:
    if not bstack1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩഭ") in CONFIG or str(CONFIG[bstack1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪമ")]).lower() in [bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨയ"), bstack1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪര")]:
      bstack1ll11ll_opy_ = bstack1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪറ")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧല")]).lower() == bstack1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫള"):
      bstack1ll11ll_opy_ = bstack1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬഴ")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪവ")]).lower() == bstack1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧശ"):
      bstack1ll11ll_opy_ = bstack1l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨഷ")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭സ")]).lower() == bstack1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫഹ"):
      bstack1ll11ll_opy_ = bstack1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬഺ")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬഻ࠩ")]).lower() == bstack1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫഼ࠧ"):
      bstack1ll11ll_opy_ = bstack1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨഽ")
      args = args[1:]
    else:
      os.environ[bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫാ")] = bstack1ll11ll_opy_
      bstack1l1lll1ll_opy_(bstack1llll1l1l_opy_)
  global bstack1l1111l1_opy_
  try:
    os.environ[bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬി")] = bstack1ll11ll_opy_
    bstack1l11l1lll_opy_(bstack1l11ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l1l11lll_opy_.format(str(e)))
  global bstack111111l1_opy_
  global bstack111llll_opy_
  global bstack1111111l_opy_
  global bstack111111l_opy_
  global bstack1ll11l1l_opy_
  global bstack11ll111l_opy_
  global bstack1l11l111_opy_
  global bstack1111l1ll_opy_
  global bstack1l1111_opy_
  global bstack1lll111_opy_
  global bstack1ll1111l_opy_
  global bstack11ll_opy_
  global bstack111ll1l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack111111l1_opy_ = webdriver.Remote.__init__
    bstack1111l1ll_opy_ = WebDriver.close
    bstack1ll1111l_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1111l1_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack1l111111_opy_():
    if bstack1ll1l1111_opy_() < version.parse(bstack11l1l1_opy_):
      logger.error(bstack1l1ll1l_opy_.format(bstack1ll1l1111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11ll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack111lll1_opy_.format(str(e)))
  bstack1lllll_opy_()
  if (bstack1ll11ll_opy_ in [bstack1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪീ"), bstack1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫു"), bstack1l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧൂ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1lll1l1l_opy_
      except Exception as e:
        logger.warn(bstack111111_opy_ + str(e))
    except Exception as e:
      bstack111ll1ll_opy_(e, bstack111111_opy_)
    bstack111llll_opy_ = Output.end_test
    bstack1111111l_opy_ = TestStatus.__init__
    bstack1ll11l1l_opy_ = pabot._run
    bstack11ll111l_opy_ = QueueItem.__init__
    bstack1l11l111_opy_ = pabot._create_command_for_execution
  if bstack1ll11ll_opy_ == bstack1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧൃ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack111ll1ll_opy_(e, bstack1lllll1_opy_)
    bstack1l1111_opy_ = Runner.run_hook
    bstack1lll111_opy_ = Step.run
  if bstack1ll11ll_opy_ == bstack1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨൄ"):
    try:
      from _pytest.config import Config
      bstack111ll1l1_opy_ = Config.getoption
    except Exception as e:
      logger.warn(e, bstack1lll1111_opy_)
  if bstack1ll11ll_opy_ == bstack1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ൅"):
    bstack1llll11ll_opy_()
    bstack1lll111ll_opy_()
    if bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭െ") in CONFIG:
      bstack1lllll1l1_opy_ = True
      bstack1l1ll1l1_opy_ = []
      for index, platform in enumerate(CONFIG[bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧേ")]):
        bstack1l1ll1l1_opy_.append(bstack1ll11lll_opy_(name=str(index),
                                      target=bstack1111lll_opy_, args=(args[0], index)))
      for t in bstack1l1ll1l1_opy_:
        t.start()
      for t in bstack1l1ll1l1_opy_:
        t.join()
    else:
      bstack1lll1l111_opy_(bstack1lll1ll1l_opy_)
      exec(open(args[0]).read())
  elif bstack1ll11ll_opy_ == bstack1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫൈ") or bstack1ll11ll_opy_ == bstack1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ൉"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack111ll1ll_opy_(e, bstack111111_opy_)
    bstack1llll11ll_opy_()
    bstack1lll1l111_opy_(bstack1l1l11111_opy_)
    if bstack1l_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬൊ") in args:
      i = args.index(bstack1l_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ോ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1l111ll1l_opy_))
    args.insert(0, str(bstack1l_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧൌ")))
    pabot.main(args)
  elif bstack1ll11ll_opy_ == bstack1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯്ࠫ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack111ll1ll_opy_(e, bstack111111_opy_)
    for a in args:
      if bstack1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪൎ") in a:
        bstack1lll1l11_opy_ = int(a.split(bstack1l_opy_ (u"ࠬࡀࠧ൏"))[1])
      if bstack1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ൐") in a:
        bstack1ll11111l_opy_ = str(a.split(bstack1l_opy_ (u"ࠧ࠻ࠩ൑"))[1])
      if bstack1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨ൒") in a:
        bstack1l1l1lll_opy_ = str(a.split(bstack1l_opy_ (u"ࠩ࠽ࠫ൓"))[1])
    bstack1lll1l111_opy_(bstack1l1l11111_opy_)
    run_cli(args)
  elif bstack1ll11ll_opy_ == bstack1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪൔ"):
    try:
      from _pytest.config import _prepareconfig
      from _pytest.config import Config
      import importlib
      bstack1l111l1ll_opy_ = importlib.find_loader(bstack1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ൕ"))
    except Exception as e:
      logger.warn(e, bstack1lll1111_opy_)
    bstack1llll11ll_opy_()
    try:
      if bstack1l_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧൖ") in args:
        i = args.index(bstack1l_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨൗ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪ൘") in args:
        i = args.index(bstack1l_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫ൙"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"ࠩ࠰ࡴࠬ൚") in args:
        i = args.index(bstack1l_opy_ (u"ࠪ࠱ࡵ࠭൛"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ൜") in args:
        i = args.index(bstack1l_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭൝"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"࠭࠭࡯ࠩ൞") in args:
        i = args.index(bstack1l_opy_ (u"ࠧ࠮ࡰࠪൟ"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack11111l11_opy_ = config.args
    bstack111l111l_opy_ = config.invocation_params.args
    bstack111l111l_opy_ = list(bstack111l111l_opy_)
    bstack1l1l111l1_opy_ = []
    for arg in bstack111l111l_opy_:
      for spec in bstack11111l11_opy_:
        if os.path.normpath(arg) != os.path.normpath(spec):
          bstack1l1l111l1_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack1l_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩൠ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11111l11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l11l11l_opy_)))
                    for bstack1l11l11l_opy_ in bstack11111l11_opy_]
    if (bstack1ll11_opy_):
      bstack1l1l111l1_opy_.append(bstack1l_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ൡ"))
      bstack1l1l111l1_opy_.append(bstack1l_opy_ (u"ࠪࡘࡷࡻࡥࠨൢ"))
    bstack1l1l111l1_opy_.append(bstack1l_opy_ (u"ࠫ࠲ࡶࠧൣ"))
    bstack1l1l111l1_opy_.append(bstack1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠪ൤"))
    bstack1l1l111l1_opy_.append(bstack1l_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨ൥"))
    bstack1l1l111l1_opy_.append(bstack1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ൦"))
    bstack11l1l1l_opy_ = []
    for spec in bstack11111l11_opy_:
      bstack11ll11l_opy_ = []
      bstack11ll11l_opy_.append(spec)
      bstack11ll11l_opy_ += bstack1l1l111l1_opy_
      bstack11l1l1l_opy_.append(bstack11ll11l_opy_)
    bstack1lllll1l1_opy_ = True
    bstack1l111l11l_opy_ = 1
    if bstack1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ൧") in CONFIG:
      bstack1l111l11l_opy_ = CONFIG[bstack1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ൨")]
    bstack1ll1l1l1_opy_ = int(bstack1l111l11l_opy_)*int(len(CONFIG[bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭൩")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ൪")]):
      for bstack11ll11l_opy_ in bstack11l1l1l_opy_:
        item = {}
        item[bstack1l_opy_ (u"ࠬࡧࡲࡨࠩ൫")] = bstack11ll11l_opy_
        item[bstack1l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ൬")] = index
        execution_items.append(item)
    bstack111ll11l_opy_ = bstack1ll1111_opy_(execution_items, bstack1ll1l1l1_opy_)
    for execution_item in bstack111ll11l_opy_:
      bstack1l1ll1l1_opy_ = []
      for item in execution_item:
        bstack1l1ll1l1_opy_.append(bstack1ll11lll_opy_(name=str(item[bstack1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭൭")]),
                                            target=bstack1l111ll11_opy_,
                                            args=(item[bstack1l_opy_ (u"ࠨࡣࡵ࡫ࠬ൮")],)))
      for t in bstack1l1ll1l1_opy_:
        t.start()
      for t in bstack1l1ll1l1_opy_:
        t.join()
  elif bstack1ll11ll_opy_ == bstack1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ൯"):
    try:
      from behave.__main__ import main as bstack11lllll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack111ll1ll_opy_(e, bstack1lllll1_opy_)
    bstack1llll11ll_opy_()
    bstack1lllll1l1_opy_ = True
    bstack1l111l11l_opy_ = 1
    if bstack1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ൰") in CONFIG:
      bstack1l111l11l_opy_ = CONFIG[bstack1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ൱")]
    bstack1ll1l1l1_opy_ = int(bstack1l111l11l_opy_)*int(len(CONFIG[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ൲")]))
    config = Configuration(args)
    bstack11111l11_opy_ = config.paths
    bstack1ll1ll111_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack11111l11_opy_:
        bstack1ll1ll111_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack1l_opy_ (u"࠭ࡷࡪࡰࡧࡳࡼࡹࠧ൳"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11111l11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l11l11l_opy_)))
                    for bstack1l11l11l_opy_ in bstack11111l11_opy_]
    bstack11l1l1l_opy_ = []
    for spec in bstack11111l11_opy_:
      bstack11ll11l_opy_ = []
      bstack11ll11l_opy_ += bstack1ll1ll111_opy_
      bstack11ll11l_opy_.append(spec)
      bstack11l1l1l_opy_.append(bstack11ll11l_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ൴")]):
      for bstack11ll11l_opy_ in bstack11l1l1l_opy_:
        item = {}
        item[bstack1l_opy_ (u"ࠨࡣࡵ࡫ࠬ൵")] = bstack1l_opy_ (u"ࠩࠣࠫ൶").join(bstack11ll11l_opy_)
        item[bstack1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ൷")] = index
        execution_items.append(item)
    bstack111ll11l_opy_ = bstack1ll1111_opy_(execution_items, bstack1ll1l1l1_opy_)
    for execution_item in bstack111ll11l_opy_:
      bstack1l1ll1l1_opy_ = []
      for item in execution_item:
        bstack1l1ll1l1_opy_.append(bstack1ll11lll_opy_(name=str(item[bstack1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ൸")]),
                                            target=bstack111llll1_opy_,
                                            args=(item[bstack1l_opy_ (u"ࠬࡧࡲࡨࠩ൹")],)))
      for t in bstack1l1ll1l1_opy_:
        t.start()
      for t in bstack1l1ll1l1_opy_:
        t.join()
  else:
    bstack1l1lll1ll_opy_(bstack1llll1l1l_opy_)
  bstack1l1ll11l_opy_()
def bstack1l1ll11l_opy_():
  global CONFIG
  try:
    if bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩൺ") in CONFIG:
      host = bstack1l_opy_ (u"ࠧࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦࠪൻ") if bstack1l_opy_ (u"ࠨࡣࡳࡴࠬർ") in CONFIG else bstack1l_opy_ (u"ࠩࡤࡴ࡮࠭ൽ")
      user = CONFIG[bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬൾ")]
      key = CONFIG[bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧൿ")]
      bstack1l1111ll1_opy_ = bstack1l_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ඀") if bstack1l_opy_ (u"࠭ࡡࡱࡲࠪඁ") in CONFIG else bstack1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩං")
      url = bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡽࢀ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠱࡮ࡸࡵ࡮ࠨඃ").format(user, key, host, bstack1l1111ll1_opy_)
      headers = {
        bstack1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ඄"): bstack1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭අ"),
      }
      if bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ආ") in CONFIG:
        params = {bstack1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪඇ"):CONFIG[bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩඈ")], bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪඉ"):CONFIG[bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪඊ")]}
      else:
        params = {bstack1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧඋ"):CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ඌ")]}
      response = requests.get(url, params=params, headers=headers)
      if response.json():
        bstack1ll11lll1_opy_ = response.json()[0][bstack1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡤࡸ࡭ࡱࡪࠧඍ")]
        if bstack1ll11lll1_opy_:
          bstack1l1l1_opy_ = bstack1ll11lll1_opy_[bstack1l_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩඎ")].split(bstack1l_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨ࠳ࡢࡶ࡫࡯ࡨࠬඏ"))[0] + bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡹ࠯ࠨඐ") + bstack1ll11lll1_opy_[bstack1l_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫඑ")]
          logger.info(bstack111lllll_opy_.format(bstack1l1l1_opy_))
          bstack1l1ll1l11_opy_ = CONFIG[bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬඒ")]
          if bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬඓ") in CONFIG:
            bstack1l1ll1l11_opy_ += bstack1l_opy_ (u"ࠫࠥ࠭ඔ") + CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧඕ")]
          if bstack1l1ll1l11_opy_!= bstack1ll11lll1_opy_[bstack1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫඖ")]:
            logger.debug(bstack11l11111_opy_.format(bstack1ll11lll1_opy_[bstack1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ඗")], bstack1l1ll1l11_opy_))
    else:
      logger.warn(bstack1l1l1111l_opy_)
  except Exception as e:
    logger.debug(bstack1ll1l1_opy_.format(str(e)))
def bstack1ll1llll_opy_(url, bstack1llll111_opy_=False):
  global CONFIG
  global bstack1lll1l_opy_
  if not bstack1lll1l_opy_:
    hostname = bstack11llll_opy_(url)
    is_private = bstack1ll111l1l_opy_(hostname)
    if (bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ඘") in CONFIG and not CONFIG[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭඙")]) and (is_private or bstack1llll111_opy_):
      bstack1lll1l_opy_ = hostname
def bstack11llll_opy_(url):
  return urlparse(url).hostname
def bstack1ll111l1l_opy_(hostname):
  for bstack1l11111ll_opy_ in bstack1lllll11_opy_:
    regex = re.compile(bstack1l11111ll_opy_)
    if regex.match(hostname):
      return True
  return False