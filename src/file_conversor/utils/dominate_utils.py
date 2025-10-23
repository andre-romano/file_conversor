# src\file_conversor\utils\dominate_utils.py

from dominate import document as document_tag
from dominate import tags

from typing import cast


# create template tag
class template_tag(tags.html_tag):
    """Custom Dominate tag representing <template>."""
    tagname = "template"


def template(*args, **kwargs) -> template_tag:
    return cast(template_tag, template_tag(*args, **kwargs))


def document(*args, **kwargs) -> document_tag:
    return cast(document_tag, document_tag(*args, **kwargs))


def a(*args, **kwargs) -> tags.a:
    return cast(tags.a, tags.a(*args, **kwargs))


def abbr(*args, **kwargs) -> tags.abbr:
    return cast(tags.abbr, tags.abbr(*args, **kwargs))


def address(*args, **kwargs) -> tags.address:
    return cast(tags.address, tags.address(*args, **kwargs))


def area(*args, **kwargs) -> tags.area:
    return cast(tags.area, tags.area(*args, **kwargs))


def article(*args, **kwargs) -> tags.article:
    return cast(tags.article, tags.article(*args, **kwargs))


def aside(*args, **kwargs) -> tags.aside:
    return cast(tags.aside, tags.aside(*args, **kwargs))


def audio(*args, **kwargs) -> tags.audio:
    return cast(tags.audio, tags.audio(*args, **kwargs))


def b(*args, **kwargs) -> tags.b:
    return cast(tags.b, tags.b(*args, **kwargs))


def base(*args, **kwargs) -> tags.base:
    return cast(tags.base, tags.base(*args, **kwargs))


def bdi(*args, **kwargs) -> tags.bdi:
    return cast(tags.bdi, tags.bdi(*args, **kwargs))


def bdo(*args, **kwargs) -> tags.bdo:
    return cast(tags.bdo, tags.bdo(*args, **kwargs))


def blockquote(*args, **kwargs) -> tags.blockquote:
    return cast(tags.blockquote, tags.blockquote(*args, **kwargs))


def body(*args, **kwargs) -> tags.body:
    return cast(tags.body, tags.body(*args, **kwargs))


def br(*args, **kwargs) -> tags.br:
    return cast(tags.br, tags.br(*args, **kwargs))


def button(*args, **kwargs) -> tags.button:
    return cast(tags.button, tags.button(*args, **kwargs))


def canvas(*args, **kwargs) -> tags.canvas:
    return cast(tags.canvas, tags.canvas(*args, **kwargs))


def caption(*args, **kwargs) -> tags.caption:
    return cast(tags.caption, tags.caption(*args, **kwargs))


def cite(*args, **kwargs) -> tags.cite:
    return cast(tags.cite, tags.cite(*args, **kwargs))


def code(*args, **kwargs) -> tags.code:
    return cast(tags.code, tags.code(*args, **kwargs))


def col(*args, **kwargs) -> tags.col:
    return cast(tags.col, tags.col(*args, **kwargs))


def colgroup(*args, **kwargs) -> tags.colgroup:
    return cast(tags.colgroup, tags.colgroup(*args, **kwargs))


def command(*args, **kwargs) -> tags.command:
    return cast(tags.command, tags.command(*args, **kwargs))


def comment(*args, **kwargs) -> tags.comment:
    return cast(tags.comment, tags.comment(*args, **kwargs))


def datalist(*args, **kwargs) -> tags.datalist:
    return cast(tags.datalist, tags.datalist(*args, **kwargs))


def dd(*args, **kwargs) -> tags.dd:
    return cast(tags.dd, tags.dd(*args, **kwargs))


def details(*args, **kwargs) -> tags.details:
    return cast(tags.details, tags.details(*args, **kwargs))


def dfn(*args, **kwargs) -> tags.dfn:
    return cast(tags.dfn, tags.dfn(*args, **kwargs))


def div(*args, **kwargs) -> tags.div:
    return cast(tags.div, tags.div(*args, **kwargs))


