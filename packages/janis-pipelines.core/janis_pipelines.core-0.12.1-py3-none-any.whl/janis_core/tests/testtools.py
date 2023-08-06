from typing import Dict, List, Any, Optional, Union

from janis_core.operators.logical import If, IsDefined
from janis_core.types import Filename

from janis_core import (
    ToolOutput,
    ToolInput,
    TInput,
    TOutput,
    String,
    Int,
    CommandTool,
    PythonTool,
    Stdout,
    InputSelector,
    Array,
    File,
    WildcardSelector,
    StringFormatter,
    ToolArgument,
    InputDocumentation,
    InputQualityType,
    Workflow,
    FirstOperator,
    ForEachSelector,
)


class EchoTestTool(CommandTool):
    def tool(self) -> str:
        return "EchoTestTool"

    def base_command(self) -> Optional[Union[str, List[str]]]:
        return "echo"

    def inputs(self) -> List[ToolInput]:
        return [ToolInput("inp", str, position=0)]

    def outputs(self):
        return [ToolOutput("out", Stdout)]

    def container(self) -> str:
        return "ubuntu:latest"

    def version(self) -> str:
        return "TEST"


class OperatorResourcesTestTool(EchoTestTool):
    def inputs(self) -> List[ToolInput]:
        return [ToolInput("inputFile", File, position=1), ToolInput("outputFiles", int)]

    def memory(self, hints: Dict[str, Any]):
        return If(InputSelector("inputFile").file_size() > 1024, 4, 2)

    def cpus(self, hints: Dict[str, Any]):
        return 2 * InputSelector("outputFiles")

    def time(self, hints: Dict[str, Any]):
        return 60


class CatTestTool(CommandTool):
    def tool(self) -> str:
        return "CatTestTool"

    def base_command(self) -> Optional[Union[str, List[str]]]:
        return "cat"

    def inputs(self) -> List[ToolInput]:
        return [ToolInput("inp", File, position=0)]

    def outputs(self):
        return [ToolOutput("out", Stdout)]

    def container(self) -> str:
        return "ubuntu:latest"

    def version(self) -> str:
        return "TEST"


class SingleTestTool(CommandTool):
    def tool(self):
        return "TestStepTool"

    def base_command(self):
        return "echo"

    def inputs(self):
        return [
            ToolInput("input1", String(), position=0),
            ToolInput("input2", String(optional=True), position=1),
            ToolInput("input3", String(optional=True), position=2),
            ToolInput("input4", String(optional=True), position=3),
        ]

    def friendly_name(self):
        return None

    def outputs(self):
        return [ToolOutput("out", String(), glob=WildcardSelector("*"))]

    def container(self):
        return None

    def version(self):
        return None


class FilenameGeneratedTool(SingleTestTool):
    def id(self):
        return "filenamegeneratedtool"

    def inputs(self):
        return [
            ToolInput("inp", str),
            ToolInput("inpOptional", Optional[str]),
            ToolInput("fileInp", File(extension=".txt")),
            ToolInput("fileInpOptional", File(extension=".txt", optional=True)),
            ToolInput(
                "generatedInp",
                Filename(prefix=InputSelector("inp"), extension=""),
                position=0,
            ),
            ToolInput(
                "generatedInpOptional",
                Filename(prefix=InputSelector("inpOptional")),
                position=0,
            ),
            ToolInput(
                "generatedFileInp",
                Filename(
                    prefix=InputSelector("fileInp", remove_file_extension=True),
                    suffix=".transformed",
                    extension=".fnp",
                ),
                position=0,
            ),
            ToolInput(
                "generatedFileInpOptional",
                Filename(
                    prefix=InputSelector("fileInpOptional", remove_file_extension=True),
                    suffix=".optional",
                    extension=".txt",
                ),
                position=0,
            ),
        ]


class ArrayTestTool(CommandTool):
    def tool(self):
        return "ArrayStepTool"

    def friendly_name(self):
        return None

    def base_command(self):
        return "echo"

    def inputs(self):
        return [ToolInput("inps", Array(String()), position=1)]

    def outputs(self):
        return [ToolOutput("outs", Array(File()), glob=WildcardSelector("*"))]

    def container(self):
        return None

    def version(self):
        return None


class TestTool(CommandTool):
    def tool(self):
        return "TestTranslationtool"

    def base_command(self):
        return "echo"

    def inputs(self) -> List[ToolInput]:
        return [
            ToolInput("testtool", String()),
            ToolInput("arrayInp", Array(String, optional=True)),
        ]

    def arguments(self) -> List[ToolArgument]:
        return [ToolArgument(StringFormatter('test:\\t:escaped:\\n:characters"'))]

    def outputs(self) -> List[ToolOutput]:
        return [ToolOutput("std", Stdout())]

    def cpus(self, hints: Dict[str, Any]):
        return 2

    def memory(self, hints: Dict[str, Any]):
        return 2

    def friendly_name(self) -> str:
        return "Tool for testing translation"

    def container(self):
        return "ubuntu:latest"

    def version(self):
        return None

    def env_vars(self):
        return {"test1": InputSelector("testtool")}


class TestToolV2(TestTool):
    def version(self):
        return "v0.0.2"


class TestToolWithSecondaryOutput(TestTool):
    def outputs(self):
        return [
            ToolOutput(
                "out", TestTypeWithSecondary(), glob=InputSelector("testtool") + "/out"
            )
        ]


class TestToolWithAppendedSecondaryOutput(TestTool):
    def outputs(self):
        return [
            ToolOutput(
                "out",
                TestTypeWithAppendedSecondary(),
                selector=InputSelector("testtool") + ".bam",
            )
        ]


