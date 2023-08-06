from janis_core import (
    Array,
    File,
    ToolInput,
    ToolOutput,
    Filename,
    InputSelector,
    ToolArgument,
    Directory,
    String,
)

from .unixtool import UnixTool


class LocaliseFolder(UnixTool):
    def tool(self):
        return "LocaliseFolder"

    def friendly_name(self):
        return "LocaliseFolder"

    def base_command(self):
        return None

    def inputs(self):
        return [
            ToolInput(
                "dir",
                Directory,
                position=3,
            ),
        ]

    def outputs(self):
        return [ToolOutput("out", Directory, selector=InputSelector("dir"))]

    def arguments(self):
        return [
            ToolArgument("cp", position=1, shell_quote=False),
            ToolArgument("-r", position=2, shell_quote=False),
            ToolArgument(".", position=4, shell_quote=False),
        ]

    def bind_metadata(self):
        self.metadata.documentation = """localise folder"""
