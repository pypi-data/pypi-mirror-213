#!/bin/bash

# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

kaitai-struct-compiler --target python --outdir no_vtf/parser/generated ksy/vtf.ksy