class TestToolWithReplacedSecondaryOutput(TestTool):
    def outputs(self):
        return [
            ToolOutput(
                "out",
                TestTypeWithReplacedSecondary(),
                selector=InputSelector("testtool") + ".bam",
            )
        ]


class TestToolWithSecondaryInput(CatTestTool):
    def inputs(self) -> List[ToolInput]:
        return [ToolInput("inp", TestTypeWithSecondary, position=0)]


class TestTypeWithSecondary(File):
    def __init__(self, optional=False):
        super().__init__(optional, extension=".txt")

    @staticmethod
    def secondary_files():
        return ["^.txt"]


class TestTypeWithAppendedSecondary(File):
    def __init__(self, optional=False):
        super().__init__(optional, extension=".bam")

    @staticmethod
    def secondary_files():
        return [".bai"]


class TestTypeWithReplacedSecondary(File):
    def __init__(self, optional=False):
        super().__init__(optional, extension=".bam")

    @staticmethod
    def secondary_files():
        return ["^.bai"]


class TestTypeWithNonEscapedSecondary(File):
    @staticmethod
    def secondary_files():
        return [".txt"]


class TestInputQualityTool(CommandTool):
    def tool(self) -> str:
        return "TESTONLY_inputQualityTool"

    def base_command(self) -> Optional[Union[str, List[str]]]:
        return "echo"

    def inputs(self) -> List[ToolInput]:
        return [
            ToolInput(
                "user", str, doc=InputDocumentation(None, quality=InputQualityType.user)
            ),
            ToolInput(
                "static",
                str,
                doc=InputDocumentation(None, quality=InputQualityType.static),
            ),
            ToolInput(
                "configuration",
                str,
                doc=InputDocumentation(None, quality=InputQualityType.configuration),
            ),
            ToolInput("none", str, doc=InputDocumentation(None, quality=None)),
        ]

    def outputs(self) -> List[ToolOutput]:
        return [ToolOutput("out", Stdout)]

    def container(self) -> str:
        return "ubuntu:latest"

    def version(self) -> str:
        return "TEST"


class TestWorkflowWithStepInputExpression(Workflow):
    def constructor(self):
        self.input("mystring", Optional[str], value="")
        self.input("mystring_backup", Optional[str])

        self.step(
            "print",
            EchoTestTool(
                inp=If(IsDefined(self.mystring), self.mystring, self.mystring_backup)
            ),
        )

        self.output("out", source=self.print)

    def friendly_name(self):
        return "TEST: WorkflowWithStepInputExpression"

    def id(self) -> str:
        return self.__class__.__name__


class TestWorkflowThatOutputsArraysOfSecondaryFiles(Workflow):
    def id(self) -> str:
        return "TestWorkflowThatOutputsArraysOfSecondaryFiles"

    def friendly_name(self):
        return "Test Workflow That outputs ararys of secondary files"

    def constructor(self):
        self.input("inp", Array(String))

        self.step(
            "stp", TestToolWithSecondaryOutput(testtool=self.inp), scatter="testtool"
        )

        self.output("out", source=self.stp.out)


class TestWorkflowWithConditionStep(Workflow):
    def constructor(self):
        self.input("mystring", Optional[str], value=None)

        someString = FirstOperator(
            [
                self.mystring,
                self.step(
                    "get_string",
                    EchoTestTool(inp="Some default value"),
                    when=self.mystring.is_null(),
                ).out,
            ]
        )

        self.step(
            "print",
            EchoTestTool(inp=someString),
        )

        self.output("out", source=self.print)

    def friendly_name(self):
        return "TEST: TestWorkflowWithConditionStep"

    def id(self) -> str:
        return self.__class__.__name__


class TestWorkflowWithAliasSelectorWorkflow(Workflow):
    def id(self) -> str:
        return "TestWorkflowWithAliasSelectorWorkflow"

    def friendly_name(self):
        return "Test Workflow with alias selector in the output"

    def constructor(self):
        self.input("inp", String, value="abc")

        self.step("stp1", TestToolWithSecondaryOutput(testtool=self.inp))
        self.step("stp2", CatTestTool(inp=self.stp1.out.as_type(File)))

        self.output("out", source=self.stp1.out)


class TestForEach(Workflow):
    def constructor(self):
        self.input("inp", Array(str))
        self.step(
            "print", EchoTestTool(inp=ForEachSelector() + "-hello"), _foreach=self.inp
        )
        self.output("out", source=self.print.out)

    def friendly_name(self):
        return self.id()

    def id(self) -> str:
        return "TestForEach"


class TestSplitTextTool(PythonTool):
    @staticmethod
    def code_block(inp: str) -> dict:
        # list splits "abc" into ["a", "b", "c"]
        return {"out": list(inp)}

    def outputs(self):
        return [TOutput("out", Array(String()))]


class TestJoinArrayTool(PythonTool):
    @staticmethod
    def code_block(inp: Array(String())) -> dict:
        return {"out": " ".join(inp)}

    def outputs(self):
        return [TOutput("out", String())]


class TestSumTool(PythonTool):
    @staticmethod
    def code_block(inp1: int, inp2: int) -> dict:
        return {"out": inp1 + inp2}

    def outputs(self):
        return [TOutput("out", Int())]


class TestFileInput(PythonTool):
    @staticmethod
    def code_block(inp: File) -> dict:
        with open(inp) as f:
            content = f.read()

        return {"out": content}

    def outputs(self):
        return [TOutput("out", String())]


class TestFileWithSecondaryInput(PythonTool):
    @staticmethod
    def code_block(inp: TestTypeWithSecondary) -> dict:
        with open(inp) as f:
            content = f.read()

        return {"out": content}

    def outputs(self):
        return [TOutput("out", String())]
