# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)

import pytest

import plopp as pp
from plopp.backends.plotly.figure import Figure
from plopp.data.testing import data_array
from plopp.graphics.figline import FigLine

pytest.importorskip("plotly")


def test_creation():
    da = data_array(ndim=1)
    fig = Figure(pp.Node(da), FigConstructor=FigLine)
    assert fig.canvas.xlabel == f'xx [{da.coords["xx"].unit}]'
    assert fig.canvas.ylabel == f'[{da.unit}]'


def test_logx_1d_toolbar_button():
    da = data_array(ndim=1)
    fig = Figure(pp.Node(da), FigConstructor=FigLine, scale={'xx': 'log'})
    assert fig.toolbar['logx'].value


def test_logy_1d_toolbar_button():
    da = data_array(ndim=1)
    fig = Figure(pp.Node(da), FigConstructor=FigLine, norm='log')
    assert fig.toolbar['logy'].value
