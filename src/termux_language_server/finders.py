r"""Finders
===========
"""
from copy import deepcopy
from dataclasses import dataclass

from jinja2 import Template
from lsprotocol.types import (
    CompletionItemKind,
    DiagnosticSeverity,
    DocumentLink,
    Position,
    Range,
    TextEdit,
)
from tree_sitter import Tree

from . import CSV, FILETYPE
from .schema import BashTrie
from .tree_sitter_lsp import UNI, Finder
from .tree_sitter_lsp.finders import (
    ErrorFinder,
    MissingFinder,
    SchemaFinder,
    UnFixedOrderFinder,
)
from .utils import get_schema

SCHEMAS = {}
for filetype in FILETYPE.__args__:  # type: ignore
    SCHEMAS[filetype] = get_schema(filetype)


@dataclass(init=False)
class BashFinder(SchemaFinder):
    r"""Bashfinder."""

    def __init__(self, filetype: FILETYPE) -> None:
        r"""Init.

        :param filetype:
        :type filetype: FILETYPE
        :rtype: None
        """
        self.validator = self.schema2validator(SCHEMAS[filetype])
        self.cls = BashTrie


@dataclass(init=False)
class UnsortedKeywordFinder(UnFixedOrderFinder):
    r"""Unsortedkeywordfinder."""

    def __init__(
        self,
        filetype: FILETYPE,
        message: str = "{{uni.get_text()}}: is unsorted due to {{_uni}}",
        severity: DiagnosticSeverity = DiagnosticSeverity.Warning,
    ) -> None:
        r"""Init.

        :param filetype:
        :type filetype: FILETYPE
        :param message:
        :type message: str
        :param severity:
        :type severity: DiagnosticSeverity
        :rtype: None
        """
        super().__init__(
            list(SCHEMAS[filetype]["properties"]), message, severity
        )
        self.keywords = UnsortedKeywordFinder.get_keywords(filetype)

    @staticmethod
    def get_keywords(filetype) -> dict[str, CompletionItemKind]:
        r"""Get keywords.

        :param filetype:
        :rtype: dict[str, CompletionItemKind]
        """
        return {
            k: (
                CompletionItemKind.Function
                if v.get("const") == 0
                else CompletionItemKind.Variable
            )
            for k, v in SCHEMAS[filetype]["properties"].items()
        }

    @staticmethod
    def is_correct_declaration(uni: UNI, _type: CompletionItemKind) -> bool:
        r"""Is correct declaration.

        :param uni:
        :type uni: UNI
        :param _type:
        :type _type: CompletionItemKind
        :rtype: bool
        """
        parent = uni.node.parent
        if parent is None:
            return False
        return (
            _type == CompletionItemKind.Variable
            and uni.node.type == "variable_name"
            and parent.type == "variable_assignment"
            and parent.children[-1].type != "array"
            or _type == CompletionItemKind.Field
            and uni.node.type == "variable_name"
            and parent.type == "variable_assignment"
            and parent.children[-1].type == "array"
            or _type == CompletionItemKind.Function
            and uni.node.type == "word"
            and parent.type == "function_definition"
        )

    @staticmethod
    def is_correct_reference(uni: UNI, _type: CompletionItemKind) -> bool:
        r"""Is correct reference.

        :param uni:
        :type uni: UNI
        :param _type:
        :type _type: CompletionItemKind
        :rtype: bool
        """
        parent = uni.node.parent
        if parent is None:
            return False
        return (
            _type in {CompletionItemKind.Variable, CompletionItemKind.Field}
            and uni.node.type == "variable_name"
            and parent.type in {"expansion", "simple_expansion"}
            or _type == CompletionItemKind.Function
            and uni.node.type == "word"
            and parent.type == "command_name"
        )

    @staticmethod
    def is_correct(uni: UNI, _type: CompletionItemKind) -> bool:
        r"""Is correct.

        :param uni:
        :type uni: UNI
        :param _type:
        :type _type: CompletionItemKind
        :rtype: bool
        """
        return UnsortedKeywordFinder.is_correct_declaration(
            uni, _type
        ) or UnsortedKeywordFinder.is_correct_reference(uni, _type)

    def filter(self, uni: UNI) -> bool:
        r"""Filter.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        text = uni.get_text()
        return (
            text in self.order
            and text in self.keywords
            and UnsortedKeywordFinder.is_correct_declaration(
                uni, self.keywords[text]
            )
        )

    def get_text_edits(self, uri: str, tree: Tree) -> list[TextEdit]:
        r"""Get text edits. Only return two to avoid `Overlapping edit`

        :param self:
        :param uri:
        :type uri: str
        :param tree:
        :type tree: Tree
        :rtype: list[TextEdit]
        """
        self.find_all(uri, tree)
        for uni, _uni in self.uni_pairs:
            parent = uni.node.parent
            _parent = _uni.node.parent
            if parent is None or _parent is None:
                return []
            # swap 2 unis
            return [
                TextEdit(UNI.node2range(parent), UNI.node2text(_parent)),
                TextEdit(UNI.node2range(_parent), UNI.node2text(parent)),
            ]
        return []


@dataclass(init=False)
class UnsortedCSVFinder(Finder):
    r"""Unsorted comma separated value finder."""

    def __init__(
        self,
        filetype: FILETYPE,
        message: str = "{{uni.get_text()}}: unsorted",
        severity: DiagnosticSeverity = DiagnosticSeverity.Warning,
    ) -> None:
        r"""Init.

        :param filetype:
        :type filetype: FILETYPE
        :param message:
        :type message: str
        :param severity:
        :type severity: DiagnosticSeverity
        :rtype: None
        """
        super().__init__(message, severity)
        self.csvs = self.get_csvs(filetype)

    @staticmethod
    def get_csvs(filetype: FILETYPE) -> set[str]:
        r"""Get csvs.

        :param filetype:
        :type filetype: FILETYPE
        :rtype: set[str]
        """
        return set(
            k
            for k, v in SCHEMAS[filetype]["properties"].items()
            if v.get("pattern") == CSV
        )

    def __call__(self, uni: UNI) -> bool:
        r"""Call.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        return self.is_csv(uni) and self.sort(uni.get_text()) != uni.get_text()

    def is_csv(self, uni: UNI) -> bool:
        r"""Is csv.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        parent = uni.node.parent
        if parent is None:
            return False
        return (
            parent.type == "variable_assignment"
            and uni.node == parent.children[-1]
            and (uni.node.type == "word" or uni.node.type == "string")
            and UNI.node2text(parent.children[0]) in self.csvs
        )

    @staticmethod
    def sort(text: str) -> str:
        r"""Sort.

        :param text:
        :type text: str
        :rtype: str
        """
        return (
            '"'
            + ", ".join(
                sorted(word.strip() for word in text.strip('"').split(","))
            )
            + '"'
        )

    def get_text_edits(self, uri: str, tree: Tree) -> list[TextEdit]:
        r"""Get text edits. Only return two to avoid `Overlapping edit`

        :param self:
        :param uri:
        :type uri: str
        :param tree:
        :type tree: Tree
        :rtype: list[TextEdit]
        """
        text_edits = [
            TextEdit(uni.get_range(), self.sort(uni.get_text()))
            for uni in self.find_all(uri, tree)
        ]
        return text_edits


@dataclass()
class CSVFinder(UnsortedCSVFinder):
    r"""Comma separated value finder."""

    def __post_init__(self) -> None:
        r"""Post init.

        :rtype: None
        """
        self.csvs -= {"TERMUX_PKG_BLACKLISTED_ARCHES"}

    def __call__(self, uni: UNI) -> bool:
        r"""Call.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        return self.is_csv(uni)

    def get_document_links(
        self, uri: str, tree: Tree, template: str
    ) -> list[DocumentLink]:
        r"""Get document links.

        :param uri:
        :type uri: str
        :param tree:
        :type tree: Tree
        :param template:
        :type template: str
        :rtype: list[DocumentLink]
        """
        links = []
        for uni in self.find_all(uri, tree):
            start = list(uni.node.start_point)
            text = uni.get_text()
            if text.startswith('"'):
                text = text.strip('"')
                start[1] += 1
            end = deepcopy(start)
            for name in text.split(","):
                if name.startswith(" "):
                    name = name.lstrip(" ")
                    start[1] += 1
                    end[1] += 1
                end[1] += len(name)
                links += [
                    DocumentLink(
                        Range(Position(*start), Position(*end)),
                        Template(template).render(name=name),
                    )
                ]
                start[1] += len(name) + 1
        return links


DIAGNOSTICS_FINDER_CLASSES = [
    ErrorFinder,
    MissingFinder,
    BashFinder,
    UnsortedKeywordFinder,
    UnsortedCSVFinder,
]
FORMAT_FINDER_CLASSES = [UnsortedKeywordFinder, UnsortedCSVFinder]
