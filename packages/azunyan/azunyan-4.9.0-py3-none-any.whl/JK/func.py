# clean text for telegram MARKDOWN_V2
def md2(text):
    for symbol in ['\\', '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']:
        if symbol in text:
            text = text.replace(symbol, RF'\{symbol}')
    return text
