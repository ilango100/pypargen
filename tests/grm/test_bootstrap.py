# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import pytest
import pathlib
import io
import pypargen as pgen


@pytest.mark.slow
def test_bootstrap():
    grm_file = pathlib.Path(__file__).parent / "grammar.grm"
    grm1 = pgen.grm.parser.parse(open(grm_file))
    # Grammar is parsed to get the grammar for the grammar

    grm2 = pgen.grm.parser.parse(io.StringIO(str(grm1)))

    grm3 = pgen.grm.parser.parse(io.StringIO(str(grm2)))

    assert grm1 == grm2 == grm3
    with open(grm_file) as grm_fp:
        assert grm_fp.read() == str(grm3)
