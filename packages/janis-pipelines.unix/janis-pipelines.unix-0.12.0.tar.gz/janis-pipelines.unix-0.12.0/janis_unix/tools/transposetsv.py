from janis_core import (
    Array,
    File,
    ToolInput,
    ToolOutput,
    Filename,
    InputSelector,
    ToolArgument,
)
from janis_unix.data_types import Tsv
from .unixtool import UnixTool


class TransposeTsv(UnixTool):
    def tool(self):
        return "TransposeTsv"

    def friendly_name(self):
        return "TransposeTsv"

    def base_command(self):
        return None

    def inputs(self):
        return [
            ToolInput("inp_tsv", Tsv, position=2),
            ToolInput(
                "outputFilename",
                Filename(
                    InputSelector("inp_tsv", remove_file_extension=True),
                    suffix=".transposed",
                    extension=".tsv",
                ),
                position=4,
            ),
        ]

    def outputs(self):
        return [ToolOutput("out", Tsv, selector=InputSelector("outputFilename"))]

    def arguments(self):
        return [
            ToolArgument(
                'echo \'BEGIN { FS=OFS="\t" }\n\
{ \n\
    for (rowNr=1;rowNr<=NF;rowNr++) {\n\
        cell[rowNr,NR] = $rowNr\n\
    }\n\
    maxRows = (NF > maxRows ? NF : maxRows)\n\
    maxCols = NR\n\
}\n\
END {\n\
    for (rowNr=1;rowNr<=maxRows;rowNr++) {\n\
        for (colNr=1;colNr<=maxCols;colNr++) {\n\
            printf "%s%s", cell[rowNr,colNr], (colNr < maxCols ? OFS : ORS)\n\
        }\n\
    }\n\
}\' > tst.awk;',
                position=0,
                shell_quote=False,
            ),
            ToolArgument("awk -f tst.awk ", position=1, shell_quote=False),
            ToolArgument(">", position=3, shell_quote=False),
        ]

    def bind_metadata(self):
        self.metadata.documentation = """transpose tsv file"""
