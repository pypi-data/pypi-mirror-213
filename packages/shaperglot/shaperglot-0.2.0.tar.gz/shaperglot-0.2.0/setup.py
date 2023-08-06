# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shaperglot', 'shaperglot.checks']

package_data = \
{'': ['*'], 'shaperglot': ['languages/*']}

install_requires = \
['gflanguages>=0.4.7',
 'num2words>=0.5,<0.6',
 'protobuf==3.19.4',
 'strictyaml',
 'termcolor==1.1.0',
 'ufo2ft',
 'vharfbuzz>=0,<1',
 'youseedee']

entry_points = \
{'console_scripts': ['shaperglot = shaperglot.cli:main']}

setup_kwargs = {
    'name': 'shaperglot',
    'version': '0.2.0',
    'description': 'Test font files for OpenType language support',
    'long_description': '# Shaperglot - Test font files for OpenType language support\n\n[![PyPI Version](https://img.shields.io/pypi/v/shaperglot.svg)](https://pypi.org/project/shaperglot)\n[![PyPI License](https://img.shields.io/pypi/l/shaperglot.svg)](https://pypi.org/project/shaperglot)\n\nShaperglot is a library and a utility for testing a font\'s language support.\nYou give it a font, and it tells you what languages are supported and to what\ndegree.\n\nMost other libraries to check for language support (for example, Rosetta\'s\nwonderful [hyperglot](https://hyperglot.rosettatype.com) library) do this by\nlooking at the Unicode codepoints that the font supports. Shaperglot takes\na different approach.\n\n## What\'s wrong with the Unicode codepoint coverage approach?\n\nFor many common languages, it\'s possible to check that the language is\nsupported just by looking at the Unicode coverage. For example, to support\nEnglish, you need the 26 lowercase and uppercase letters of the Latin alphabet.\n\nHowever, for the majority of scripts around the world, covering the codepoints\nneeded is not enough to say that a font really *supports* a particular language.\nFor correct language support, the font must also *behave* in a particular way.\n\nTake the case of Arabic as an example. A font might contain glyphs which cover\nall the codepoints in the Arabic block (0x600-0x6FF). But the font only *supports*\nArabic if it implements joining rules for the `init`, `medi` and `fina` features.\nTo say that a font supports Devanagari, it needs to implement conjuncts (which\nset of conjuncts need to be included before we can say the font "supports"\nDevanagari is debated...) and half forms, as well as contain a `languagesystem`\nstatement which triggers Indic reordering.\n\nEven within the Latin script, a font only supports a language such as Turkish\nif its casing behaving respects the dotless / dotted I distinction; a font\nonly supports Navajo if its ogonek anchoring is different to the anchoring used in\nPolish; and so on.\n\nBut there\'s a further problem with testing language support by codepoint coverage:\nit encourages designers to "fill in the blanks" to get to support, rather than\nnecessarily engage with the textual requirements of particular languages.\n\n## Testing for behaviour, not coverage\n\nShaperglot therefore determines language support not just on codepoint coverage,\nbut also by examining how the font behaves when confronted with certain character\nsequences.\n\nThe trick is to do this in a way which is not prescriptive. We know that there\nare many different ways of implementing language support within a font, and that\ndesign and other considerations will factor into precisely how a font is\nconstructed. Shaperglot presents the font with different strings, and makes sure\nthat "something interesting happened" - without necessarily specifying what.\n\nIn the case of Arabic, we need to know that the `init` feature is present, and that\nwhen we shape some Arabic glyphs, the output with `init` turned on is different\nto the output with `init` turned off. We don\'t care what\'s different; we only\ncare that something has happened. *(Yes, this still makes it possible to trick shaperglot into reporting support for a language which is not correctly implemented, but at that point, it\'s probably less effort to actually implement it...)*\n\nShaperglot includes (or will include) the following kinds of test:\n\n* Certain codepoints were mapped to base or mark glyphs.\n* A named feature was present.\n* A named feature changed the output glyphs.\n* A mark glyph was attached to a base glyph or composed into a precomposed glyph (but not left unattached).\n* Certain glyphs in the output were different to one another.\n* Languagesystems were defined in the font.\n* ...\n\nUsing this library of tests, we then create language support definitions which\nexercise the font\'s capabilities to obtain a fuller picture of its support for\na particular language. These language support definitions, expressed as YAML\nfiles, are the core of Shaperglot; to extend and improve Shaperglot, we need as\nmany language support definition files as possible - so if you know a language\nwell and can express what it means to "support" that language properly, please\ncontribute a definition!\n\n## Using Shaperglot\n\nTo report whether or not a given language is supported, pass a font and one or\nmore ISO639-3 language codes. \n\n```\n$ shaperglot -v -v MyFont.ttf urd\nFont does not fully support language \'urd\'\n * PASS: All base glyphs were present in the font\n * FAIL: Some mark glyphs were missing: ْ\n * PASS: Required feature \'mark\' was present\n * PASS: Mark glyph ◌َ  (FATHA) took part in a mark positioning rule\n * PASS: Mark glyph ◌ُ  (DAMMA) took part in a mark positioning rule\n * PASS: Mark glyph ◌ِ  (KASRA) took part in a mark positioning rule\n * PASS: Mark glyph ◌ٰ  (LONG_A) took part in a mark positioning rule\n * PASS: Required feature \'init\' was present\n * PASS: Glyph ع (AINu1) took part in a init rule\n * PASS: Required feature \'medi\' was present\n * PASS: Glyph ع (AINu1) took part in a medi rule\n * PASS: Required feature \'fina\' was present\n * PASS: Glyph ع (AINu1) took part in a fina rule\n * PASS: Repeated beh forms should produce different shapes\n * PASS: Initial and final forms should differ\n```\n\nShaperglot can also be run in bulk mode to check language support of entire font libraries. This is done by running `bulk-run-sg-.py` located in the scripts folder.\n\n```\n$ python bulk-run-sg.py ./<path-to-font-library>\n```\n\nThis script will automatically drill down the direcory tree and identify all .ttf font files and check them against a subset of language tags. At this time `bulk-run-sg.py` only checks fonts for Pan-African language support. The list of relevant language tags are defined in `language_tag_data/iso639-3-afr-all.txt`. Shaperglot results procesed in bulk can be quite large and may require additional tools to analyze. See [font-lang-support-afr](https://github.com/JamraPatel/font-lang-support-afr) for an example of how bulk results can be reported. Results are saved into two `.json` files.\n\n```\nresults.json\nafr_tag_overview.json\n```\n\n`results.json` contains the checker results (`<failure type>: <failure details>`) for each language tag, broken down by font.\n`afr_tag_overview.json` is a summary of which fonts in the library pass and fail for each language tag that was checked.\n\n\n# Setup\n\n## Requirements\n\n* Python 3.9+\n\n## Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\n$ pip install shaperglot\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add shaperglot\n```\n\n# Usage\n\nAfter installation, the package can imported:\n\n```text\n$ python\n>>> import shaperglot\n>>> shaperglot.__version__\n```\n',
    'author': 'Simon Cozens',
    'author_email': 'simon@simon-cozens.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/shaperglot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
