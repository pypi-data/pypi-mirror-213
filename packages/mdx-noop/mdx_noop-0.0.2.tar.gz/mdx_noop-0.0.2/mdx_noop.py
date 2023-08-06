from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
from markdown.util import AtomicString
import xml.etree.ElementTree as etree


class IgnoreLatexInlineProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element('latex')
        el.text = AtomicString(m.group(1))
        return el, m.start(0), m.end(0)


class IgnoreLatexExtension(Extension):
    def extendMarkdown(self, md):
        LATEX_PATTERN = r'(\$\$.+?\$\$|\$.+?\$)'  # like --del--
        md.inlinePatterns.register(
            IgnoreLatexInlineProcessor(LATEX_PATTERN, md), 'latex', 10000
        )


def makeExtension(**kwargs):  # pragma: no cover
    return IgnoreLatexExtension(**kwargs)
