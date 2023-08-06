import operator
from typing import Optional, List

from janis_core import File
from janis_core.tool.test_classes import TTestExpectedOutput, TTestPreprocessor


class TextFile(File):
    def __init__(self, optional=False, extension=".txt"):
        super().__init__(optional, extension=extension)

    @staticmethod
    def name():
        return "TextFile"

    def doc(self):
        return "A textfile, ending with .txt"

    @classmethod
    def basic_test(
        cls,
        tag: str,
        min_size: int,
        min_required_content: Optional[str] = None,
        line_count: Optional[int] = None,
        md5: Optional[str] = None,
        expected_file_path: Optional[str] = None,
    ) -> List[TTestExpectedOutput]:
        outcome = [
            TTestExpectedOutput(
                tag=tag,
                preprocessor=TTestPreprocessor.FileSize,
                operator=operator.ge,
                expected_value=min_size,
            ),
        ]

        if min_required_content is not None:
            outcome += [
                TTestExpectedOutput(
                    tag=tag,
                    preprocessor=TTestPreprocessor.FileContent,
                    operator=operator.contains,
                    expected_value=min_required_content,
                ),
            ]

        if line_count is not None:
            outcome += [
                TTestExpectedOutput(
                    tag=tag,
                    preprocessor=TTestPreprocessor.LineCount,
                    operator=operator.eq,
                    expected_value=line_count,
                ),
            ]

        if md5 is not None:
            outcome += [
                TTestExpectedOutput(
                    tag=tag,
                    preprocessor=TTestPreprocessor.FileMd5,
                    operator=operator.eq,
                    expected_value=md5,
                ),
            ]

        if expected_file_path is not None:
            outcome += [
                TTestExpectedOutput(
                    tag=tag,
                    preprocessor=TTestPreprocessor.FileContent,
                    operator=operator.eq,
                    expected_file=expected_file_path,
                ),
            ]

        return outcome
