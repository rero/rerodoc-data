#!/bin/bash
# -*- coding: utf-8 -*-

echo "Building version: $1"
source /rerodoc/rerodoc/bin/activate && \
cd rerodoc/src && \
git clone https://github.com/rero/rerodoc-data.git && \
cd rerodoc-data; pip install .[all]


