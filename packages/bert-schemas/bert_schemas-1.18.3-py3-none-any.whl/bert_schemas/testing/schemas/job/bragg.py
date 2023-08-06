"""Schema definitions for BRAGG jobs"""

from typing import Literal

from pydantic import conlist, confloat

from .... import job as job_schema
from . import shared as shared_schema


class BraggInputValues(job_schema.InputValues):
    end_time_ms: confloat(ge=80.0, le=80.0)
    lasers: conlist(shared_schema.Laser, min_items=1, max_items=1)
    rf_evaporation: shared_schema.RfEvaporation
    optical_landscape: None
    optical_barriers: None


class BraggCreateInput(job_schema.InputWithoutOutput):
    values: BraggInputValues
    output: None


class BraggCompleteInput(job_schema.Input):
    values: BraggInputValues
    output: job_schema.BarrierOutput


class BraggCreateJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.BRAGG] = job_schema.JobType.BRAGG
    inputs: conlist(BraggCreateInput, min_items=1, max_items=1)


class BraggCompleteJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.BRAGG] = job_schema.JobType.BRAGG
    inputs: conlist(BraggCompleteInput, min_items=1, max_items=1)


class BraggCreateBatchJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.BRAGG] = job_schema.JobType.BRAGG
    inputs: conlist(BraggCreateInput, min_items=2, max_items=30)


class BraggCompleteBatchJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.BRAGG] = job_schema.JobType.BRAGG
    inputs: conlist(BraggCompleteInput, min_items=2, max_items=30)


class BraggCreateJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.BRAGG] = job_schema.JobType.BRAGG
    inputs: conlist(BraggCreateInput, min_items=1, max_items=1)


class BraggCompleteJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.BRAGG] = job_schema.JobType.BRAGG
    inputs: conlist(BraggCompleteInput, min_items=1, max_items=1)


class BraggCreateBatchJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.BRAGG] = job_schema.JobType.BRAGG
    inputs: conlist(BraggCreateInput, min_items=2, max_items=30)


class BraggCompleteBatchJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.BRAGG] = job_schema.JobType.BRAGG
    inputs: conlist(BraggCompleteInput, min_items=2, max_items=30)