def dl(*args, **kwargs) -> tags.dl:
    return cast(tags.dl, tags.dl(*args, **kwargs))


def dom1core(*args, **kwargs) -> tags.dom1core:
    return cast(tags.dom1core, tags.dom1core(*args, **kwargs))


def dom_tag(*args, **kwargs) -> tags.dom_tag:
    return cast(tags.dom_tag, tags.dom_tag(*args, **kwargs))


def dt(*args, **kwargs) -> tags.dt:
    return cast(tags.dt, tags.dt(*args, **kwargs))


def em(*args, **kwargs) -> tags.em:
    return cast(tags.em, tags.em(*args, **kwargs))


def embed(*args, **kwargs) -> tags.embed:
    return cast(tags.embed, tags.embed(*args, **kwargs))


def fieldset(*args, **kwargs) -> tags.fieldset:
    return cast(tags.fieldset, tags.fieldset(*args, **kwargs))


def figcaption(*args, **kwargs) -> tags.figcaption:
    return cast(tags.figcaption, tags.figcaption(*args, **kwargs))


def figure(*args, **kwargs) -> tags.figure:
    return cast(tags.figure, tags.figure(*args, **kwargs))


def footer(*args, **kwargs) -> tags.footer:
    return cast(tags.footer, tags.footer(*args, **kwargs))


def font(*args, **kwargs) -> tags.font:
    return cast(tags.font, tags.font(*args, **kwargs))


def form(*args, **kwargs) -> tags.form:
    return cast(tags.form, tags.form(*args, **kwargs))


def h1(*args, **kwargs) -> tags.h1:
    return cast(tags.h1, tags.h1(*args, **kwargs))


def h2(*args, **kwargs) -> tags.h2:
    return cast(tags.h2, tags.h2(*args, **kwargs))


def h3(*args, **kwargs) -> tags.h3:
    return cast(tags.h3, tags.h3(*args, **kwargs))


def h4(*args, **kwargs) -> tags.h4:
    return cast(tags.h4, tags.h4(*args, **kwargs))


def h5(*args, **kwargs) -> tags.h5:
    return cast(tags.h5, tags.h5(*args, **kwargs))


def h6(*args, **kwargs) -> tags.h6:
    return cast(tags.h6, tags.h6(*args, **kwargs))


def head(*args, **kwargs) -> tags.head:
    return cast(tags.head, tags.head(*args, **kwargs))


def header(*args, **kwargs) -> tags.header:
    return cast(tags.header, tags.header(*args, **kwargs))


def hgroup(*args, **kwargs) -> tags.hgroup:
    return cast(tags.hgroup, tags.hgroup(*args, **kwargs))


def hr(*args, **kwargs) -> tags.hr:
    return cast(tags.hr, tags.hr(*args, **kwargs))


def html(*args, **kwargs) -> tags.html:
    return cast(tags.html, tags.html(*args, **kwargs))


def html_tag(*args, **kwargs) -> tags.html_tag:
    return cast(tags.html_tag, tags.html_tag(*args, **kwargs))


def i(*args, **kwargs) -> tags.i:
    return cast(tags.i, tags.i(*args, **kwargs))


def iframe(*args, **kwargs) -> tags.iframe:
    return cast(tags.iframe, tags.iframe(*args, **kwargs))


def img(*args, **kwargs) -> tags.img:
    return cast(tags.img, tags.img(*args, **kwargs))


def input_(*args, **kwargs) -> tags.input_:
    return cast(tags.input_, tags.input_(*args, **kwargs))


def ins(*args, **kwargs) -> tags.ins:
    return cast(tags.ins, tags.ins(*args, **kwargs))


def kbd(*args, **kwargs) -> tags.kbd:
    return cast(tags.kbd, tags.kbd(*args, **kwargs))


def keygen(*args, **kwargs) -> tags.keygen:
    return cast(tags.keygen, tags.keygen(*args, **kwargs))


def label(*args, **kwargs) -> tags.label:
    return cast(tags.label, tags.label(*args, **kwargs))


