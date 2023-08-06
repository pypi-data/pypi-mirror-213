import os
import sys
import html
import tomlkit
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trrc.create_parser import create_parser, parse_argument
from trrc.utils import RegexPattern
import trrc.utils as ankiadderall
from trrc.config_opts import read_toml_config
from unittest import mock


@pytest.fixture
def regex_compiles():
    regex = RegexPattern()
    return regex

@pytest.mark.parametrize("card_str, br_answer, prevent_HTML_answer",
                         [('long <br>sent\\nences\\\\n', 'long <br>sent<br>ences&#92n', 'long &ltbr&gtsent\\nences\\\\n'),
                          ('other <br>sent\\nences\\\\n', 'other <br>sent<br>ences&#92n', 'other &ltbr&gtsent\\nences\\\\n')])
def test_regexes_compiles(regex_compiles, card_str, br_answer, prevent_HTML_answer):

    re_compile = regex_compiles.newline_to_html_br_compile
    pattern = regex_compiles.newline_to_html_br_pattern

    assert re_compile.sub(lambda mo: pattern[mo.group()], card_str) == br_answer

    re_compile = regex_compiles.prevent_html_interpret_compile
    pattern = regex_compiles.prevent_html_interpret_pattern

    assert re_compile.sub(lambda mo: pattern[mo.group()], card_str) == prevent_HTML_answer


@pytest.mark.parametrize("card_str, br_answer, prevent_HTML_answer",
                         [('long <br>sent\\nences\\\\n', 'long <br>sent<br>ences&#92n', 'long &ltbr&gtsent\\nences\\\\n'),
                          ('other <br>sent\\nences\\\\n', 'other <br>sent<br>ences&#92n', 'other &ltbr&gtsent\\nences\\\\n')])
def test_html(regex_compiles, card_str, br_answer, prevent_HTML_answer):

    #assert html.unescape(card_str) == br_answer

#    re_compile = regex_compiles.prevent_html_interpret_compile
#    pattern = regex_compiles.prevent_html_interpret_pattern
#
    assert html.escape(card_str) == prevent_HTML_answer
#    assert re_compile.sub(lambda mo: pattern[mo.group()], card_str) == prevent_HTML_answer
