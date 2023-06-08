from rope.base.project import Project
from rope.base.libutils import path_to_resource
from rope.refactor.extract import ExtractMethod
from rope.refactor.rename import Rename
from rope.refactor.inline import create_inline
from rope.contrib.codeassist import code_assist


def load_project(project_path: str = "."):
    return Project(project_path)


# Create a temporary project and resource for the Python file
project = Project(".")
python_file = "example.py"
resource = project.get_resource(python_file)

# Create an instance of Rename and perform the refactoring
rename = Rename(project, resource, resource.read().index("add_numbers"))
changes = rename.get_changes("sum_numbers")
project.do(changes)

# Save the changes to the file
with open(python_file, "w") as file:
    file.write(resource.read())

# Create an instance of Inline and perform the refactoring
inline = create_inline(project, resource, resource.read().index("sum_numbers"))
changes = inline.get_changes()
project.do(changes)

# Save the changes to the file
with open(python_file, "w") as file:
    file.write(resource.read())
