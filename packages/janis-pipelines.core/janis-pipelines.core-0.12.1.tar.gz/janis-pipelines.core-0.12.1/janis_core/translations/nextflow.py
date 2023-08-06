import os
import re
import posixpath
import json
from typing import Tuple, Dict, List, Optional, Union, Any

from janis_core.types import (
    DataType,
    Array,
    String,
    File,
    Int,
    Float,
    Double,
    Directory,
    Stdout,
    Stderr,
    Filename,
    InputSelector,
    WildcardSelector,
    Boolean,
    InputNodeSelector,
    StepOutputSelector,
    AliasSelector,
)
from janis_core.operators import Operator, StringFormatter, Selector

from janis_core.tool.commandtool import (
    CommandTool,
    ToolInput,
    ToolOutput,
    ToolArgument,
    Tool,
    ToolType,
    TOutput,
    TInput,
)
from janis_core.code.codetool import CodeTool
from janis_core.code.pythontool import PythonTool
from janis_core.translations.translationbase import TranslatorBase
from janis_core import Logger
from janis_core.workflow.workflow import StepNode, InputNode, OutputNode, WorkflowBase
from janis_core.utils.secondary import apply_secondary_file_format_to_filename
from janis_core.translationdeps.supportedtranslations import SupportedTranslation
from janis_core.translations import nfgen


