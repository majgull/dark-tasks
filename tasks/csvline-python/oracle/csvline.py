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
    i, n = 0, len(line)
    while True:
        if i < n and line[i] == '"':
            i += 1
            buf = []
            while True:
                if i >= n:
                    raise ValueError("unterminated quote")
                ch = line[i]
                if ch == '"':
                    if i + 1 < n and line[i + 1] == '"':
                        buf.append('"')
                        i += 2
                        continue
                    i += 1
                    break
                buf.append(ch)
                i += 1
            fields.append("".join(buf))
            if i < n and line[i] != ",":
                raise ValueError(f"text after closing quote at {i}")
        else:
            j = line.find(",", i)
            end = n if j < 0 else j
            if '"' in line[i:end]:
                raise ValueError(f"quote inside unquoted field at {i}")
            fields.append(line[i:end])
            i = end
        if i >= n:
            return fields
        i += 1  # the comma
        if i == n:
            fields.append("")
            return fields
