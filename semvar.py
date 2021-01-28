import semantic_version
import sys

version = "1.0.0"
v = semantic_version.Version(f"{version}+build.{sys.argv[1]}")

print(f"Major: {v.major}")
print(f"Minor: {v.minor}")
print(f"Patch: {v.patch}")
print(f"Build: {v.build}")

print(f"Version: {v}")

with open("version.txt", 'w') as f:
    f.write(f"{str(v)}\n")
    f.write(f"{version}.{sys.argv[1]}")
