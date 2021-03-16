# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import pytest
import pathlib
import io
from pypargen.grm import parser


@pytest.mark.slow
def test_bootstrap():
    grm_file = pathlib.Path(__file__).parent / "grammar.grm"
    grm_parser = parser.GrmParser()
    with grm_file.open() as fp:
        grm1 = grm_parser.parse(fp)
    # Grammar grammar is parsed to get the grammar for the grammar

    grm2 = grm_parser.parse(io.StringIO(str(grm1)))

    grm3 = grm_parser.parse(io.StringIO(str(grm2)))

    assert grm1 == grm2 == grm3
    with open(grm_file) as grm_fp:
        assert grm_fp.read() == str(grm3)
