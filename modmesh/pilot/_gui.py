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


"""
Graphical-user interface code
"""

# Use flake8 http://flake8.pycqa.org/en/latest/user/error-codes.html


import sys
import importlib

from . import _pilot_core as _pcore

if _pcore.enable:
    from PySide6.QtGui import QAction
    from . import _mesh

__all__ = [  # noqa: F822
    'launch',
]

_holder = {}


def populate_menu():
    wm = _pcore.RManager.instance

    def _addAction(menu, text, tip, funcname):
        act = QAction(text, wm.mainWindow)
        act.setStatusTip(tip)
        if callable(funcname):
            act.triggered.connect(lambda *a: funcname())
        elif funcname:
            modname, funcname = funcname.rsplit('.', maxsplit=1)
            mod = importlib.import_module(modname)
            func = getattr(mod, funcname)
            act.triggered.connect(lambda *a: func())
        menu.addAction(act)

    _holder['gmsh_dialog'] = _mesh.GmshFileDialog(mgr=wm)
    _holder['gmsh_dialog'].populate_menu()

    if sys.platform != 'darwin':
        _addAction(
            menu=wm.fileMenu,
            text="Exit",
            tip="Exit the application",
            funcname=lambda: wm.quit(),
        )

    _addAction(
        menu=wm.oneMenu,
        text="Euler solver",
        tip="One-dimensional shock-tube problem with Euler solver",
        funcname="modmesh.app.euler1d.load_app",
    )

    _holder['sample_mesh'] = _mesh.SampleMesh(mgr=wm)
    _holder['sample_mesh'].populate_menu()

    _addAction(
        menu=wm.meshMenu,
        text="Sample: NACA 4-digit",
        tip="Draw a NACA 4-digit airfoil",
        funcname="modmesh.gui.naca.runmain",
    )

    _addAction(
        menu=wm.addonMenu,
        text="Load linear_wave",
        tip="Load linear_wave",
        funcname="modmesh.app.linear_wave.load_app",
    )

    _addAction(
        menu=wm.addonMenu,
        text="Load bad_euler1d",
        tip="Load bad_euler1d",
        funcname="modmesh.app.bad_euler1d.load_app",
    )

    _addAction(
        menu=wm.windowMenu,
        text="(empty)",
        tip="(empty)",
        funcname=None,
    )


def launch(name="pilot", size=(1000, 600)):
    """
    The entry point of the pilot GUI application.

    :param name: Main window name.
    :param size: Main window size.
    :return: nothing
    """
    wm = _pcore.RManager.instance
    wm.setUp()
    wm.windowTitle = name
    wm.resize(w=size[0], h=size[1])
    populate_menu()
    wm.show()
    return wm.exec()

# vim: set ff=unix fenc=utf8 et sw=4 ts=4 sts=4:
