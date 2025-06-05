import re

def escape_markdown(text):
    # Список символов, которые нужно экранировать в Markdown
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text)