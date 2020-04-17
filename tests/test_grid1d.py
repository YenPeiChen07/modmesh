# Copyright (c) 2019, Yung-Yu Chen <yyc@solvcon.net>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import unittest

import numpy as np

import modmesh


class StaticGrid1dTC(unittest.TestCase):

    def test_getset(self):

        gd = modmesh.StaticGrid1d(11)

        self.assertEqual(11, gd.nx)
        self.assertEqual(11, len(gd))

        for it in range(len(gd)):
            gd[it] = it
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], list(gd))

    def test_ndarray(self):

        gd = modmesh.StaticGrid1d(11)

        self.assertEqual(np.float64, gd.coord.dtype)
        gd.coord = np.arange(10, -1, -1, dtype='float64')
        self.assertEqual([10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], list(gd))

        def check_life_cycle():

            gd2 = modmesh.StaticGrid1d(5)
            gd2.coord = np.arange(5, dtype='float64')
            return gd2.coord

        coord = check_life_cycle()
        self.assertEqual([0, 1, 2, 3, 4], coord.tolist())

    def test_fill(self):

        gd = modmesh.StaticGrid1d(11)
        gd.fill(102)

# vim: set ff=unix fenc=utf8 et sw=4 ts=4 sts=4:
