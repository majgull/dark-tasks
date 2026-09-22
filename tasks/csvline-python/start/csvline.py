"""split_line(line) -> list[str]: the fields of one CSV record.

Fields are separated by commas. A field is either unquoted (taken as
is, spaces included, may be empty) or quoted: it starts with a double
quote, ends with a double quote, and inside it a comma is literal and
a doubled double quote "" stands for one double quote. The quotes
themselves are not part of the value. An empty line is one empty field
([""]); "a,b," is three fields ["a", "b", ""]; '"x,y",z' is ["x,y", "z"];
'"a ""b"" c",x' is ['a "b" c', "x"].

A quoted field that never closes, or a quote character appearing inside
an unquoted field or after a closing quote before the next comma
(so 'a"b' and '"a"b'), raises ValueError. Never use the csv module.
"""


def split_line(line):
    fields = []
    field = []
    quoted = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '"':
            quoted = not quoted
        elif ch == "," and not quoted:
            fields.append("".join(field))
            field = []
        else:
            field.append(ch)
        i += 1
    if quoted:
        raise ValueError("unterminated quote")
    if field:
        fields.append("".join(field))
    return fields
