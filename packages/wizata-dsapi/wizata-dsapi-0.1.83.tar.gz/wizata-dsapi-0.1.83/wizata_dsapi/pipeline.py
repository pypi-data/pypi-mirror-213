import uuid
import json

from .api_dto import ApiDto
from .script import ScriptConfig

from enum import Enum


class StepType(Enum):
    QUERY = 'query'
    SCRIPT = 'script'
    MODEL = 'model'


class PipelineStep(ApiDto):
    """
    Step of a pipeline.
    """

    def __init__(self,
                 step_id: uuid.UUID = None,
                 step_type: StepType = None,
                 config=None,
                 inputs=None,
                 outputs=None):

        if outputs is None:
            outputs = []
        if step_id is None:
            step_id = uuid.uuid4()
        self.step_id = step_id
        self.step_type = step_type
        self.config = config
        self.inputs = inputs
        self.outputs = outputs

    def from_json(self, obj):
        """
        load from JSON dictionary representation
        """
        if "id" in obj.keys():
            self.step_id = uuid.UUID(obj["id"])

        if "type" in obj.keys():
            if obj["type"] in ['query', 'script', 'model']:
                self.step_type = StepType(obj["type"])
            else:
                raise TypeError(f'unsupported step type {obj["type"]}')
        else:
            raise TypeError(f'pipeline step must have a type.')
        if "config" in obj.keys():
            if self.step_type == StepType.SCRIPT:
                self.config = ScriptConfig()
                self.config.from_json(obj['config'])
            else:
                self.config = obj['config']
        self.inputs = []
        if "inputs" in obj.keys():
            for step_input in obj["inputs"]:
                if isinstance(step_input, dict):
                    self.inputs.append(step_input)
                else:
                    raise TypeError(f'unsupported input type {step_input.__class__.__name__}')

        self.outputs = []
        if "outputs" in obj.keys():
            for step_output in obj["outputs"]:
                if isinstance(step_output, dict):
                    self.outputs.append(step_output)
                else:
                    raise TypeError(f'unsupported output type {step_output.__class__.__name__}')

    def to_json(self):
        obj = {
            "id": str(self.step_id)
        }
        if self.step_type is not None:
            obj["type"] = str(self.step_type)
        if self.config is not None:
            obj["config"] = self.config
        if self.inputs is not None:
            obj["inputs"] = self.inputs
        if self.outputs is not None:
            obj["outputs"] = self.outputs
        return obj

    def inputs_names(self, f_type: str = None) -> list:
        """
        get a list str representing inputs names
        :param f_type: filter on a type
        :return: list str
        """
        names = []
        for d_key in self.inputs:
            if not isinstance(d_key, dict):
                raise TypeError(f'unsupported output type {d_key} expected dataframe or model')
            if "dataframe" in d_key.keys() and (f_type is None or f_type == 'dataframe'):
                names.append(d_key["dataframe"])
            elif "model" in d_key.keys() and (f_type is None or f_type == 'model'):
                names.append(d_key["model"])
            elif f_type is None:
                raise TypeError(f'unsupported input type {d_key} expected dataframe or model')
        return names

    def outputs_names(self, f_type: str = None) -> list:
        """
        get a list str representing outputs names
        :param f_type: filter on a type
        :return: list str
        """
        names = []
        for d_key in self.outputs:
            if not isinstance(d_key, dict):
                raise TypeError(f'unsupported output type {d_key} expected dataframe or model')
            elif "dataframe" in d_key.keys() and (f_type is None or f_type == 'dataframe'):
                names.append(d_key["dataframe"])
            elif "model" in d_key.keys() and (f_type is None or f_type == 'model'):
                names.append(d_key["model"])
            elif f_type is None:
                raise TypeError(f'unsupported output type {d_key} expected dataframe or model')
        return names

    def get_input(self, name: str) -> dict:
        """
        get input dict based on value name.
        :param name: value name to find.
        :return: input dict
        """
        for d_input in self.inputs:
            if name in d_input.values():
                return d_input

    def get_output(self, name: str) -> dict:
        """
        get output dict based on value name.
        :param name: value name to find.
        :return: input dict
        """
        for d_output in self.outputs:
            if name in d_output.values():
                return d_output


