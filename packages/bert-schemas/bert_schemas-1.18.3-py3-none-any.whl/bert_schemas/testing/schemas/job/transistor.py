"""Schema definitions for TRANSISTOR jobs"""

from typing import Literal

from pydantic import conlist, confloat

from .... import job as job_schema
from . import shared as shared_schema


class TransistorInputValues(job_schema.InputValues):
    end_time_ms: confloat(ge=80.0, le=80.0)
    rf_evaporation: shared_schema.RfEvaporation
    optical_landscape: shared_schema.OpticalLandscape
    optical_barriers: conlist(shared_schema.Barrier, min_items=1, max_items=5)
    lasers: conlist(shared_schema.Laser, min_items=1, max_items=1)


class TransistorCreateInput(job_schema.InputWithoutOutput):
    values: TransistorInputValues
    output: None


class TransistorCompleteInput(job_schema.Input):
    values: TransistorInputValues
    output: job_schema.BarrierOutput


class TransistorCreateJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.TRANSISTOR] = job_schema.JobType.TRANSISTOR
    inputs: conlist(TransistorCreateInput, min_items=1, max_items=1)


class TransistorCompleteJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.TRANSISTOR] = job_schema.JobType.TRANSISTOR
    inputs: conlist(TransistorCompleteInput, min_items=1, max_items=1)


class TransistorCreateBatchJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.TRANSISTOR] = job_schema.JobType.TRANSISTOR
    inputs: conlist(TransistorCreateInput, min_items=2, max_items=30)


class TransistorCompleteBatchJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.TRANSISTOR] = job_schema.JobType.TRANSISTOR
    inputs: conlist(TransistorCompleteInput, min_items=2, max_items=30)


class TransistorCreateJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.TRANSISTOR] = job_schema.JobType.TRANSISTOR
    inputs: conlist(TransistorCreateInput, min_items=1, max_items=1)


class TransistorCompleteJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.TRANSISTOR] = job_schema.JobType.TRANSISTOR
    inputs: conlist(TransistorCompleteInput, min_items=1, max_items=1)


class TransistorCreateBatchJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.TRANSISTOR] = job_schema.JobType.TRANSISTOR
    inputs: conlist(TransistorCreateInput, min_items=2, max_items=30)


class TransistorCompleteBatchJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.TRANSISTOR] = job_schema.JobType.TRANSISTOR
    inputs: conlist(TransistorCompleteInput, min_items=2, max_items=30)
