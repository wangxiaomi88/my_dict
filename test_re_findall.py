import re

line="affronted        [ affront: ] a deliberate insult"

tup = re.findall(r"(\w+)\s+(.*)",line)[0]

print(tup)
