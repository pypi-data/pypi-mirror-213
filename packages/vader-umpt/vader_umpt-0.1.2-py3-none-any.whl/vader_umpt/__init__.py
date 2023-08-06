#!/usr/bin/env python3

from argparse import ArgumentParser
from . import vader
import os
import json
import sys
from typing import cast, Dict, Any


def main():
    parser = ArgumentParser(
        prog="VADER-UMPT",
        description="Ferramenta para análise de sentimento em português",
    )

    parser.add_argument(
        "--export-dicts", help="Exporta os dicionários", action="store_true"
    )

    parser.add_argument(
        "-l",
        "--lexicon",
        help="Ficheiro com o dicionário a ser utilizado",
        type=str,
        default=os.path.join(
            vader.PACKAGE_DIRECTORY, "lexicons", "vader_lexicon_ptbr.txt"
        ),
    )
    parser.add_argument(
        "--emoji-lexicon",
        help="Ficheiro com o dicionário de emojis a ser utilizado",
        type=str,
        default=os.path.join(
            vader.PACKAGE_DIRECTORY, "lexicons", "emoji_utf8_lexicon_ptbr.txt"
        ),
    )
    parser.add_argument(
        "-e",
        "--explain",
        help="Imprimir explicação detalhada sobre como a pontuação foi calculada",
        action="store_true",
    )
    parser.add_argument(
        "-w",
        "--web",
        help="Executar um playground web para testar o analisador",
        action="store_true",
    )

    args = parser.parse_args()

    analyser = vader.SentimentIntensityAnalyzer(
        lexicon_file=args.lexicon, emoji_lexicon=args.emoji_lexicon
    )

    if args.web:
        import streamlit.web.bootstrap
        from streamlit import config as _config

        _config.set_option("server.headless", True)
        args = []
        streamlit.web.bootstrap.run(
            os.path.join((os.path.dirname(__file__)), "web.py"),
            "",
            args,
            flag_options={},
        )
    else:
        if args.export_dicts:
            e = {
                "lexicon": analyser.lexicon,
                "emojis": analyser.emojis,
                "punctuation": vader.PUNC_LIST,
                "negation": vader.NEGATE,
                "booster": vader.BOOSTER_DICT,
            }

            print(json.dumps(e, ensure_ascii=False))
        else:
            for line in sys.stdin:
                scores = analyser.polarity_scores(line)
                if not args.explain:
                    print(json.dumps(scores[0], ensure_ascii=False))
                else:
                    new_scores = cast(Dict[str, Any], scores[0])
                    new_scores["explanation"] = scores[1]
                    print(json.dumps(new_scores, ensure_ascii=False))


if __name__ == "__main__":
    main()
