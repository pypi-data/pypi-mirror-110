# Copyright 2019 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from typing import Dict, List, Optional, Sequence, Set, TYPE_CHECKING, Union

import cirq
from cirq_google.engine.client import quantum
from cirq_google.engine.client.quantum import types as qtypes
from cirq_google.engine.result_type import ResultType
from cirq_google import gate_sets
from cirq_google.api import v2
from cirq_google.engine import engine_job

if TYPE_CHECKING:
    import cirq_google.engine.engine as engine_base


class EngineProgram:
    """A program created via the Quantum Engine API.

    This program wraps a Circuit with additional metadata used to
    schedule against the devices managed by Quantum Engine.

    Attributes:
        project_id: A project_id of the parent Google Cloud Project.
        program_id: Unique ID of the program within the parent project.
    """

    def __init__(
        self,
        project_id: str,
        program_id: str,
        context: 'engine_base.EngineContext',
        _program: Optional[qtypes.QuantumProgram] = None,
        result_type: ResultType = ResultType.Program,
    ) -> None:
        """A job submitted to the engine.

        Args:
            project_id: A project_id of the parent Google Cloud Project.
            program_id: Unique ID of the program within the parent project.
            context: Engine configuration and context to use.
            _program: The optional current program state.
            result_type: The type of program that was created.
        """
        self.project_id = project_id
        self.program_id = program_id
        self.context = context
        self._program = _program
        self.result_type = result_type

    def run_sweep(
        self,
        job_id: Optional[str] = None,
        params: cirq.Sweepable = None,
        repetitions: int = 1,
        processor_ids: Sequence[str] = ('xmonsim',),
        description: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> engine_job.EngineJob:
        """Runs the program on the QuantumEngine.

        In contrast to run, this runs across multiple parameter sweeps, and
        does not block until a result is returned.

        Args:
            job_id: Optional job id to use. If this is not provided, a random id
                of the format 'job-################YYMMDD' will be generated,
                where # is alphanumeric and YYMMDD is the current year, month,
                and day.
            params: Parameters to run with the program.
            repetitions: The number of circuit repetitions to run.
            processor_ids: The engine processors that should be candidates
                to run the program. Only one of these will be scheduled for
                execution.
            description: An optional description to set on the job.
            labels: Optional set of labels to set on the job.

        Returns:
            An EngineJob. If this is iterated over it returns a list of
            TrialResults, one for each parameter sweep.
        """
        import cirq_google.engine.engine as engine_base

        if self.result_type != ResultType.Program:
            raise ValueError('Please use run_batch() for batch mode.')
        if not job_id:
            job_id = engine_base._make_random_id('job-')
        sweeps = cirq.to_sweeps(params or cirq.ParamResolver({}))
        run_context = self._serialize_run_context(sweeps, repetitions)

        created_job_id, job = self.context.client.create_job(
            project_id=self.project_id,
            program_id=self.program_id,
            job_id=job_id,
            processor_ids=processor_ids,
            run_context=run_context,
            description=description,
            labels=labels,
        )
        return engine_job.EngineJob(
            self.project_id, self.program_id, created_job_id, self.context, job
        )

    def run_batch(
        self,
        job_id: Optional[str] = None,
        params_list: List[cirq.Sweepable] = None,
        repetitions: int = 1,
        processor_ids: Sequence[str] = (),
        description: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> engine_job.EngineJob:
        """Runs a batch of circuits on the QuantumEngine.

        This method should only be used if the Program object was created
        with a BatchProgram.  The number of parameter sweeps should match
        the number of circuits within that BatchProgram.

        This method does not block until a result is returned.  However,
        no results will be available until the entire batch is complete.

        Args:
            job_id: Optional job id to use. If this is not provided, a random id
                of the format 'job-################YYMMDD' will be generated,
                where # is alphanumeric and YYMMDD is the current year, month,
                and day.
            params_list: Parameter sweeps to run with the program.  There must
                be one Sweepable object for each circuit in the batch. If this
                is None, it is assumed that the circuits are not parameterized
                and do not require sweeps.
            repetitions: The number of circuit repetitions to run.
            processor_ids: The engine processors that should be candidates
                to run the program. Only one of these will be scheduled for
                execution.
            description: An optional description to set on the job.
            labels: Optional set of labels to set on the job.

        Returns:
            An EngineJob. If this is iterated over it returns a list of
            TrialResults. All TrialResults for the first circuit are listed
            first, then the TrialResults for the second, etc. The TrialResults
            for a circuit are listed in the order imposed by the associated
            parameter sweep.

        Raises:
            ValueError: if the program was not a batch program or no processors
                were supplied.
        """
        import cirq_google.engine.engine as engine_base

        if self.result_type != ResultType.Batch:
            raise ValueError('Can only use run_batch() in batch mode.')
        if params_list is None:
            params_list = [None] * self.batch_size()
        if not job_id:
            job_id = engine_base._make_random_id('job-')
        if not processor_ids:
            raise ValueError('No processors specified')

        # Pack the run contexts into batches
        batch = v2.batch_pb2.BatchRunContext()
        for param in params_list:
            sweeps = cirq.to_sweeps(param)
            current_context = batch.run_contexts.add()
            for sweep in sweeps:
                sweep_proto = current_context.parameter_sweeps.add()
                sweep_proto.repetitions = repetitions
                v2.sweep_to_proto(sweep, out=sweep_proto.sweep)
        batch_context = qtypes.any_pb2.Any()
        batch_context.Pack(batch)

        created_job_id, job = self.context.client.create_job(
            project_id=self.project_id,
            program_id=self.program_id,
            job_id=job_id,
            processor_ids=processor_ids,
            run_context=batch_context,
            description=description,
            labels=labels,
        )
        return engine_job.EngineJob(
            self.project_id,
            self.program_id,
            created_job_id,
            self.context,
            job,
            result_type=ResultType.Batch,
        )

    def run_calibration(
        self,
        job_id: Optional[str] = None,
        processor_ids: Sequence[str] = (),
        description: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> engine_job.EngineJob:
        """Runs layers of calibration routines on the Quantum Engine.

        This method should only be used if the Program object was created
        with a `FocusedCalibration`.

        This method does not block until a result is returned.  However,
        no results will be available until all calibration routines complete.

        Args:
            job_id: Optional job id to use. If this is not provided, a random id
                of the format 'calibration-################YYMMDD' will be
                generated, where # is alphanumeric and YYMMDD is the current
                year, month, and day.
            processor_ids: The engine processors that should be candidates
                to run the program. Only one of these will be scheduled for
                execution.
            description: An optional description to set on the job.
            labels: Optional set of labels to set on the job.

        Returns:
            An EngineJob.  Results can be accessed with calibration_results().
        """
        import cirq_google.engine.engine as engine_base

        if not job_id:
            job_id = engine_base._make_random_id('calibration-')
        if not processor_ids:
            raise ValueError('No processors specified')

        # Default run context
        # Note that Quantum Engine currently requires a valid type url
        # on a run context in order to succeed validation.
        any_context = qtypes.any_pb2.Any()
        any_context.Pack(v2.run_context_pb2.RunContext())

        created_job_id, job = self.context.client.create_job(
            project_id=self.project_id,
            program_id=self.program_id,
            job_id=job_id,
            processor_ids=processor_ids,
            run_context=any_context,
            description=description,
            labels=labels,
        )
        return engine_job.EngineJob(
            self.project_id,
            self.program_id,
            created_job_id,
            self.context,
            job,
            result_type=ResultType.Batch,
        )

    def run(
        self,
        job_id: Optional[str] = None,
        param_resolver: cirq.ParamResolver = cirq.ParamResolver({}),
        repetitions: int = 1,
        processor_ids: Sequence[str] = ('xmonsim',),
        description: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> cirq.Result:
        """Runs the supplied Circuit via Quantum Engine.

        Args:
            job_id: Optional job id to use. If this is not provided, a random id
                of the format 'job-################YYMMDD' will be generated,
                where # is alphanumeric and YYMMDD is the current year, month,
                and day.
            param_resolver: Parameters to run with the program.
            repetitions: The number of repetitions to simulate.
            processor_ids: The engine processors that should be candidates
                to run the program. Only one of these will be scheduled for
                execution.
            description: An optional description to set on the job.
            labels: Optional set of labels to set on the job.

        Returns:
            A single Result for this run.
        """
        return list(
            self.run_sweep(
                job_id=job_id,
                params=[param_resolver],
                repetitions=repetitions,
                processor_ids=processor_ids,
                description=description,
                labels=labels,
            )
        )[0]

    def _serialize_run_context(
        self,
        sweeps: List[cirq.Sweep],
        repetitions: int,
    ) -> qtypes.any_pb2.Any:
        import cirq_google.engine.engine as engine_base

        context = qtypes.any_pb2.Any()
        proto_version = self.context.proto_version
        if proto_version == engine_base.ProtoVersion.V2:
            run_context = v2.run_context_pb2.RunContext()
            for sweep in sweeps:
                sweep_proto = run_context.parameter_sweeps.add()
                sweep_proto.repetitions = repetitions
                v2.sweep_to_proto(sweep, out=sweep_proto.sweep)

            context.Pack(run_context)
        else:
            raise ValueError(f'invalid run context proto version: {proto_version}')
        return context

    def engine(self) -> 'engine_base.Engine':
        """Returns the parent Engine object.

        Returns:
            The program's parent Engine.
        """
        import cirq_google.engine.engine as engine_base

        return engine_base.Engine(self.project_id, context=self.context)

    def get_job(self, job_id: str) -> engine_job.EngineJob:
        """Returns an EngineJob for an existing Quantum Engine job.

        Args:
            job_id: Unique ID of the job within the parent program.

        Returns:
            A EngineJob for the job.
        """
        return engine_job.EngineJob(self.project_id, self.program_id, job_id, self.context)

    def list_jobs(
        self,
        created_before: Optional[Union[datetime.datetime, datetime.date]] = None,
        created_after: Optional[Union[datetime.datetime, datetime.date]] = None,
        has_labels: Optional[Dict[str, str]] = None,
        execution_states: Optional[Set[quantum.enums.ExecutionStatus.State]] = None,
    ):
        """Returns the list of jobs for this program.

        Args:
            project_id: A project_id of the parent Google Cloud Project.
            program_id: Unique ID of the program within the parent project.
            created_after: retrieve jobs that were created after this date
                or time.
            created_before: retrieve jobs that were created after this date
                or time.
            has_labels: retrieve jobs that have labels on them specified by
                this dict. If the value is set to `*`, filters having the label
                regardless of the label value will be filtered. For example, to
                query programs that have the shape label and have the color
                label with value red can be queried using

                {'color': 'red', 'shape':'*'}

            execution_states: retrieve jobs that have an execution state  that
                is contained in `execution_states`. See
                `quantum.enums.ExecutionStatus.State` enum for accepted values.
        """
        client = self.context.client
        response = client.list_jobs(
            self.project_id,
            self.program_id,
            created_before=created_before,
            created_after=created_after,
            has_labels=has_labels,
            execution_states=execution_states,
        )
        return [
            engine_job.EngineJob(
                project_id=client._ids_from_job_name(j.name)[0],
                program_id=client._ids_from_job_name(j.name)[1],
                job_id=client._ids_from_job_name(j.name)[2],
                context=self.context,
                _job=j,
            )
            for j in response
        ]

    def _inner_program(self) -> qtypes.QuantumProgram:
        if not self._program:
            self._program = self.context.client.get_program(self.project_id, self.program_id, False)
        return self._program

    def create_time(self) -> 'datetime.datetime':
        """Returns when the program was created."""
        return self._inner_program().create_time.ToDatetime()

    def update_time(self) -> 'datetime.datetime':
        """Returns when the program was last updated."""
        self._program = self.context.client.get_program(self.project_id, self.program_id, False)
        return self._program.update_time.ToDatetime()

    def description(self) -> str:
        """Returns the description of the program."""
        return self._inner_program().description

    def set_description(self, description: str) -> 'EngineProgram':
        """Sets the description of the program.

        Params:
            description: The new description for the program.

        Returns:
             This EngineProgram.
        """
        self._program = self.context.client.set_program_description(
            self.project_id, self.program_id, description
        )
        return self

    def labels(self) -> Dict[str, str]:
        """Returns the labels of the program."""
        return self._inner_program().labels

    def set_labels(self, labels: Dict[str, str]) -> 'EngineProgram':
        """Sets (overwriting) the labels for a previously created quantum
        program.

        Params:
            labels: The entire set of new program labels.

        Returns:
             This EngineProgram.
        """
        self._program = self.context.client.set_program_labels(
            self.project_id, self.program_id, labels
        )
        return self

    def add_labels(self, labels: Dict[str, str]) -> 'EngineProgram':
        """Adds new labels to a previously created quantum program.

        Params:
            labels: New labels to add to the existing program labels.

        Returns:
             This EngineProgram.
        """
        self._program = self.context.client.add_program_labels(
            self.project_id, self.program_id, labels
        )
        return self

    def remove_labels(self, keys: List[str]) -> 'EngineProgram':
        """Removes labels with given keys from the labels of a previously
        created quantum program.

        Params:
            label_keys: Label keys to remove from the existing program labels.

        Returns:
             This EngineProgram.
        """
        self._program = self.context.client.remove_program_labels(
            self.project_id, self.program_id, keys
        )
        return self

    def get_circuit(self, program_num: Optional[int] = None) -> cirq.Circuit:
        """Returns the cirq Circuit for the Quantum Engine program. This is only
        supported if the program was created with the V2 protos.

        Args:
            program_num: if this is a batch program, the index of the circuit in
                the batch.  This argument is zero-indexed. Negative values
                indexing from the end of the list.

        Returns:
            The program's cirq Circuit.
        """
        if not self._program or not self._program.HasField('code'):
            self._program = self.context.client.get_program(self.project_id, self.program_id, True)
        return self._deserialize_program(self._program.code, program_num)

    def batch_size(self) -> int:
        """Returns the number of programs in a batch program.

        Raises:
            ValueError: if the program created was not a batch program.
        """
        if self.result_type != ResultType.Batch:
            raise ValueError(
                f'Program was not a batch program but instead was of type {self.result_type}.'
            )
        import cirq_google.engine.engine as engine_base

        if not self._program or not self._program.HasField('code'):
            self._program = self.context.client.get_program(self.project_id, self.program_id, True)
        code = self._program.code
        code_type = code.type_url[len(engine_base.TYPE_PREFIX) :]
        if code_type == 'cirq.google.api.v2.BatchProgram':
            batch = v2.batch_pb2.BatchProgram.FromString(code.value)
            return len(batch.programs)
        raise ValueError(f'Program was not a batch program but instead was of type {code_type}.')

    @staticmethod
    def _deserialize_program(
        code: qtypes.any_pb2.Any, program_num: Optional[int] = None
    ) -> cirq.Circuit:
        import cirq_google.engine.engine as engine_base

        code_type = code.type_url[len(engine_base.TYPE_PREFIX) :]
        program = None
        if code_type == 'cirq.google.api.v1.Program' or code_type == 'cirq.api.google.v1.Program':
            raise ValueError('deserializing a v1 Program is not supported')
        elif code_type == 'cirq.google.api.v2.Program' or code_type == 'cirq.api.google.v2.Program':
            program = v2.program_pb2.Program.FromString(code.value)
        elif code_type == 'cirq.google.api.v2.BatchProgram':
            if program_num is None:
                raise ValueError(
                    'A program number must be specified when deserializing a Batch Program'
                )
            batch = v2.batch_pb2.BatchProgram.FromString(code.value)
            if abs(program_num) >= len(batch.programs):
                raise ValueError(
                    f'Only {len(batch.programs)} in the batch but '
                    f'index {program_num} was specified'
                )

            program = batch.programs[program_num]
        if program:
            gate_set_map = {g.gate_set_name: g for g in gate_sets.GOOGLE_GATESETS}
            if program.language.gate_set not in gate_set_map:
                raise ValueError(
                    f'Unknown gateset {program.language.gate_set}. '
                    f'Supported gatesets: {list(gate_set_map.keys())}.'
                )
            return gate_set_map[program.language.gate_set].deserialize(program)

        raise ValueError(f'unsupported program type: {code_type}')

    def delete(self, delete_jobs: bool = False) -> None:
        """Deletes a previously created quantum program.

        Params:
            delete_jobs: If True will delete all the program's jobs, other this
                will fail if the program contains any jobs.
        """
        self.context.client.delete_program(
            self.project_id, self.program_id, delete_jobs=delete_jobs
        )

    def __str__(self) -> str:
        return f'EngineProgram(project_id=\'{self.project_id}\', program_id=\'{self.program_id}\')'
