import sys
import xml.sax
from typing import Iterable, Optional, Set, Union

"""Main module."""
'''plagirised from https://www.tutorialspoint.com/python3/python_xml_processing.htm'''


class Saxtract(xml.sax.ContentHandler):
    def __init__(self, *, tags: Optional[Iterable[str]], instream=sys.stdin, outstream=sys.stdout,
                 child_tag: Optional[str] = None, show_tags: bool = False, verbose: int = 0):
        self.tags: Union(Set[str], None) = set(tags)
        self.instream = instream
        self.outstream = outstream
        self.child_tag: str = child_tag
        self.show_tags: bool = show_tags
        self.verbose: int = verbose
        self.ran: bool = show_tags

        self.current_tag = ''
        self.current_content = ''
        if self.verbose:
            self._output(f'Tags: {",".join(tags)}')

        self._init_parser()

    def _init_parser(self) -> None:
        self.parser = xml.sax.make_parser()
        # turning off namepsaces
        self.parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        self.parser.setContentHandler(self)

        # Call when an element starts
    def startElement(self, tag: str, attributes: str) -> None:
        self.current_tag = tag

    # Call when an elements ends
    def endElement(self, tag: str) -> None:
        if self._show_tag(tag):
            self._output(f'{self.current_tag}: ')
        if self._show_content():
            self._output(f'{self.current_content},')
        if self._add_newline(tag):
            self._output('\n')

        self.current_tag = self.current_content = ''

    # Call when a character is read
    def characters(self, content: str) -> None:
        if self._relevant_data(self.tags, self.current_tag):
            self.current_content += content

    def _relevant_data(self, struct, data) -> bool:
        return True if data in struct or not struct else False

    def _show_tag(self, tag: str) -> bool:
        return True if all([tag, self.show_tags, self._relevant_data(self.tags, tag)]) else False

    def _show_content(self) -> bool:
        return True if self.current_content else False

    def _add_newline(self, tag: str) -> bool:
        return True if tag == self.child_tag else False

    def _output(self, content: str) -> None:
        if self.outstream:
            self.outstream.write(f'{content}')

    def start(self) -> None:
        if not self.ran:
            self.ran = True
            self.parser.parse(self.instream)
