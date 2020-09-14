import semantic_version
import sys

v = semantic_version.Version(f"0.1.0+build.{sys.argv[1]}")

print(f"Major: {v.major}")
print(f"Minor: {v.minor}")
print(f"Patch: {v.patch}")
print(f"Build: {v.build}")

print(f"Version: {v}")

with open("version.txt", 'w') as f:
    f.write(str(v))