def legend(*args, **kwargs) -> tags.legend:
    return cast(tags.legend, tags.legend(*args, **kwargs))


def li(*args, **kwargs) -> tags.li:
    return cast(tags.li, tags.li(*args, **kwargs))


def link(*args, **kwargs) -> tags.link:
    return cast(tags.link, tags.link(*args, **kwargs))


def main(*args, **kwargs) -> tags.main:
    return cast(tags.main, tags.main(*args, **kwargs))


def map_(*args, **kwargs) -> tags.map_:
    return cast(tags.map_, tags.map_(*args, **kwargs))


def meter(*args, **kwargs) -> tags.meter:
    return cast(tags.meter, tags.meter(*args, **kwargs))


def menu(*args, **kwargs) -> tags.menu:
    return cast(tags.menu, tags.menu(*args, **kwargs))


def mark(*args, **kwargs) -> tags.mark:
    return cast(tags.mark, tags.mark(*args, **kwargs))


def meta(*args, **kwargs) -> tags.meta:
    return cast(tags.meta, tags.meta(*args, **kwargs))


def nav(*args, **kwargs) -> tags.nav:
    return cast(tags.nav, tags.nav(*args, **kwargs))


def noscript(*args, **kwargs) -> tags.noscript:
    return cast(tags.noscript, tags.noscript(*args, **kwargs))


def object_(*args, **kwargs) -> tags.object_:
    return cast(tags.object_, tags.object_(*args, **kwargs))


def ol(*args, **kwargs) -> tags.ol:
    return cast(tags.ol, tags.ol(*args, **kwargs))


def optgroup(*args, **kwargs) -> tags.optgroup:
    return cast(tags.optgroup, tags.optgroup(*args, **kwargs))


def option(*args, **kwargs) -> tags.option:
    return cast(tags.option, tags.option(*args, **kwargs))


def output(*args, **kwargs) -> tags.output:
    return cast(tags.output, tags.output(*args, **kwargs))


def p(*args, **kwargs) -> tags.p:
    return cast(tags.p, tags.p(*args, **kwargs))


def param(*args, **kwargs) -> tags.param:
    return cast(tags.param, tags.param(*args, **kwargs))


def pre(*args, **kwargs) -> tags.pre:
    return cast(tags.pre, tags.pre(*args, **kwargs))


def progress(*args, **kwargs) -> tags.progress:
    return cast(tags.progress, tags.progress(*args, **kwargs))


def q(*args, **kwargs) -> tags.q:
    return cast(tags.q, tags.q(*args, **kwargs))


def rp(*args, **kwargs) -> tags.rp:
    return cast(tags.rp, tags.rp(*args, **kwargs))


def rt(*args, **kwargs) -> tags.rt:
    return cast(tags.rt, tags.rt(*args, **kwargs))


def ruby(*args, **kwargs) -> tags.ruby:
    return cast(tags.ruby, tags.ruby(*args, **kwargs))


def s(*args, **kwargs) -> tags.s:
    return cast(tags.s, tags.s(*args, **kwargs))


def samp(*args, **kwargs) -> tags.samp:
    return cast(tags.samp, tags.samp(*args, **kwargs))


def script(*args, **kwargs) -> tags.script:
    return cast(tags.script, tags.script(*args, **kwargs))


def section(*args, **kwargs) -> tags.section:
    return cast(tags.section, tags.section(*args, **kwargs))


def select(*args, **kwargs) -> tags.select:
    return cast(tags.select, tags.select(*args, **kwargs))


def small(*args, **kwargs) -> tags.small:
    return cast(tags.small, tags.small(*args, **kwargs))


def source(*args, **kwargs) -> tags.source:
    return cast(tags.source, tags.source(*args, **kwargs))


def span(*args, **kwargs) -> tags.span:
    return cast(tags.span, tags.span(*args, **kwargs))


def strong(*args, **kwargs) -> tags.strong:
    return cast(tags.strong, tags.strong(*args, **kwargs))


def style(*args, **kwargs) -> tags.style:
    return cast(tags.style, tags.style(*args, **kwargs))


