import os
from typing import Optional

from rope.base.change import ChangeContents, ChangeSet, MoveResource
from rope.base.project import Project
from rope.base.libutils import path_to_resource
from rope.base.resources import File, Folder
from rope.refactor.extract import ExtractMethod
from rope.refactor.rename import Rename
from rope.refactor.inline import create_inline
from rope.contrib.codeassist import code_assist



class RopeRefactorer:
    def __init__(self, project: Project, resource: File | Folder) -> None:
        self.project: Project = project
        self.resource: File | Folder = resource

        self.changes: Optional[ChangeSet] = None

    def __del__(self) -> None:
        self.project.close()

    @classmethod
    def create_with_paths(
        cls, resource_path: str, project_path: Optional[str] = None
    ) -> "RopeRefactorer":
        if project_path is None:
            path = "."

        project = Project(project_path)
        resource: File | Folder = project.get_resource(resource_path)

        return cls(project, resource)

    def do(self, undo: bool = False, redo: bool = False, preview: bool = False) -> None:
        if self.changes is None:
            raise ValueError("No changes to perform")

        if preview:
            print(changes.get_description())

        elif undo:
            self.project.history.undo()

        elif redo:
            self.project.history.redo()

        else:
            self.project.do(self.changes)

    def rename(self, )

    # def perform_change()


# Create a temporary project and resource for the Python file
resource = get_file("rope_scratch.py")

# Create an instance of Rename and perform the refactoring
rename = Rename(project, resource, resource.read().index("add_numbers"))
changes = rename.get_changes("sum_numbers")
project.do(changes)

# Save the changes to the file
with open(resource, "w") as file:
    file.write(resource.read())

# Create an instance of Inline and perform the refactoring
inline = create_inline(project, resource, resource.read().index("sum_numbers"))
changes = inline.get_changes()
project.do(changes)

# Save the changes to the file
with open(python_file, "w") as file:
    file.write(resource.read())
