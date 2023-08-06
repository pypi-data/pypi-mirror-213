import os
import re
import typing

import flachtex
from flachtex.command_substitution import NewCommandSubstitution, find_new_commands
from flachtex.rules import ChangesRule, TodonotesRule
from flachtex.rules.skip_rules import RegexSkipRule
from flachtex.utils import Range

from .latex_document import DetexedText, LatexDocument, LatexSource


class _IgnoreRule(RegexSkipRule):
    """
    A skip rule for flachtex to remove parts delimited by `%%PAUSE-CHECKING`
    and `%%CONTINUE-CHECKING`.
    """

    def __init__(self):
        super().__init__(
            r"((^\s*%%PAUSE-CHECKING)"
            r"(?P<skipped_part>.*?)"
            r"(^\s*%%CONTINUE-CHECKING))"
        )

    def determine_skip(self, match: re.Match):
        span_to_be_skipped = Range(
            match.start("skipped_part"), match.end("skipped_part")
        )
        return span_to_be_skipped


class LatexParser:
    def __init__(
        self,
        file_finder: typing.Optional[flachtex.FileFinder] = None,
        yalafi_opts: typing.Optional[typing.Dict] = None,
    ):
        self._ff = file_finder
        self.file_finder = file_finder if file_finder else flachtex.FileFinder()
        self._yalafi_opts = yalafi_opts

    def newcommand(self, name: int, num_parameters: int, definition: str):
        pass

    def _find_command_definitions(self, path) -> NewCommandSubstitution:
        """
        Parse the document once independently to extract new commands.
        :param path:
        :return:
        """
        preprocessor = flachtex.Preprocessor(os.path.dirname(path))
        preprocessor.file_finder = self.file_finder
        doc = preprocessor.expand_file(path)
        cmds = find_new_commands(doc)
        ncs = NewCommandSubstitution()
        for cmd in cmds:
            ncs.new_command(cmd)
        return ncs

    def parse_source(
        self, path: str, project_root: typing.Optional[str] = None
    ) -> LatexSource:
        if project_root:
            self.file_finder.set_root(project_root)
        else:
            self.file_finder.set_root(os.path.dirname(path))
        preprocessor = flachtex.Preprocessor(os.path.dirname(path))
        preprocessor.file_finder = self.file_finder
        preprocessor.skip_rules.append(TodonotesRule())
        preprocessor.skip_rules.append(_IgnoreRule())
        preprocessor.substitution_rules.append(ChangesRule())
        preprocessor.substitution_rules.append(ChangesRule(True))
        preprocessor.substitution_rules.append(self._find_command_definitions(path))
        flat_source = preprocessor.expand_file(path)
        return LatexSource(
            flachtex.remove_comments(flat_source), preprocessor.structure
        )

    def parse(
        self, path: str, project_root: typing.Optional[str] = None
    ) -> LatexDocument:
        source = self.parse_source(path, project_root)
        return LatexDocument(
            source, DetexedText(str(source.flat_source), self._yalafi_opts)
        )