class Pipeline(ApiDto):

    def __init__(self,
                 pipeline_id: uuid.UUID = None,
                 key: str = None,
                 variables: list = None,
                 steps: list = None,
                 plots: list = None,
                 template_id: uuid.UUID = None):

        if pipeline_id is None:
            pipeline_id = uuid.uuid4()
        self.pipeline_id = pipeline_id
        self.key = key
        self.variables = variables
        self.template_id = template_id
        self.plots = plots
        if plots is None:
            self.plots = []
        if steps is not None:
            for step in steps:
                if not isinstance(step, PipelineStep):
                    raise TypeError(f'step expected PipelineStep but received {step.__class__.__name__}')
            self.steps = steps
        else:
            self.steps = []

    def check_path(self) -> bool:
        """
        validate that steps create a valid path.
        return true if path is valid, otherwise raise errors
        """

        followed = []  # all steps already followed
        produced = []  # all outputs already produced

        steps_to_follow = self._next_steps(followed, produced)
        if len(steps_to_follow) == 0:
            raise ValueError('path does not contains any initial steps producing outputs')

        while len(steps_to_follow) > 0:
            for step in steps_to_follow:
                self._follow_step(step, followed, produced)
            steps_to_follow = []
            if len(followed) < len(self.steps):
                steps_to_follow = self._next_steps(followed, produced)

        if len(followed) == len(self.steps):
            return True
        else:
            raise RuntimeError(f'missing {len(self.steps)-len(followed)} step(s) that could not be followed')

    def _follow_step(self,
                     step: PipelineStep,
                     followed: list,
                     produced: list):
        """
        simulate that step have been followed.
        """
        if step in followed:
            raise RuntimeError(f'path cannot pass two times through same step {step.step_id}')
        followed.append(step)
        for output in step.outputs_names():
            if step.step_type == StepType.QUERY and len(step.outputs) != 1:
                raise RuntimeError(f'query step must have exactly one output and be of type dataframe')
            if output in produced:
                raise RuntimeError(f'output {output} is already produced.')
            produced.append(output)

    def _next_steps(self, followed, produced):
        """
        find all next steps that are ready to be executed
        """
        next_steps = []
        step: PipelineStep
        for step in self.steps:
            if all(s_input in produced for s_input in step.inputs_names()) and step not in followed:
                next_steps.append(step)
        return next_steps

    def api_id(self) -> str:
        """
        Id of the pipeline

        :return: string formatted UUID of the Pipeline.
        """
        return str(self.pipeline_id).upper()

    def endpoint(self) -> str:
        """
        Name of the endpoints used to manipulate pipeline.
        :return: Endpoint name.
        """
        return "Pipelines"

    def from_json(self, obj):
        """
        load from JSON dictionary representation
        """
        if "id" in obj.keys():
            self.pipeline_id = uuid.UUID(obj["id"])
        if "key" in obj.keys():
            self.key = str(obj['key'])
        if "id" not in obj.keys() and "key" not in obj.keys():
            raise KeyError("at least id or key must be set on a pipeline")
        if "templateId" in obj.keys() and obj["templateId"] is not None:
            self.template_id = uuid.UUID(obj["templateId"])
        if "variables" in obj.keys():
            if isinstance(obj["variables"], str):
                self.variables = json.loads(obj["variables"])
            else:
                self.variables = obj["variables"]
        if "steps" in obj.keys():
            if isinstance(obj["steps"], str):
                steps = json.loads(obj["steps"])
            else:
                steps = obj["steps"]
            for obj_step in steps:
                step = PipelineStep()
                step.from_json(obj_step)
                self.steps.append(step)
        if "plots" in obj.keys():
            if isinstance(obj["plots"], str):
                self.plots = json.loads(obj["plots"])
            else:
                self.plots = obj["plots"]

    def to_json(self):
        """
        Convert to a json version of Execution definition.
        By default, use DS API format.
        """
        obj = {
            "id": str(self.pipeline_id)
        }
        if self.key is not None:
            obj["key"] = self.key
        if self.steps is not None:
            obj_steps = []
            step: PipelineStep
            for step in self.steps:
                obj_steps.append(step.to_json())
            obj["steps"] = json.dumps(obj_steps)
        if self.plots is not None:
            obj["plots"] = json.dumps(self.plots)
        if self.variables is not None:
            obj["variables"] = json.dumps(self.variables)
        if self.template_id is not None:
            obj["templateId"] = str(self.template_id)
        return obj




