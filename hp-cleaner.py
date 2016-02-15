#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 Vale Tolpegin
# Distributed under the terms of the MIT License.

# -- Modules ------------------------------------------------------------------

from cleaner import Cleaner
from Options import parseOptions

# -- Start --------------------------------------------------------------------

Cleaner(*parseOptions())
