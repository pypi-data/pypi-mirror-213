import operator
from typing import Optional, List, Callable, Dict

from janis_core import File
from janis_core.tool.test_classes import TTestExpectedOutput, TTestPreprocessor


class ZipFile(File):
    def __init__(self, optional=False, extension=".zip"):
        super().__init__(optional, extension=extension)

    @staticmethod
    def name():
        return "Zip"

    def doc(self):
        return "A zip archive, ending with .zip"

    @classmethod
    def basic_test(
        cls,
        tag: str,
        min_size: int,
        md5: Optional[str] = None,
    ) -> List[TTestExpectedOutput]:
        outcome = [
            TTestExpectedOutput(
                tag=tag,
                preprocessor=TTestPreprocessor.FileSize,
                operator=operator.ge,
                expected_value=min_size,
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
        return outcome
