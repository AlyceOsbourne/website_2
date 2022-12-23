import re

from markdown import markdown
from markupsafe import Markup
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name


def ext(app):
    # filter to render text as markdown, with syntax highlighting.
    # add css for the highlighting to the highlighted.css file.
    @app.template_filter('markdown')
    def highlight_filter(s):
        pattern = re.compile(r'```(\w+)?\s*([\s\S]+?)\s*```')

        def repl(match):
            lang = match.group(1)
            code = match.group(2)
            if lang:
                return highlight(code, get_lexer_by_name(lang), HtmlFormatter())
            else:
                return highlight(code, get_lexer_by_name('text'), HtmlFormatter())

        formatted = pattern.sub(repl, s)
        return Markup(markdown(formatted))
