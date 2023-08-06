"""Schema definitions for BARRIER jobs"""

from typing import Literal

from pydantic import conlist, confloat

from .... import job as job_schema
from . import shared as shared_schema


class BarrierInputValues(job_schema.InputValues):
    end_time_ms: confloat(ge=80.0, le=80.0)
    optical_barriers: conlist(shared_schema.Barrier, min_items=1, max_items=5)
    rf_evaporation: shared_schema.RfEvaporation
    optical_landscape: None
    lasers: None


class BarrierCreateInput(job_schema.InputWithoutOutput):
    values: BarrierInputValues
    output: None


class BarrierCompleteInput(job_schema.Input):
    values: BarrierInputValues
    output: job_schema.BarrierOutput


class BarrierCreateJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.BARRIER] = job_schema.JobType.BARRIER
    inputs: conlist(BarrierCreateInput, min_items=1, max_items=1)


class BarrierCompleteJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.BARRIER] = job_schema.JobType.BARRIER
    inputs: conlist(BarrierCompleteInput, min_items=1, max_items=1)


class BarrierCreateBatchJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.BARRIER] = job_schema.JobType.BARRIER
    inputs: conlist(BarrierCreateInput, min_items=2, max_items=30)


class BarrierCompleteBatchJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.BARRIER] = job_schema.JobType.BARRIER
    inputs: conlist(BarrierCompleteInput, min_items=2, max_items=30)


class BarrierCreateJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.BARRIER] = job_schema.JobType.BARRIER
    inputs: conlist(BarrierCreateInput, min_items=1, max_items=1)


class BarrierCompleteJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.BARRIER] = job_schema.JobType.BARRIER
    inputs: conlist(BarrierCompleteInput, min_items=1, max_items=1)


class BarrierCreateBatchJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.BARRIER] = job_schema.JobType.BARRIER
    inputs: conlist(BarrierCreateInput, min_items=2, max_items=30)


class BarrierCompleteBatchJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.BARRIER] = job_schema.JobType.BARRIER
    inputs: conlist(BarrierCompleteInput, min_items=2, max_items=30)
