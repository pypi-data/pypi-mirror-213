import json
import shutil
import typing

from checkmytex.latex_document import LatexDocument, Origin

from .abstract_checker import Checker
from .problem import Problem


class Languagetool(Checker):
    def __init__(self, lang="en-US"):
        """
        If you modify the language, you may also have to modify the
        `disable_rules`. These can be modified any time before running `check`.
        :param lang: Language option. E.g. "de-DE" for german. The original
            language tool code used with `-l` in the CLI.
        """
        super().__init__()
        self._lang = lang
        self.disable_rules = [
            f"MORFOLOGIK_RULE_{lang.upper().replace('-', '_').strip()}",
            # disable spell checking because it is very slow.
            "WHITESPACE_RULE",
            # The whitespaces will be off due to detexing.
            "COMMA_PARENTHESIS_WHITESPACE",
            # Also not reliable in detexed text.
            "THE_SUPERLATIVE",  # not true in computer science and math where we can have, e.g., multiple equivalent extremal solutions.
        ]

    def _get_languagetool_json(self, document: LatexDocument) -> dict:
        result, err, ex = self._run(
            f"{shutil.which('languagetool')} --json -l {self._lang} "
            f"--disable {','.join(self.disable_rules)}",
            input=document.get_text(),
        )
        if err:
            self.log(err)
        lines = result.split("\n")
        lines.sort(key=len, reverse=True)
        for line in lines:
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
        self.log("ERROR: Could not read output of languagetool!")
        self.log(result)
        return {}

    def check(self, document: LatexDocument) -> typing.Iterable[Problem]:
        self.log("Running Langugagetool...")
        data = self._get_languagetool_json(document=document)
        for problem in data["matches"]:
            try:
                look_up_url = problem["rule"]["urls"][0]["value"]
            except KeyError:
                look_up_url = None
            origin = document.get_simplified_origin_of_text(
                problem["offset"], problem["offset"] + problem["length"]
            )
            # using source context because the detexed context is too unstable with math
            context = document.get_source_context(origin)
            # the rule 'a/an' results in many false positives before math or commands.
            if self._is_an_before_math(problem, origin, document):
                continue
            # the upper case sentence start rule has an issue with "ABR.\ bla"
            if self._is_uppercase_letter_after_backslash(problem, origin, document):
                continue
            yield Problem(
                origin=origin,
                context=problem["context"]["text"],
                message=problem["message"],
                long_id=problem["message"] + context,
                rule=problem["rule"]["id"],
                tool="languagetool",
                look_up_url=look_up_url,
            )

    def _is_an_before_math(
        self, problem, origin: Origin, document: LatexDocument
    ) -> bool:
        """
        'A' before math or a command will frequently lead to false positives.
        """
        if problem["rule"]["id"] != "EN_A_VS_AN":
            return False
        source = document.get_source()
        context = source[
            origin.end.source.index : max(len(source), origin.end.source.index + 10)
        ].strip()
        if context and context[0] in ("\\", "$"):
            return True
        return False

    def _is_uppercase_letter_after_backslash(
        self, problem, origin: Origin, document: LatexDocument
    ) -> bool:
        if problem["rule"]["id"] != "UPPERCASE_SENTENCE_START":
            return False
        source = document.get_source()
        context = source[
            max(0, origin.begin.source.index - 10) : origin.begin.source.index
        ].strip()
        if context and context[-1] == "\\":
            return True
        return False

    def is_available(self) -> bool:
        return bool(shutil.which("languagetool"))

    def needs_detex(self):
        return True

    def installation_guide(self) -> str:
        return (
            "You can probably install install languagetool directly"
            " with your package manager.\n"
            " e.g. brew install languagetool\n"
            "      apt-get install languagetool\n"
            "      pacman -S languagetool\n"
            "...\n"
            "Otherwise, you can install it by hand:"
            " https://github.com/languagetool-org/languagetool"
        )
