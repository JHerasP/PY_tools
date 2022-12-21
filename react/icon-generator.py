from io import TextIOWrapper
import os

# Generates a react component with a selector based on the files inside a folder


## Utils ##


def write_imports(relative_path: str, files: list[str], new_file: TextIOWrapper):
    for file in files:
        file_no_extension = os.path.splitext(file)[0]
        new_file.write(
            f'import {{ ReactComponent as {file_no_extension} }} from "{relative_path}/{file}\";')


def write_list_values(files: list[str], list_name: str, new_file: TextIOWrapper):
    new_file.write(f'export const {list_name} = Object.freeze([')

    for file in files:
        file_no_extension = os.path.splitext(file)[0]
        new_file.write(f"\'{file_no_extension}\',")

    new_file.write("] as const);")


def write_type_utils(list_name: str, type_name: str, type_single_value_name: str, new_file: TextIOWrapper):
    new_file.write(f'export type {type_name} = typeof {list_name};')
    new_file.write(
        f"export type {type_single_value_name} = typeof {list_name}[number];")


def write_component_selector(files: list[str], new_file: TextIOWrapper):
    new_file.write("switch (iconName) {")

    for file in files:
        file_no_extension = os.path.splitext(file)[0]
        new_file.write(f"case \'{file_no_extension}\':")
        new_file.write(f"return <{file_no_extension}/>")
        new_file.write(";")

    new_file.write("default:")
    new_file.write("return null;")
    new_file.write("}")


## /Utils ##


# Folder where the files are located
PATH_READ = "G:/Projects/the-joker/client/src/public/icons"
# Folder where the component will be created
PATH_WRITE = "G:/Projects/the-joker/client/src/components/inputs/icons"
# Relative path to import the files
RELATIVE_PATH = os.path.relpath(PATH_READ, PATH_WRITE).replace(
    "\\", '/')

FILES = os.listdir(PATH_READ)  # List of files
FILE_NAME = "Icons.tsx"
LIST_NAME = "ICON_LIST"  # Export with the values of the generated list
TYPE_LIST_NAME = "TIconList"  # Export with the type of the {listName}
TYPE_ITEM_LIST = "TIcon"  # Export with string values of the list
COMPONENT_NAME = "Icons"  # React component name

newFile = open(PATH_WRITE + "/" + FILE_NAME, 'w')


write_imports(RELATIVE_PATH, FILES, newFile)

write_list_values(FILES, LIST_NAME, newFile)

write_type_utils(LIST_NAME, TYPE_LIST_NAME, TYPE_ITEM_LIST, newFile)

# Declaration of the react component
newFile.write(
    f"export default function {COMPONENT_NAME}({{ iconName }}: {{ iconName: {TYPE_ITEM_LIST} }}) " + "{")

write_component_selector(FILES, newFile)

# End of the react component
newFile.write("}")
