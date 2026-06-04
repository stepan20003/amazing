import sys


if not sys.prefix == sys.base_prefix:
    print("YOU ARE NOT IN")
else:
    print("YOU ARE IN")
