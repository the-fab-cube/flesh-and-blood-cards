from markdown import Markdown
from io import StringIO

# Based off StackOverflow comment here: https://stackoverflow.com/a/54923798

_md = None

def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()

def unmark(text):
    if _md == None:
        Markdown.output_formats["plain"] = unmark_element
        __md = Markdown(output_format="plain")
        __md.stripTopLevelTags = False
    return __md.convert(text)