def sub(*args, **kwargs) -> tags.sub:
    return cast(tags.sub, tags.sub(*args, **kwargs))


def summary(*args, **kwargs) -> tags.summary:
    return cast(tags.summary, tags.summary(*args, **kwargs))


def sup(*args, **kwargs) -> tags.sup:
    return cast(tags.sup, tags.sup(*args, **kwargs))


def table(*args, **kwargs) -> tags.table:
    return cast(tags.table, tags.table(*args, **kwargs))


def tbody(*args, **kwargs) -> tags.tbody:
    return cast(tags.tbody, tags.tbody(*args, **kwargs))


def td(*args, **kwargs) -> tags.td:
    return cast(tags.td, tags.td(*args, **kwargs))


def textarea(*args, **kwargs) -> tags.textarea:
    return cast(tags.textarea, tags.textarea(*args, **kwargs))


def tfoot(*args, **kwargs) -> tags.tfoot:
    return cast(tags.tfoot, tags.tfoot(*args, **kwargs))


def th(*args, **kwargs) -> tags.th:
    return cast(tags.th, tags.th(*args, **kwargs))


def thead(*args, **kwargs) -> tags.thead:
    return cast(tags.thead, tags.thead(*args, **kwargs))


def time_(*args, **kwargs) -> tags.time_:
    return cast(tags.time_, tags.time_(*args, **kwargs))


def title(*args, **kwargs) -> tags.title:
    return cast(tags.title, tags.title(*args, **kwargs))


def track(*args, **kwargs) -> tags.track:
    return cast(tags.track, tags.track(*args, **kwargs))


def tr(*args, **kwargs) -> tags.tr:
    return cast(tags.tr, tags.tr(*args, **kwargs))


def u(*args, **kwargs) -> tags.u:
    return cast(tags.u, tags.u(*args, **kwargs))


def ul(*args, **kwargs) -> tags.ul:
    return cast(tags.ul, tags.ul(*args, **kwargs))


def video(*args, **kwargs) -> tags.video:
    return cast(tags.video, tags.video(*args, **kwargs))


def wbr(*args, **kwargs) -> tags.wbr:
    return cast(tags.wbr, tags.wbr(*args, **kwargs))


def var(*args, **kwargs) -> tags.var:
    return cast(tags.var, tags.var(*args, **kwargs))


__all__ = [
    'tags',
    'document',
    'template',
    'a',
    'abbr',
    'address',
    'area',
    'article',
    'aside',
    'audio',
    'b',
    'base',
    'bdi',
    'bdo',
    'blockquote',
    'body',
    'br',
    'button',
    'canvas',
    'caption',
    'cite',
    'code',
    'col',
    'colgroup',
    'command',
    'comment',
    'datalist',
    'dd',
    'details',
    'dfn',
    'div',
    'dl',
    'dom1core',
    'dom_tag',
    'dt',
    'em',
    'embed',
    'fieldset',
    'figcaption',
    'figure',
    'footer',
    'font',
    'form',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'head',
    'header',
    'hgroup',
    'hr',
    'html',
    'html_tag',
    'i',
    'iframe',
    'img',
    'input_',
    'ins',
    'kbd',
    'keygen',
    'label',
    'legend',
    'li',
    'link',
    'main',
    'map_',
    'meter',
    'menu',
    'mark',
    'meta',
    'nav',
    'noscript',
    'object_',
    'ol',
    'optgroup',
    'option',
    'output',
    'p',
    'param',
    'pre',
    'progress',
    'q',
    'rp',
    'rt',
    'ruby',
    's',
    'samp',
    'script',
    'section',
    'select',
    'small',
    'source',
    'span',
    'strong',
    'style',
    'sub',
    'summary',
    'sup',
    'table',
    'tbody',
    'td',
    'textarea',
    'tfoot',
    'th',
    'thead',
    'time_',
    'title',
    'track',
    'tr',
    'u',
    'ul',
    'video',
    'wbr',
    'var',
    'video',
    'wbr',
    'var'
]