class NextflowTranslator(TranslatorBase):
    LIB_FILENAME = "lib.nf"
    OUTPUT_METADATA_FILENAME = "janis.outputs.metadata"
    NO_FILE_PATH_PREFIX = f"JANIS_NO_FILE"
    PARAM_VAR = "%PARAM%"
    LIST_OF_FILES_PARAM = "%LIST_OF_FILES_PARAM%"
    LIST_OF_FILE_PAIRS_PARAM = "%LIST_OF_FILE_PAIRS_PARAM%"
    PYTHON_CODE_FILE_PATH_PARAM = "%PYTHON_CODE_FILE_PATH%"
    PYTHON_CODE_OUTPUT_FILENAME_PREFIX = "janis_out_"
    FINAL_STEP_NAME = "janis_outputs"
    TOOL_STDOUT_FILENAME = "janisstdout"

    INPUT_IN_SELECTORS = {}

    def __init__(self):
        super().__init__(name="nextflow")

    @classmethod
    def translate_workflow(
        cls,
        workflow,
        with_container=True,
        with_resource_overrides=False,
        allow_empty_container=False,
        container_override: dict = None,
    ) -> Tuple[any, Dict[str, any]]:

        step_keys = list(workflow.step_nodes.keys())
        process_files = {}
        tools = {}

        items_to_import = {}
        main_items = {}
        for step_id in workflow.step_nodes:
            tool = workflow.step_nodes[step_id].tool
            tools[tool.versioned_id()] = tool

            nf_items = cls.generate_nf_items_for_workflow_step(
                tool,
                step_id,
                step_keys,
                with_container=with_container,
                with_resource_overrides=with_resource_overrides,
                allow_empty_container=allow_empty_container,
                container_override=container_override,
            )
            nf_file = nfgen.NFFile(
                imports=[cls.init_helper_functions_import(".")], items=nf_items
            )

            tool_filename = f"{step_id}_{tool.versioned_id()}"
            process_files[tool_filename] = nf_file
            items_to_import[tool_filename] = [nf_items[0]]

            # for subworkflow, we only want the workflow object
            for i in nf_items:
                main_items[step_id] = nf_items[0]

        (
            out_process_inp,
            out_process_out,
        ) = cls.prepare_output_process_params_for_worfklow(workflow)

        imports = [cls.init_helper_functions_import()] + cls.init_tool_steps_import(
            items_to_import
        )
        items = [
            cls.generate_nf_output_process(out_process_inp, out_process_out),
            cls.generate_nf_workflow(workflow=workflow, nf_items=main_items),
        ]
        nf_file = nfgen.NFFile(imports=imports, items=items)

        tool_scripts = {t: process_files[t].get_string() for t in process_files}

        return (nf_file.get_string(), tool_scripts)

    @classmethod
    def generate_nf_items_for_workflow_step(
        cls,
        tool: Tool,
        step_id: str,
        step_keys: List[str],
        with_container=True,
        with_resource_overrides=False,
        allow_empty_container=False,
        container_override: dict = None,
    ) -> List[nfgen.NFBase]:
        """
        For each of the workflow step, we need to generate a Nextflow subworkflow or process object

        :param tool:
        :type tool:
        :param step_id:
        :type step_id:
        :param step_keys:
        :type step_keys:
        :param with_container:
        :type with_container:
        :param with_resource_overrides:
        :type with_resource_overrides:
        :param allow_empty_container:
        :type allow_empty_container:
        :param container_override:
        :type container_override:
        :return:
        :rtype:
        """
        provided_inputs = cls.generate_wf_tool_inputs(tool)

        if isinstance(tool, CommandTool):
            nf_item = cls.generate_nf_process_for_command_tool(
                tool, step_id, provided_inputs
            )
            nf_item = cls.handle_container(
                tool, nf_item, with_container, allow_empty_container, container_override
            )

            return [nf_item]
        elif isinstance(tool, PythonTool):
            nf_item = cls.generate_nf_process_for_python_code_tool(
                tool, step_id, provided_inputs
            )
            nf_item = cls.handle_container(
                tool, nf_item, with_container, allow_empty_container, container_override
            )

            return [nf_item]
        elif isinstance(tool, WorkflowBase):
            sub_step_keys = list(tool.step_nodes.keys())
            nf_items = []

            for sub_step_id in tool.step_nodes:
                step_tool = tool.step_nodes[sub_step_id].tool
                nf_items += cls.generate_nf_items_for_workflow_step(
                    step_tool,
                    f"{step_id}_{sub_step_id}",
                    sub_step_keys,
                    with_container=with_container,
                    with_resource_overrides=with_resource_overrides,
                    allow_empty_container=allow_empty_container,
                    container_override=container_override,
                )

            nf_items = [cls.generate_nf_subworkflow(tool, step_id, nf_items)] + nf_items

            return nf_items
        elif isinstance(tool, CodeTool):
            raise Exception("Only PythonTool code tool is supported for the moment")
        else:
            raise Exception(
                f"Nextflow translation for this {tool.__class__} is not yet supported"
            )

    @classmethod
    def translate_tool_internal(
        cls,
        tool: CommandTool,
        with_container: bool = True,
        with_resource_overrides: bool = False,
        allow_empty_container: bool = False,
        container_override: dict = None,
    ) -> str:
        """
        Generate Nextflow translation for Janis command line tool

        :param tool:
        :type tool:
        :param with_container:
        :type with_container:
        :param with_resource_overrides:
        :type with_resource_overrides:
        :param allow_empty_container:
        :type allow_empty_container:
        :param container_override:
        :type container_override:
        :return:
        :rtype:
        """

        process = cls.generate_nf_process_for_command_tool(tool)
        process = cls.handle_container(
            tool, process, with_container, allow_empty_container, container_override
        )

        imports = [cls.init_helper_functions_import()]

        out_process_inp, out_process_out = cls.prepare_output_process_params_for_tool(
            tool, process
        )

        items = [
            process,
            cls.generate_nf_output_process(
                inputs=out_process_inp, tool_outputs=out_process_out
            ),
            cls.generate_nf_execution_workflow(tool, nf_process=process),
        ]
        nf_file = nfgen.NFFile(imports=imports, items=items)

        return nf_file.get_string()

    @classmethod
    def translate_code_tool_internal(
        cls,
        tool: CodeTool,
        with_container=True,
        allow_empty_container=False,
        container_override: dict = None,
    ) -> str:
        """
        Generate Nextflow translation for Janis code tool

        :param tool:
        :type tool:
        :param with_container:
        :type with_container:
        :param allow_empty_container:
        :type allow_empty_container:
        :param container_override:
        :type container_override:
        :return:
        :rtype:
        """

        if isinstance(tool, PythonTool):
            process = cls.generate_nf_process_for_python_code_tool(tool)
            process = cls.handle_container(
                tool, process, with_container, allow_empty_container, container_override
            )

            imports = [cls.init_helper_functions_import()]

            (
                out_process_inp,
                out_process_out,
            ) = cls.prepare_output_process_params_for_tool(tool, process)

            items = [
                process,
                cls.generate_nf_output_process(
                    inputs=out_process_inp, tool_outputs=out_process_out
                ),
                cls.generate_nf_execution_workflow(tool, nf_process=process),
            ]
            nf_file = nfgen.NFFile(imports=imports, items=items)

            return nf_file.get_string()
        else:
            raise Exception("Only PythonTool code tool is supported for the moment.")

    @classmethod
    def generate_nf_subworkflow(
        cls, subworkflow: WorkflowBase, name: str, nf_items: List[nfgen.NFBase]
    ) -> nfgen.Workflow:
        """
        Generate a Nextflow Workflow object for a Janis subworkflow inside a workflow

        :param subworkflow:
        :type subworkflow:
        :param name:
        :type name:
        :param nf_items:
        :type nf_items:
        :return:
        :rtype:
        """
        main = []
        take = []
        emit = []

        inputsdict = subworkflow.inputs_map()
        step_keys = list(subworkflow.step_nodes.keys())

        wf_provided_inputs = cls.generate_wf_tool_inputs(subworkflow)

        for i in subworkflow.input_nodes:
            if (
                i not in wf_provided_inputs
                and subworkflow.input_nodes[i].default is not None
            ):
                wf_provided_inputs[i] = subworkflow.input_nodes[i].default

        for key in subworkflow.connections:
            as_param = None
            input_type = inputsdict.get(key).intype
            if isinstance(input_type, File):
                # inp.as_process_param = f"Channel.fromPath({cls.PARAM_VAR}).collect()"
                as_param = cls.LIST_OF_FILES_PARAM
            elif isinstance(input_type, Array) and isinstance(
                input_type.subtype(), Array
            ):
                as_param = cls.LIST_OF_FILE_PAIRS_PARAM

            take.append(nfgen.WorkflowInput(name=key, as_param=as_param))

        for step_id in subworkflow.step_nodes:
            nf_item = [i for i in nf_items if i.name == f"{name}_{step_id}"][0]
            tool = subworkflow.step_nodes[step_id].tool
            tool_inp_dict = tool.inputs_map()

            provided_inputs = cls.generate_wf_tool_inputs(
                tool,
                inputs_replacement="$",
                tool_id_prefix=f"${name}_",
            )

            provided_inputs = cls.apply_outer_workflow_inputs(
                subworkflow, tool, provided_inputs, wf_provided_inputs
            )

            args = cls.handle_nf_process_args(
                tool,
                nf_item.inputs,
                tool_inp_dict,
                provided_inputs,
                input_param_prefix=f"{name}_{step_id}_",
                step_key_prefix=f"{name}_",
                workflow=subworkflow,
                scatter=subworkflow.step_nodes[step_id].scatter,
            )

            main.append(f"{name}_{step_id}({args})")

        wf_outputs = cls.generate_wf_tool_outputs(subworkflow, f"{name}_")
        for o in wf_outputs:
            emit.append(nfgen.WorkflowOutput(name=o, expression=wf_outputs[o]))

        return nfgen.Workflow(name=name, main=main, take=take, emit=emit)

    @classmethod
    def generate_nf_workflow(
        cls,
        workflow,
        nf_items: Dict[str, Union[nfgen.Process, nfgen.Workflow]],
        nf_workflow_name: str = "",
    ) -> nfgen.Workflow:
        """
        Generate a Nextflow Workflow object

        :param workflow:
        :type workflow:
        :param nf_items:
        :type nf_items:
        :param nf_workflow_name:
        :type nf_workflow_name:
        :return:
        :rtype:
        """
        main = []

        step_keys = list(workflow.step_nodes.keys())

        for step_id in workflow.step_nodes:
            tool = workflow.step_nodes[step_id].tool
            provided_inputs = cls.generate_wf_tool_inputs(tool)

            inputsdict = tool.inputs_map()

            nf_process = nf_items[step_id]

            if isinstance(nf_process, nfgen.Process):
                nf_inputs = nf_process.inputs
            elif isinstance(nf_process, nfgen.Workflow):
                nf_inputs = nf_process.take

            args = cls.handle_nf_process_args(
                tool,
                nf_inputs,
                inputsdict,
                provided_inputs,
                input_param_prefix=f"{step_id}_",
                workflow=workflow,
                scatter=workflow.step_nodes[step_id].scatter,
            )

            main.append(f"{nf_process.name}({args})")

        # calling outputs process for Janis to be able to find output files
        args_list = [val for val in cls.generate_wf_tool_outputs(workflow).values()]

        args = ", ".join(args_list)
        main.append(f"{cls.FINAL_STEP_NAME}({args})")

        return nfgen.Workflow(name=nf_workflow_name, main=main)

    @classmethod
    def apply_outer_workflow_inputs(
        cls,
        workflow: WorkflowBase,
        tool: Tool,
        provided_inputs: Dict[str, Any],
        wf_provided_inputs: Dict[str, Any],
    ) -> dict:
        """
        Generate a dictionary of user provided inputs for a tool by
        taking into considerations inputs provided to its parent workflow

        :param workflow:
        :type workflow:
        :param provided_inputs: inputs provided to this tool
        :type provided_inputs:
        :param wf_provided_inputs: inputs provided to the outer workflow this tool is called from
        :type wf_provided_inputs:
        :return:
        :rtype:
        """
        # Apply value from workflow that is calling it
        wf_input_names = workflow.connections.keys()
        step_keys = workflow.step_nodes.keys()
        wf_inputsdict = workflow.inputs_map()
        tool_inputsdict = tool.inputs_map()

        for key in provided_inputs:
            val = provided_inputs[key]

            # Here, we are looking for input variables that are not an input of the subworkflow
            # but, it is pointing to a variable of the outer workflow that calls this workflow
            if (
                key not in wf_input_names
                and isinstance(val, str)
                and val.startswith("$")
            ):
                if key in wf_provided_inputs:
                    provided_inputs[key] = str(wf_provided_inputs[key])

            # if we are just using the variable name from the nextflow subworkflow
            for wf_input in wf_inputsdict:
                if val is not None and val == f"${wf_input}":
                    wf_inp_type = wf_inputsdict.get(wf_input).intype
                    tool_inp_type = (
                        tool_inputsdict.get(key).intype
                        or tool_inputsdict.get(key).input_type
                    )
                    if (
                        isinstance(wf_inp_type, File)
                        and wf_inp_type.has_secondary_files()
                    ):
                        if (
                            tool_inp_type.is_base_type(File)
                            and not tool_inp_type.has_secondary_files()
                        ) or (
                            isinstance(tool_inp_type, Array)
                            and isinstance(tool_inp_type.subtype(), File)
                            and not tool_inp_type.subtype().has_secondary_files()
                        ):
                            provided_inputs[key] += ".map{ tuple -> tuple[0] }"

            for step_key in step_keys:
                if isinstance(val, str) and f"{step_key}.out." in val:

                    parts = val.strip("][").split(f"{step_key}.out.")
                    step_output_var = parts[1]
                    step_outputs = workflow.step_nodes.get(step_key).outputs()

                    src_type = step_outputs.get(step_output_var).outtype
                    tool_inp_type = (
                        tool_inputsdict.get(key).intype
                        or tool_inputsdict.get(key).input_type
                    )

                    # any file types or array of files
                    if src_type.is_base_type(File) and src_type.has_secondary_files():
                        if (
                            tool_inp_type.is_base_type(File)
                            and not tool_inp_type.has_secondary_files()
                        ) or (
                            isinstance(tool_inp_type, Array)
                            and isinstance(tool_inp_type.subtype(), File)
                            and not tool_inp_type.subtype().has_secondary_files()
                        ):
                            provided_inputs[key] += ".map{ tuple -> tuple[0] }"

        # Now, get rid of anything that points to workflow input variables but is not provided as workflow inputs
        for key, val in provided_inputs.items():
            if isinstance(val, str) and val.startswith("$"):
                val = val.strip("$")
                if val in wf_inputsdict and val not in wf_provided_inputs:
                    provided_inputs[key] = None

        return provided_inputs

    @classmethod
    def handle_container(
        cls,
        tool,
        process: nfgen.Process,
        with_container: bool = True,
        allow_empty_container=False,
        container_override: dict = None,
    ) -> nfgen.Process:
        """
        Add container information to a Nexflow Process object

        :param tool:
        :type tool:
        :param process:
        :type process:
        :param with_container:
        :type with_container:
        :param allow_empty_container:
        :type allow_empty_container:
        :param container_override:
        :type container_override:
        :return:
        :rtype:
        """
        if with_container:
            container = (
                NextflowTranslator.get_container_override_for_tool(
                    tool, container_override
                )
                or tool.container()
            )

        if container is not None:
            process.directives.append(
                nfgen.ContainerDirective(
                    cls.unwrap_expression(container, quote_string=False, tool=tool)
                )
            )
        elif not allow_empty_container:
            raise Exception(
                f"The tool '{tool.id()}' did not have a container and no container override was specified. "
                f"Although not recommended, Janis can export empty docker containers with the parameter "
                f"'allow_empty_container=True' or --allow-empty-container"
            )

        return process

    @classmethod
    def generate_python_script(cls, tool: PythonTool) -> str:
        """
        Generate python script to be included inside a Nextflow process

        :param tool:
        :type tool:
        :return:
        :rtype:
        """
        return tool.prepared_script(SupportedTranslation.Nextflow)

    @classmethod
    def translate_helper_files(cls, tool) -> Dict[str, str]:
        """
        Generate a dictionary of helper files to run Nextflow.
        Key of the dictionary is the filename, the value is the file content

        :param tool:
        :type tool:
        :return:
        :rtype:
        """
        helpers = {}

        # Groovy helper functions
        lib_file = nfgen.NFFile(imports=[], items=cls.generate_generic_functions())
        helpers[cls.LIB_FILENAME] = lib_file.get_string()

        helpers = cls.generate_python_code_files(tool, helpers)

        return helpers

    @classmethod
    def generate_python_code_files(cls, tool: PythonTool, helpers: dict):
        # Python files for Python code tools
        if isinstance(tool, PythonTool):
            helpers["__init__.py"] = ""
            helpers[f"{tool.versioned_id()}.py"] = cls.generate_python_script(tool)
            return helpers

        elif isinstance(tool, WorkflowBase):
            for step_id in tool.step_nodes:
                step_tool = tool.step_nodes[step_id].tool
                helpers = cls.generate_python_code_files(step_tool, helpers)

        return helpers

    @classmethod
    def prepare_output_process_params_for_tool(
        cls, tool: Tool, nf_process: nfgen.NFBase
    ):
        """
        Every one of our tools will call a Nextflow process named "janis_outputs".
        This process will collect all the final outputs for this tool or workflow.
        This allows Janis to process outputs more easily.

        This function is used to generate the inputs and outputs for "janis_outputs" Nextflow process.

        :param tool:
        :type tool:
        :param nf_process: This is the Nextflow Process of the actual tool
        :type nf_process:
        :return:
        :rtype:
        """
        inputs = []
        for o in nf_process.outputs:
            # Always use 'val' qualifier
            inp = nfgen.ProcessInput(
                qualifier=nfgen.InputProcessQualifier.val, name=nf_process.name + o.name
            )
            inputs.append(inp)

        tool_outputs = cls.prepare_tool_output(tool)

        return inputs, tool_outputs

    @classmethod
    def prepare_output_process_params_for_worfklow(
        cls, workflow: WorkflowBase
    ) -> Tuple[List[nfgen.ProcessInput], Dict]:
        """
        Every one of our tools will call a Nextflow process named "janis_outputs".
        This process will collect all the final outputs for this tool or workflow.
        This allows Janis to process outputs more easily.

        This function is used to generate the inputs and outputs for "janis_outputs" Nextflow workflow.

        :param workflow:
        :type workflow:
        :return:
        :rtype:
        """
        wf_outputs = cls.generate_wf_tool_outputs(workflow)
        output_dict = workflow.outputs_map()

        inputs = []
        outputs = {}

        for key, val in wf_outputs.items():
            inp_var_name = key.replace(".", "")
            # Always use 'val' qualifier
            inp = nfgen.ProcessInput(
                qualifier=nfgen.InputProcessQualifier.val, name=inp_var_name
            )
            inputs.append(inp)

            output_var = inp_var_name
            if key in output_dict:
                if (
                    output_dict[key].outtype.is_array()
                    and isinstance(output_dict[key].outtype.subtype(), File)
                    and output_dict[key].outtype.subtype().has_secondary_files()
                ):
                    output_var = f"{inp_var_name}.map{{ item -> item[0] }}"
                elif (
                    isinstance(output_dict[key].outtype, File)
                    and output_dict[key].outtype.has_secondary_files()
                ):
                    output_var = f"{inp_var_name}[0]"

            outputs[key] = f"${{{output_var}}}"

        return inputs, outputs

    @classmethod
    def generate_nf_output_process(
        cls, inputs: List[nfgen.ProcessInput], tool_outputs: Dict
    ) -> nfgen.Process:
        """
        Every one of our tools will call a Nextflow process named "janis_outputs".
        This process will collect all the final outputs for this tool or workflow.
        This allows Janis to process outputs more easily.

        This function creates this "janis_outputs" Nextflow process.

        :param inputs:
        :type inputs:
        :param tool_outputs:
        :type tool_outputs:
        :return:
        :rtype:
        """

        # The script is simply adding tool outputs as key-value pairs into a text file
        script = ""
        for key, val in tool_outputs.items():
            script += f"echo {key}={val} >> {cls.OUTPUT_METADATA_FILENAME}\n"

        outputs = [
            nfgen.ProcessOutput(
                qualifier=nfgen.OutputProcessQualifier.path,
                name="janis_output_metadata",
                expression=f"'{cls.OUTPUT_METADATA_FILENAME}'",
            )
        ]

        process = nfgen.Process(
            name=cls.FINAL_STEP_NAME,
            script=script,
            script_type=nfgen.ProcessScriptType.script,
            inputs=inputs,
            outputs=outputs,
        )

        process.directives.append(nfgen.CacheDirective(False))

        return process

    @classmethod
    def init_helper_functions_import(cls, path: Optional[str] = None) -> nfgen.Import:
        """
        Generate Nextflow Import object to import our Groovy helper functions

        :param path:
        :type path:
        :return:
        :rtype:
        """
        if path is None:
            path = os.path.join(".", cls.DIR_TOOLS)

        items = [
            nfgen.ImportItem(name=f.name) for f in cls.generate_generic_functions()
        ]
        return nfgen.Import(items, os.path.join(path, cls.LIB_FILENAME))

    @classmethod
    def init_tool_steps_import(
        cls, processes: Dict[str, nfgen.Process]
    ) -> List[nfgen.Import]:
        """
        Generate a list of Nextflow Import objects for each of the steps in a workflow.

        :param processes:
        :type processes:
        :return:
        :rtype:
        """
        imports = []
        for filename, nf_items in processes.items():
            items_in_one_file = []
            for p in nf_items:
                item = nfgen.ImportItem(name=p.name)
                items_in_one_file.append(item)

            imp = nfgen.Import(
                items_in_one_file, os.path.join(".", cls.DIR_TOOLS, filename)
            )
            imports.append(imp)

        return imports

    @classmethod
    def generate_nf_process_for_command_tool(
        cls,
        tool: CommandTool,
        name: Optional[str] = None,
        provided_inputs: Optional = None,
    ) -> nfgen.Process:
        """
        Generate a Nextflow Process object for a Janis Command line tool

        :param tool:
        :type tool:
        :param name: Generally, this is a workflow step id, so that we can prefix variables or process names
        :type name:
        :param provided_inputs:
        :type provided_inputs:
        :return:
        :rtype:
        """
        inputs: List[ToolInput] = []

        # construct script
        for i in tool.inputs():
            if provided_inputs is not None:
                optional = (
                    i.input_type.optional is None or i.input_type.optional is True
                )
                if i.id() in provided_inputs or i.default is not None or not optional:
                    inputs.append(i)
                elif isinstance(i.input_type, Filename):
                    inputs.append(i)
            else:
                inputs.append(i)

        process_name = name or tool.id()
        script = cls.prepare_script_for_command_tool(process_name, tool, inputs)
        pre_script = cls.prepare_expression_inputs(tool, inputs)
        pre_script += cls.prepare_input_vars(inputs)

        (
            resources_var,
            resource_var_names,
            resource_param_names,
        ) = cls.prepare_resources_var(tool, name)
        pre_script += resources_var

        # pre_script += cls.prepare_inputs_in_selector(tool, inputs, resource_var_names)
        pre_script = (
            cls.prepare_inputs_in_selector(tool, inputs, resource_var_names)
            + pre_script
        )

        process = nfgen.Process(
            name=process_name,
            script=script,
            script_type=nfgen.ProcessScriptType.script,
            pre_script=pre_script,
        )

        for i in inputs:
            qual = cls.get_input_qualifier_for_inptype(i.input_type)
            inp = nfgen.ProcessInput(qualifier=qual, name=i.id())

            process.inputs.append(inp)

        process.outputs = cls.generate_nf_outputs_for_nf_process(process_name, tool)
        process.directives = cls.generate_nf_directives_for_nf_process(
            process_name, resource_param_names
        )

        return process

    @classmethod
    def generate_nf_directives_for_nf_process(
        cls, process_name: str, resource_param_names: List[str]
    ) -> List[nfgen.ProcessDirective]:

        nf_directives = []
        nf_directives.append(nfgen.PublishDirDirective(f"$launchDir/{process_name}"))

        # Add directives for input resources
        for res in resource_param_names:
            if res.endswith("runtime_cpu"):
                nf_directives.append(nfgen.CpusDirective(f"${{{res} ? {res} : ''}}"))
            elif res.endswith("runtime_memory"):
                nf_directives.append(
                    nfgen.MemoryDirective(f"${{{res} ? {res} + 'GB': ''}}")
                )
            elif res.endswith("runtime_seconds"):
                nf_directives.append(nfgen.TimeDirective(f"${{{res} + 's'}}"))
            elif res.endswith("runtime_disks"):
                nf_directives.append(
                    nfgen.DiskDirective(f"${{{res} ? {res} + 'GB': ''}}")
                )

        return nf_directives

    @classmethod
    def generate_nf_outputs_for_nf_process(
        cls, process_name: str, tool: Tool
    ) -> List[nfgen.ProcessOutput]:
        """
        Generate a list of tool outputs in the form of nfgen.ProcessOutput objects

        :param process_name:
        :type process_name:
        :param tool:
        :type tool:
        :return:
        :rtype:
        """
        outputs: List[ToolOutput] = tool.outputs()

        nf_outputs = []
        for o in outputs:
            output_type = o.output_type
            selector = o.selector

            qual = cls.get_output_qualifier_for_outtype(output_type)
            expression = cls.unwrap_expression(
                selector, inputs_dict=tool.inputs_map(), tool=tool, for_output=True
            )

            if isinstance(output_type, Array):
                if isinstance(output_type.subtype(), (File, Directory)):
                    sub_qual = nfgen.OutputProcessQualifier.path
                else:
                    sub_qual = nfgen.OutputProcessQualifier.val

                tuple_elements = expression.strip("][").split(",")
                formatted_list = []
                for expression in tuple_elements:
                    sub_exp = nfgen.TupleElementForOutput(
                        qualifier=sub_qual, expression=expression
                    )
                    formatted_list.append(sub_exp.get_string())

                expression = ", ".join(formatted_list)
            elif isinstance(output_type, Stdout):
                expression = f"'{cls.TOOL_STDOUT_FILENAME}_{process_name}'"
            elif isinstance(output_type, File) and output_type.has_secondary_files():
                sub_qual = nfgen.OutputProcessQualifier.path
                tuple_elements = [expression]

                primary_ext = output_type.extension
                secondary_ext = []

                if o.secondaries_present_as is not None:
                    secondaries_present_as = o.secondaries_present_as
                else:
                    secondaries_present_as = {}

                for ext in output_type.secondary_files():
                    if ext in secondaries_present_as:
                        secondary_ext.append(secondaries_present_as[ext])
                    else:
                        secondary_ext.append(ext)

                for ext in secondary_ext:
                    replacement = primary_ext + ext
                    if ext.startswith("^"):
                        replacement = ext[1:]

                    sec_exp = None
                    if primary_ext in expression:
                        sec_exp = expression.replace(primary_ext, replacement)
                    elif ".name" in expression:
                        sec_exp = expression.replace(
                            ".name", f".baseName + '{replacement}'"
                        )

                    if sec_exp is not None:
                        tuple_elements.append(sec_exp)

                formatted_list = []
                for sec_exp in tuple_elements:
                    tuple_el = nfgen.TupleElementForOutput(
                        qualifier=sub_qual, expression=sec_exp
                    )
                    formatted_list.append(tuple_el.get_string())

                expression = ", ".join(formatted_list)
                qual = nfgen.OutputProcessQualifier.tuple

            out = nfgen.ProcessOutput(
                qualifier=qual,
                name=o.id(),
                expression=expression,
                # is_optional=output_type.optional, # disable this because nextflow doesn't allow workflow to point to optional output
            )

            nf_outputs.append(out)

        return nf_outputs

    @classmethod
    def generate_nf_output_expression(cls, o: Union[TOutput, ToolOutput]):
        """
        Based on the Janis output type, we generate string expression to represent outputs in Nextflow Process.

        :param tool:
        :type tool:
        :param o:
        :type o:
        :return:
        :rtype:
        """
        if isinstance(o, TOutput):
            output_type = o.outtype
        elif isinstance(o, ToolOutput):
            output_type = o.output_type
        else:
            raise Exception("Unknown output object")

        if isinstance(output_type, File):
            expression = f"'*{output_type.extension}'"
            qual = nfgen.OutputProcessQualifier.path
        elif isinstance(output_type, Array) and isinstance(output_type.subtype(), File):
            expression = f"'*{output_type.subtype().extension}'"
            qual = nfgen.OutputProcessQualifier.path
        else:
            qual = nfgen.OutputProcessQualifier.val
            expression = f"file(\"$workDir/{cls.PYTHON_CODE_OUTPUT_FILENAME_PREFIX}{o.tag}\").text.replace('[', '').replace(']', '').split(', ')"

        return qual, expression

    @classmethod
    def generate_nf_process_for_python_code_tool(
        cls,
        tool: CodeTool,
        name: Optional[str] = None,
        provided_inputs: Optional = None,
    ) -> nfgen.Process:
        """
        Generate a Nextflow Process object for Janis python code tool

        :param tool:
        :type tool:
        :param name:
        :type name:
        :param provided_inputs:
        :type provided_inputs:
        :return:
        :rtype:
        """
        inputs: List[TInput] = []
        outputs: List[TOutput] = tool.outputs()

        # construct script
        for i in tool.inputs():
            if provided_inputs is not None:
                optional = i.intype.optional is None or i.intype.optional is True
                if i.id() in provided_inputs or i.default is not None or not optional:
                    inputs.append(i)
                # note: Filename is set to optional=True, but they have a default value that is not set to i.default
                if isinstance(i.intype, Filename):
                    inputs.append(i)
            else:
                inputs.append(i)

        script = cls.prepare_script_for_python_code_tool(tool, inputs)

        process_name = name or tool.id()
        process = nfgen.Process(
            name=process_name,
            script=script,
            script_type=nfgen.ProcessScriptType.script,
        )

        python_file_input = nfgen.ProcessInput(
            qualifier=nfgen.InputProcessQualifier.path,
            name=cls.PYTHON_CODE_FILE_PATH_PARAM.strip("%"),
            as_param=cls.PYTHON_CODE_FILE_PATH_PARAM,
        )
        process.inputs.append(python_file_input)
        for i in inputs:
            qual = cls.get_input_qualifier_for_inptype(i.intype)
            inp = nfgen.ProcessInput(qualifier=qual, name=i.id())

            if isinstance(i.intype, File) or (
                isinstance(i.intype, Array) and isinstance(i.intype.subtype(), File)
            ):
                inp.as_param = cls.LIST_OF_FILES_PARAM

            process.inputs.append(inp)

        for o in outputs:
            qual, expression = cls.generate_nf_output_expression(o)
            out = nfgen.ProcessOutput(
                qualifier=qual, name=o.id(), expression=expression
            )
            process.outputs.append(out)

        (
            resources_var,
            resource_var_names,
            resource_param_names,
        ) = cls.prepare_resources_var(tool, name)

        process.directives = cls.generate_nf_directives_for_nf_process(
            process_name, resource_param_names
        )

        return process

    @classmethod
    def handle_nf_process_args(
        cls,
        tool: Tool,
        nfgen_inputs: Union[List[nfgen.ProcessInput], List[nfgen.WorkflowInput]],
        inputsdict: Dict[str, ToolInput],
        provided_inputs: Dict[str, Any],
        workflow: WorkflowBase,
        input_param_prefix: str = "",
        step_key_prefix: str = "",
        scatter: Optional[str] = None,
    ) -> str:
        """
        Generate a string to represent a Nextflow process arguments

        :param tool:
        :type tool:
        :param nfgen_inputs:
        :type nfgen_inputs:
        :param inputsdict:
        :type inputsdict:
        :param provided_inputs:
        :type provided_inputs:
        :param workflow:
        :type workflow:
        :param scatter:
        :type scatter:
        :return:
        :rtype:
        """
        step_keys = [f"{step_key_prefix}{s}" for s in list(workflow.step_nodes.keys())]

        args_list = []
        for i in nfgen_inputs:
            if i.name in provided_inputs:
                p = provided_inputs[i.name]
                if p is None:
                    p = "''"
                elif isinstance(p, bool):
                    p = f"'{p}'"
                elif "$" in p:
                    p = p.replace("$", "")
                else:
                    p = f"'{p}'"
            elif i.name in inputsdict:
                p = f"'{inputsdict[i.name].default}'" or "''"
                if "inputs." in p:
                    p = p.replace("inputs.", f"params.{input_param_prefix}").strip("'")
            else:
                p = i.as_param

            # Extra processing
            if cls.PYTHON_CODE_FILE_PATH_PARAM in p:
                path_to_python_code_file = posixpath.join(
                    "$baseDir", cls.DIR_TOOLS, f"{tool.versioned_id()}.py"
                )
                p = p.replace(
                    cls.PYTHON_CODE_FILE_PATH_PARAM, f'"{path_to_python_code_file}"'
                )
            elif i.name in inputsdict:
                toolinput = inputsdict.get(i.name)

                if isinstance(toolinput, ToolInput):
                    input_type = toolinput.input_type
                elif isinstance(toolinput, TInput):
                    input_type = toolinput.intype

                if isinstance(input_type, File):
                    if p.startswith("params."):
                        p = f"Channel.fromPath({p}).collect()"
                elif isinstance(input_type, Array) and isinstance(
                    input_type.subtype(), Array
                ):
                    if p.startswith("params."):
                        p = f"Channel.from({p}).map{{ pair -> pair }}"
                # we need to concat multiple list of channels
                elif isinstance(input_type, Array) and isinstance(
                    input_type.subtype(), File
                ):
                    if input_type.subtype().has_secondary_files():
                        p = p.strip("][").replace(",", " + ")

            if scatter is not None and i.name in scatter.fields:
                p = cls.handle_scatter_argument(p, inputsdict[i.name], step_keys)

            args_list.append(p)

        args = ", ".join(args_list)

        return args

    @classmethod
    def handle_scatter_argument(
        cls, p: str, input: ToolInput, step_keys: List[str] = []
    ):
        """

        :param p: string to represent the argument
        :type p: str
        :param step_keys: List of worfklow step names
        :type step_keys: List[str]

        :return:
        :rtype:
        """
        if isinstance(input, ToolInput):
            input_type = input.input_type
        elif isinstance(input, TInput):
            input_type = input.intype
        else:
            raise Exception("Unknown input object")

        # If it comes from our input files, it is already properly formatted
        # e.g array of array are in the correct formats
        matches = []
        pattern = r"\b(params(\..+?)+)\b"
        found = re.findall(pattern, p)
        # found is in this format
        # [('params.intervals', '.intervals'), ('step_id.out.test', '.test')]
        if found is not None:
            matches += [t[0] for t in found]

        for m in matches:
            p = p.replace(m, f"Channel.from({m}).map{{ item -> item }}")

        # Handling outputs from internal workflow steps
        matches = []
        for step_id in step_keys:
            pattern = rf"\b({step_id}(\..+?)+)\b"
            found = re.findall(pattern, p)
            # found is in this format
            # [('params.intervals', '.intervals'), ('step_id.out.test', '.test')]
            if found is not None:
                matches += [t[0] for t in found]

        for m in matches or []:
            if input_type.has_secondary_files() or input_type.is_paired():
                p = p.replace(m, f"{m}.map{{ pair -> pair }}")
            else:
                p = p.replace(m, f"{m}.flatten()")

        return p

    @classmethod
    def generate_nf_execution_workflow(
        cls, tool, nf_process: nfgen.Process
    ) -> nfgen.Workflow:
        """
        In the main translation file, we call a Nextflow Workflow even if it is only for a tool.
        This function generates this Nextflow Workflow object.

        :param tool:
        :type tool:
        :param nf_process:
        :type nf_process:
        :return:
        :rtype:
        """
        args_list = []
        for i in nf_process.inputs:
            p = f"params.{i.name}"

            # Extra processing when we need to set up the process input parameters
            if i.as_param:
                if cls.LIST_OF_FILES_PARAM in i.as_param:
                    p = i.as_param.replace(
                        cls.LIST_OF_FILES_PARAM, f"Channel.fromPath({p}).collect()"
                    )
                elif cls.LIST_OF_FILE_PAIRS_PARAM in i.as_param:
                    p = i.as_param.replace(
                        cls.LIST_OF_FILE_PAIRS_PARAM,
                        f"Channel.from({p}).map{{ pair -> pair }}",
                    )
                elif cls.PYTHON_CODE_FILE_PATH_PARAM in i.as_param:

                    path_to_python_code_file = posixpath.join(
                        "$baseDir", cls.DIR_TOOLS, f"{tool.versioned_id()}.py"
                    )
                    p = i.as_param.replace(
                        cls.PYTHON_CODE_FILE_PATH_PARAM, f'"{path_to_python_code_file}"'
                    )

            args_list.append(p)

        args = ", ".join(args_list)
        outputs_args = ", ".join(
            f"{nf_process.name}.out.{o.name}" for o in nf_process.outputs
        )

        main = [f"{nf_process.name}({args})", f"{cls.FINAL_STEP_NAME}({outputs_args})"]

        return nfgen.Workflow(name="", main=main)

    @classmethod
    def generate_wf_tool_inputs(
        cls,
        tool: Tool,
        inputs_replacement: str = "$params.",
        tool_id_prefix: str = "$",
    ) -> dict:
        """
        Generate a dictionary to represent the input values provided to a tool
        key is the input name
        value is the input expression

        :param tool:
        :type tool:
        :param inputs_replacement:
        :type inputs_replacement:
        :param tool_id_prefix:
        :type tool_id_prefix:
        :return:
        :rtype:
        """

        inputs = {}
        for key in tool.connections:
            if tool.connections[key] is None:
                val = None
            elif hasattr(tool.connections[key], "nextflow"):
                val = tool.connections[key].nextflow(
                    var_indicator=inputs_replacement, step_indicator=tool_id_prefix
                )
            else:
                val = cls.unwrap_expression(
                    tool.connections[key],
                    tool=tool,
                    inputs_dict=tool.inputs_map(),
                    quote_string=False,
                    var_indicator=inputs_replacement,
                    step_indicator=tool_id_prefix,
                )

            inputs[key] = val

        return inputs

    @classmethod
    def generate_wf_tool_outputs(
        cls, wf: WorkflowBase, tool_var_prefix: str = ""
    ) -> Dict[str, str]:
        """
        Generate a dictionary containing values of tool output expressions
        key is the output tag name
        value is the output expression

        :param wf:
        :type wf:
        :param tool_var_prefix:
        :type tool_var_prefix:
        :return:
        :rtype:
        """

        outputs = {}
        for o in wf.output_nodes:
            if hasattr(wf.output_nodes[o].source, "nextflow"):
                val = wf.output_nodes[o].source.nextflow(step_indicator=tool_var_prefix)
            else:
                val = str(val)

            outputs[o] = val

        return outputs

    @classmethod
    def generate_generic_functions(cls) -> List[nfgen.Function]:
        """
        Generate Groovy helper functions to run our Nextflow processes

        :return:
        :rtype:
        """

        functions = [
            nfgen.Function(
                name="apply_prefix",
                parameters=["var", "prefix", "prefix_applies_to_all_elements"],
                definition=f"""
if (prefix_applies_to_all_elements == 'True') {{
    def l = var.split(' ')
    
    prefix = prefix.toString() 
    
    return prefix + l.join(' ' + prefix)
}}
else {{
    return prefix.toString() + var.toString()
}}
""",
            ),
            nfgen.Function(
                name="optional",
                parameters=["var", "prefix", "prefix_applies_to_all_elements"],
                definition=f"""
var = var.toString()
if (var && ( var != 'None' ) && (! var.contains('{cls.NO_FILE_PATH_PREFIX}')))
{{
    return apply_prefix(var, prefix, prefix_applies_to_all_elements)
}}
else
{{
    return ''
}}
""",
            ),
            nfgen.Function(
                name="boolean_flag",
                parameters=["var", "prefix"],
                definition=f"""
var = var.toString()
if (var == 'True')
{{
    return prefix.toString()
}}
else
{{
    return ''
}}
""",
            ),
            nfgen.Function(
                name="get_primary_files",
                parameters=["var"],
                definition=f"""
def primary = []

var.eachWithIndex {{item, index -> 
    if (index % 2 == 0) {{
        primary.add(item)
    }}
}}

return primary

""",
            ),
        ]

        return functions

    @classmethod
    def unwrap_expression(
        cls,
        value,
        quote_string=True,
        tool=None,
        for_output=False,
        inputs_dict=None,
        skip_inputs_lookup=False,
        in_shell_script=False,
        var_indicator=None,
        step_indicator=None,
        **debugkwargs,
    ):
        """
        The main logic to unwrap a janis expression and represent it in Nextflow translation

        :param value:
        :type value:
        :param quote_string:
        :type quote_string:
        :param tool:
        :type tool:
        :param for_output:
        :type for_output:
        :param inputs_dict:
        :type inputs_dict:
        :param skip_inputs_lookup:
        :type skip_inputs_lookup:
        :param in_shell_script:
        :type in_shell_script:
        :param debugkwargs:
        :type debugkwargs:
        :return:
        :rtype:
        """
        if value is None:
            if quote_string:
                return "null"
            return None

        if isinstance(value, StepNode):
            raise Exception(
                f"The Step node '{value.id()}' was found when unwrapping an expression, "
                f"you might not have selected an output."
            )

        if isinstance(value, list):
            toolid = debugkwargs.get("tool_id", "unwrap_list_expression")
            elements = []
            for i in range(len(value)):
                el = cls.unwrap_expression(
                    value[i],
                    quote_string=quote_string,
                    tool=tool,
                    tool_id=toolid + "." + str(i),
                    inputs_dict=inputs_dict,
                    skip_inputs_lookup=skip_inputs_lookup,
                    for_output=for_output,
                    in_shell_script=in_shell_script,
                    var_indicator=var_indicator,
                    step_indicator=step_indicator,
                )

                elements.append(el)

            list_representation = f"[{', '.join(elements)}]"

            return list_representation

        elif isinstance(value, str):
            if quote_string:
                return f"'{value}'"
            else:
                return value
        elif isinstance(value, bool):
            # return value
            if quote_string:
                return f"'{value}'"
            else:
                return value
        elif isinstance(value, int) or isinstance(value, float):
            return str(value)
        elif isinstance(value, Filename):
            formatted = value.generated_filename()
            return formatted

        elif isinstance(value, StringFormatter):
            return cls.translate_string_formatter(
                value,
                in_shell_script=in_shell_script,
                tool=tool,
                inputs_dict=inputs_dict,
                skip_inputs_lookup=skip_inputs_lookup,
                **debugkwargs,
            )
        elif isinstance(value, InputSelector):
            if for_output:
                el = cls.prepare_filename_replacements_for(
                    value, inputsdict=inputs_dict
                )
                return el
            return cls.translate_input_selector(
                selector=value,
                inputs_dict=inputs_dict,
                skip_inputs_lookup=False,
                in_shell_script=in_shell_script,
                tool=tool,
            )

        elif isinstance(value, AliasSelector):
            return cls.unwrap_expression(
                value.inner_selector,
                quote_string=quote_string,
                tool=tool,
                inputs_dict=inputs_dict,
                skip_inputs_lookup=skip_inputs_lookup,
                for_output=for_output,
                in_shell_script=in_shell_script,
                var_indicator=var_indicator,
                step_indicator=step_indicator,
            )

        elif isinstance(value, WildcardSelector):
            # raise Exception(
            #     f"A wildcard selector cannot be used as an argument value for '{debugkwargs}' {tool.id()}"
            # )
            return f"'{value.wildcard}'"
        elif isinstance(value, Operator):
            unwrap_expression_wrap = lambda exp: cls.unwrap_expression(
                exp,
                quote_string=quote_string,
                tool=tool,
                for_output=for_output,
                inputs_dict=inputs_dict,
                skip_inputs_lookup=skip_inputs_lookup,
                in_shell_script=in_shell_script,
                **debugkwargs,
            )

            return value.to_nextflow(unwrap_expression_wrap, *value.args)

        elif callable(getattr(value, "nextflow", None)):
            if var_indicator is not None and step_indicator is not None:
                return value.nextflow(
                    var_indicator=var_indicator, step_indicator=step_indicator
                )
            else:
                return value.nextflow()

        raise Exception(
            "Could not detect type %s to convert to input value" % type(value)
        )

    @classmethod
    def translate_string_formatter(
        cls,
        selector: StringFormatter,
        tool,
        in_shell_script=False,
        inputs_dict=None,
        skip_inputs_lookup=False,
        **debugkwargs,
    ):
        """
        Translate Janis StringFormatter data type to Nextflow

        :param selector:
        :type selector:
        :param tool:
        :type tool:
        :param in_shell_script:
        :type in_shell_script:
        :param inputs_dict:
        :type inputs_dict:
        :param skip_inputs_lookup:
        :type skip_inputs_lookup:
        :param debugkwargs:
        :type debugkwargs:
        :return:
        :rtype:
        """
        if len(selector.kwargs) == 0:
            return str(selector)

        kwargreplacements = {
            k: f"{cls.unwrap_expression(v, tool=tool, inputs_dict=inputs_dict, skip_inputs_lookup=skip_inputs_lookup, **debugkwargs)}"
            for k, v in selector.kwargs.items()
        }

        arg_val = selector._format
        for k in selector.kwargs:
            arg_val = arg_val.replace(f"{{{k}}}", f"${{{str(kwargreplacements[k])}}}")

        if in_shell_script:
            arg_val = arg_val.replace("\\", "\\\\")

        return arg_val

    @classmethod
    def prepare_filename_replacements_for(
        cls, inp: Optional[Selector], inputsdict: Optional[Dict[str, ToolInput]]
    ) -> Optional[str]:
        """
        Generate a string expression to represent a filename in Nextflow

        :param inp:
        :type inp:
        :param inputsdict:
        :type inputsdict:
        :return:
        :rtype:
        """
        if inp is None or not isinstance(inp, InputSelector):
            return None

        if not inputsdict:
            return f"${inp.input_to_select}.name"
            # raise Exception(
            #     f"Couldn't generate filename as an internal error occurred (inputsdict did not contain {inp.input_to_select})"
            # )

        if isinstance(inp, InputSelector):
            if inp.input_to_select not in inputsdict:
                raise Exception(
                    f"The InputSelector '{inp.input_to_select}' did not select a valid input"
                )

            tinp = inputsdict.get(inp.input_to_select)
            intype = tinp.intype

            if intype.is_base_type((File, Directory)):
                potential_extensions = (
                    intype.get_extensions() if intype.is_base_type(File) else None
                )

                base = f"{tinp.id()}"
                if intype.has_secondary_files():
                    base = f"{tinp.id()}[0]"

                if inp.remove_file_extension and potential_extensions:
                    base = f"{base}.simpleName"
                elif hasattr(tinp, "localise_file") and tinp.localise_file:
                    base = f"{base}.name"

            elif isinstance(intype, Filename):
                base = str(
                    cls.unwrap_expression(
                        intype.generated_filename(),
                        inputs_dict=inputsdict,
                        for_output=True,
                    )
                )
            elif (
                intype.is_array()
                and isinstance(intype.fundamental_type(), (File, Directory))
                and tinp.localise_file
            ):
                base = f"{tinp.id()}.map{{ el.name }}"
            else:
                base = f"{tinp.id()}"

            if intype.optional:
                default = "'generated'"
                if isinstance(intype, Filename):
                    default = base

                replacement = f"({inp.input_to_select} && {inp.input_to_select} != 'None' && {inp.input_to_select} != '' ? {inp.input_to_select} : {default})"
            else:
                replacement = f"{base}"

            # return f"\"${{{replacement}}}\""
            return replacement

    @classmethod
    def translate_input_selector(
        cls,
        selector: InputSelector,
        inputs_dict,
        tool,
        skip_inputs_lookup=False,
        in_shell_script=False,
    ):
        """
        Translate Janis InputSelector data type into Nextflow expressions

        :param selector:
        :type selector:
        :param inputs_dict:
        :type inputs_dict:
        :param tool:
        :type tool:
        :param skip_inputs_lookup:
        :type skip_inputs_lookup:
        :param in_shell_script:
        :type in_shell_script:
        :param for_output:
        :type for_output:
        :return:
        :rtype:
        """
        if tool.versioned_id() not in cls.INPUT_IN_SELECTORS:
            cls.INPUT_IN_SELECTORS[tool.versioned_id()] = set()

        cls.INPUT_IN_SELECTORS[tool.versioned_id()].add(selector.input_to_select)

        sel: str = selector.input_to_select
        if not sel:
            raise Exception(
                "No input was selected for input selector: " + str(selector)
            )

        skip_lookup = skip_inputs_lookup or sel.startswith("runtime_")

        if not skip_lookup:

            if inputs_dict is None:
                raise Exception(
                    f"An internal error occurred when translating input selector '{sel}': the inputs dictionary was None"
                )
            if selector.input_to_select not in inputs_dict:
                raise Exception(
                    f"Couldn't find the input '{sel}' for the InputSelector(\"{sel}\")"
                )

            tinp: ToolInput = inputs_dict[selector.input_to_select]

            intype = tinp.intype

            if intype.is_base_type((File, Directory)):
                if intype.has_secondary_files():
                    sel = f"{sel}[0]"

            if selector.remove_file_extension:
                if intype.is_base_type((File, Directory)):

                    potential_extensions = (
                        intype.get_extensions() if intype.is_base_type(File) else None
                    )
                    if selector.remove_file_extension and potential_extensions:
                        sel = f"{sel}.simpleName"

                elif intype.is_array() and isinstance(
                    intype.fundamental_type(), (File, Directory)
                ):
                    inner_type = intype.fundamental_type()
                    extensions = (
                        inner_type.get_extensions()
                        if isinstance(inner_type, File)
                        else None
                    )

                    inner_sel = f"el.basename"
                    if extensions:
                        for ext in extensions:
                            inner_sel += f'.replace(/{ext}$/, "")'
                    sel = f"{sel}.map(function(el) {{ return {inner_sel}; }})"
                else:
                    Logger.warn(
                        f"InputSelector {sel} is requesting to remove_file_extension but it has type {tinp.input_type.id()}"
                    )

        if in_shell_script:
            sel = f"${{{sel}}}"

        return sel

    @classmethod
    def build_inputs_file(
        cls,
        tool,
        recursive=False,
        merge_resources=False,
        hints=None,
        additional_inputs: Dict = None,
        max_cores=None,
        max_mem=None,
        max_duration=None,
    ) -> Dict[str, any]:
        """
        Generate a dictionary containing input name and its values from users or
        its default values if inputs not provided.

        :param tool:
        :type tool:
        :param recursive:
        :type recursive:
        :param merge_resources:
        :type merge_resources:
        :param hints:
        :type hints:
        :param additional_inputs:
        :type additional_inputs:
        :param max_cores:
        :type max_cores:
        :param max_mem:
        :type max_mem:
        :param max_duration:
        :type max_duration:
        :return:
        :rtype:
        """

        ad = additional_inputs or {}
        values_provided_from_tool = {i.id(): i.default for i in tool.tool_inputs()}

        count = 0
        inp = {}

        for i in tool.tool_inputs():
            val = ad.get(i.id(), values_provided_from_tool.get(i.id()))

            if val is None:
                if isinstance(i.intype, (File, Directory)) or (
                    isinstance(i.intype, (Array))
                    and isinstance(i.intype.subtype(), (File, Directory))
                ):
                    count += 1
                    val = f"/{cls.NO_FILE_PATH_PREFIX}{count}"
                else:
                    val = ""
            else:
                if isinstance(i.intype, Boolean):
                    val = ad.get(i.tag, values_provided_from_tool.get(i.tag)) or ""
                    if val == "True":
                        val = True
                    if val == "False" or val == "":
                        val = False
                elif isinstance(i.intype, File):

                    if i.intype.has_secondary_files():
                        primary_file = val
                        secondary_files = []
                        for suffix in i.intype.secondary_files():
                            sec_file = apply_secondary_file_format_to_filename(
                                primary_file, suffix
                            )
                            secondary_files.append(sec_file)

                        # Note: we want primary file to always be the first item in the array
                        val = [primary_file] + secondary_files

            inp[i.id()] = val

        if merge_resources:
            for k, v in cls.build_resources_input(
                tool,
                hints,
                max_cores=max_cores,
                max_mem=max_mem,
                max_duration=max_duration,
            ).items():
                inp[k] = ad.get(k, v)

        return inp

    @staticmethod
    def stringify_translated_workflow(wf):
        return wf

    @staticmethod
    def stringify_translated_tool(tool):
        return tool

    @staticmethod
    def stringify_translated_inputs(inputs):
        """
        convert dictionary inputs to string

        :param inputs:
        :type inputs:
        :return:
        :rtype:
        """
        formatted = {}
        for key in inputs:
            # We want list to be formatted as ["xxx", "yyy"] instead of "['xxx', 'yyy']"
            if inputs[key] is not None:
                if (
                    type(inputs[key]) is list
                    or type(inputs[key]) is int
                    or type(inputs[key]) is float
                ):
                    val = inputs[key]
                else:
                    val = str(inputs[key])
            else:
                val = ""

            formatted[key] = val

        return json.dumps(formatted, indent=2)

    @staticmethod
    def workflow_filename(workflow):
        """
        Generate the main workflow filename

        :param workflow:
        :type workflow:
        :return:
        :rtype:
        """
        return workflow.versioned_id() + ".nf"

    @staticmethod
    def inputs_filename(workflow):
        """
        Generate the input filename

        :param workflow:
        :type workflow:
        :return:
        :rtype:
        """
        return workflow.versioned_id() + ".input.json"

    @staticmethod
    def tool_filename(tool):
        prefix = tool
        if isinstance(tool, Tool):
            prefix = tool.versioned_id()

        return prefix + ".nf"

    @staticmethod
    def resources_filename(workflow):
        """
        Generate resoureces filename

        :param workflow:
        :type workflow:
        :return:
        :rtype:
        """
        return workflow.id() + "-resources.json"

    @staticmethod
    def validate_command_for(wfpath, inppath, tools_dir_path, tools_zip_path):
        pass

    @classmethod
    def prepare_script_for_python_code_tool(cls, tool: CodeTool, inputs) -> str:
        """
        Generate the content of the script section in a Nextflow process for Janis python code tool

        :param tool:
        :type tool:
        :param inputs:
        :type inputs:
        :return:
        :rtype:
        """
        PYTHON_SHEBANG = "#!/usr/bin/env python"
        python_script_filename = f"{tool.versioned_id()}"

        # TODO: handle args of type list of string (need to quote them)
        all_args = []
        for i in inputs:
            arg_value = f"${i.tag}"
            if isinstance(i.intype, Array):
                arg_value = f'"{arg_value}".split(" ")'
            elif isinstance(i.intype, File) and i.intype.has_secondary_files():
                arg_value = f'"{arg_value}".split(" ")[0]'
            elif not isinstance(i.intype, (Array, Int, Float, Double)):
                arg_value = f'"{arg_value}"'

            arg_value = f"{i.tag}={arg_value}"

            all_args.append(arg_value)

        args = ", ".join(a for a in all_args)

        script = f"""{PYTHON_SHEBANG}
from {python_script_filename} import code_block
import os
import json

result = code_block({args})

work_dir = os.getenv("PYENV_DIR")
for key in result:
    with open(os.path.join("$workDir", f"{cls.PYTHON_CODE_OUTPUT_FILENAME_PREFIX}{{key}}"), "w") as f:
        f.write(json.dumps(result[key]))
"""

        return script

    @classmethod
    def prepare_script_for_command_tool(
        cls, process_name: str, tool: CommandTool, inputs
    ):
        """
        Generate the script content of a Nextflow process for Janis command line tool

        :param process_name:
        :type process_name:
        :param tool:
        :type tool:
        :param inputs:
        :type inputs:
        :return:
        :rtype:
        """
        bc = tool.base_command()
        pargs = []

        if bc:
            pargs.append(" ".join(bc) if isinstance(bc, list) else str(bc))

        arguments = []
        if isinstance(tool, CommandTool):
            arguments = tool.arguments() or []

        args = [a for a in arguments if a.position is not None or a.prefix is not None]
        args += [a for a in inputs if a.position is not None or a.prefix is not None]

        args = sorted(args, key=lambda a: (a.prefix is None))
        args = sorted(args, key=lambda a: (a.position or 0))

        inputsdict = tool.inputs_map()
        for a in args:
            if isinstance(a, ToolInput):
                pargs.append(f"${a.id()}WithPrefix")
            elif isinstance(a, ToolArgument):

                expression = cls.unwrap_expression(
                    a.value,
                    inputs_dict=inputsdict,
                    tool=tool,
                    skip_inputs_lookup=True,
                    quote_string=False,
                    in_shell_script=True,
                )

                if a.prefix is not None:
                    space = ""
                    if a.separate_value_from_prefix is not False:
                        space = " "

                    cmd_arg = f'{a.prefix}{space}"{expression}"'
                else:
                    cmd_arg = expression

                pargs.append(cmd_arg)
            else:
                raise Exception("unknown input type")

        main_script = " \\\n".join(pargs)

        pre_script = ""
        for dir in tool.directories_to_create() or []:
            unwrapped_dir = cls.unwrap_expression(
                dir, inputs_dict=inputsdict, tool=tool, in_shell_script=True
            )
            pre_script += f"mkdir -p '{unwrapped_dir}'"

        return f"""
{pre_script}

{main_script} | tee {cls.TOOL_STDOUT_FILENAME}_{process_name}

"""

    @classmethod
    def prepare_tool_output(cls, tool: Tool) -> Dict[str, str]:
        """
        Generate a dictionary that contains Nextflow expressions to represent Janis outputs

        :param tool:
        :type tool:
        :return:
        :rtype:
        """
        outputs = {}
        for out in tool.outputs():
            if isinstance(out, TOutput):
                output_type = out.outtype
            elif isinstance(out, ToolOutput):
                output_type = out.output_type

            val = f"{tool.id()}{out.tag}"

            if (
                output_type.is_array()
                and isinstance(output_type.subtype(), File)
                and output_type.subtype().has_secondary_files()
            ):
                val = f"{val}.map{{ item -> item[0] }}"
            elif isinstance(output_type, File) and output_type.has_secondary_files():
                val = f"{val}[0]"

            outputs[out.tag] = f"${{{val}}}"

        return outputs

    @classmethod
    def prepare_expression_inputs(cls, tool, inputs) -> str:
        """
        Generate Groovy code to represent the values of input variable definitions for complex expressions

        :param tool:
        :type tool:
        :param inputs:
        :type inputs:
        :return:
        :rtype:
        """

        inputsdict = tool.inputs_map()

        script_lines = []
        for i in inputs:
            if hasattr(i, "input_type"):
                input_type = i.input_type
            elif hasattr(i, "intype"):
                input_type = i.intype
            else:
                raise Exception("Failed to get input type attribute")

            if isinstance(input_type, Filename):
                val = cls.unwrap_expression(
                    input_type.generated_filename(), inputs_dict=inputsdict, tool=tool
                )

                if input_type.optional:
                    val = f"{i.id()} && {i.id()} != 'None' ? {i.id()} : {val}"

                code = f"""
def {i.id()} = {val}
"""
                script_lines.append(code)

        return "".join(script_lines)

    @classmethod
    def generate_input_var_definition(cls, inp: ToolInput, arg_name: str) -> str:
        """
        Generate Groovy code to represent the values of input variable definitions

        :param inp:
        :type inp:
        :param arg_name:
        :type arg_name:
        :return:
        :rtype:
        """
        if isinstance(inp.input_type, Array):
            if (
                isinstance(inp.input_type.subtype(), File)
                and inp.input_type.subtype().has_secondary_files()
            ):
                arg_value = f"get_primary_files({arg_name}).join(' ')"
            else:
                arg_value = f"{arg_name}.join(' ')"

        elif (
            isinstance(inp.input_type, (File)) and inp.input_type.has_secondary_files()
        ):
            arg_value = f"{arg_name}[0]"
        else:
            arg_value = arg_name

        prefix = ""
        if inp.prefix is not None:
            prefix = inp.prefix

        space = ""
        if inp.separate_value_from_prefix is not False:
            space = " "

        prefix_applies_to_all_elements = "False"
        if inp.prefix_applies_to_all_elements is True:
            prefix_applies_to_all_elements = "True"

        if isinstance(inp.input_type, Boolean):
            arg = f"boolean_flag({arg_value}, '{prefix}{space}')"
        else:
            if inp.input_type.optional:
                arg = f"optional({arg_value}, '{prefix}{space}', '{prefix_applies_to_all_elements}')"
            else:
                arg = f"apply_prefix({arg_value}, '{prefix}{space}', '{prefix_applies_to_all_elements}')"
                # arg = f"'{prefix}{space}' + {arg_value}"

        return arg

    @classmethod
    def prepare_input_vars(cls, inputs) -> str:
        """
        Generate Groovy code for input variables definitions inside the Nextflow script section.
        This is where we apply prefix or preprocessiong if necessary.

        :param inputs:
        :type inputs:
        :return:
        :rtype:
        """
        pre_script_lines = []
        for a in inputs:
            arg_name = ""
            if isinstance(a, ToolInput):
                arg_name = a.id()
            elif isinstance(a, ToolArgument):
                continue
            else:
                raise Exception("unknown input type")

            arg = cls.generate_input_var_definition(a, arg_name)

            code = f"""
def {arg_name}WithPrefix = {arg}
"""

            pre_script_lines.append(code)

        return "".join(pre_script_lines)

    @classmethod
    def prepare_resources_var(cls, tool, name: Optional[str] = None):
        """
        Generate Groovy code for resources variables definitions inside the Nextflow script section.

        :param tool:
        :type tool:
        :param name:
        :type name:
        :return:
        :rtype:
        """
        pre_script_lines = []
        var_names = []
        param_names = []
        for k, v in cls.build_resources_input(
            tool,
            hints=None,
        ).items():
            prefix = ""
            if name is not None:
                prefix = f"{name}_"

            param_name = f"params.{prefix}{k}"

            code = f"""
def {k} = {param_name}
"""
            var_names.append(k)
            param_names.append(param_name)
            pre_script_lines.append(code)

        return "".join(pre_script_lines), var_names, param_names

    @classmethod
    def prepare_inputs_in_selector(
        cls, tool, inputs: List[ToolInput], resources: List[str]
    ):
        """
        If there is any input being referenced by Janis InputSelector,
        we need to add their Groovy variable definitions

        :param tool:
        :type tool:
        :param inputs:
        :type inputs:
        :param resources:
        :type resources:
        :return:
        :rtype:
        """
        pre_script_lines = []

        if tool.versioned_id() not in cls.INPUT_IN_SELECTORS:
            return ""

        input_keys = [i.id() for i in inputs]

        for k in cls.INPUT_IN_SELECTORS[tool.versioned_id()]:
            if k not in input_keys and k not in resources:
                val = "''"

                code = f"""
def {k} =  {val}
"""
                pre_script_lines.append(code)

        return "".join(pre_script_lines)

    @classmethod
    def get_input_qualifier_for_inptype(
        cls, inp_type: DataType
    ) -> nfgen.InputProcessQualifier:
        """
        Get Nextflow input qualifier based on Janis data type

        :param inp_type:
        :type inp_type:
        :return:
        :rtype:
        """

        if isinstance(inp_type, Array):
            inp_type = inp_type.fundamental_type()

        if isinstance(inp_type, (File, Directory)):
            return nfgen.InputProcessQualifier.path

        # Handle UnionType
        if inp_type.is_base_type(File) or inp_type.is_base_type(Directory):
            return nfgen.InputProcessQualifier.path

        return nfgen.InputProcessQualifier.val

    @classmethod
    def get_output_qualifier_for_outtype(
        cls,
        out_type: DataType,
    ) -> nfgen.OutputProcessQualifier:
        """
        Generate Nextflow output qualifier based on Janis output data type

        :param out_type:
        :type out_type:
        :return:
        :rtype:
        """
        if isinstance(out_type, Array):
            return nfgen.OutputProcessQualifier.tuple

        # elif isinstance(out_type, Stdout):
        #     return nfgen.OutputProcessQualifier.stdout

        elif isinstance(out_type, (File, Directory, Stdout)):
            return nfgen.OutputProcessQualifier.path

        return nfgen.OutputProcessQualifier.val
