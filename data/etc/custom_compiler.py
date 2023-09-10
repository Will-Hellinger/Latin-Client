import pkg_resources
import ast
import os
import sys
import time


def get_imports(script_content: str) -> list[str]:
    imports = []
    try:
        tree = ast.parse(script_content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)
            elif isinstance(node, ast.ImportFrom):
                for n in node.names:
                    imports.append(f"{node.module}.{n.name}")
    except Exception as e:
        print(f"Error parsing script: {e}")
    return imports


if os.name == 'nt':
    seperator = ';'
else:
    seperator = ':'

if len(sys.argv) <2:
    print('Please enter a file to compile')
    exit()


installed_packages = [pkg.key for pkg in pkg_resources.working_set]
needed_packages = []
exclude_packages = ''
commands = ''

start_time = time.time()

file_list = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            for package in get_imports(open(file).read()):
                if package not in needed_packages:
                    needed_packages.append(package)

for package in installed_packages:
    if package not in needed_packages:
        exclude_packages += f' --exclude-module {package}'

for i in range(2, len(sys.argv)):
    commands += f' {sys.argv[i]}'

print(f'Time taken to prep for compilation: {time.time()-start_time}')
print(f'pyinstaller {str(sys.argv[1])} --add-data=".{seperator}." {str(exclude_packages)}')