"""Schema definitions for PAINT_1D jobs"""

from typing import Literal

from pydantic import conlist, confloat

from .... import job as job_schema
from . import shared as shared_schema


class Paint1DInputValues(job_schema.InputValues):
    end_time_ms: confloat(ge=80.0, le=80.0)
    optical_landscape: shared_schema.OpticalLandscape
    optical_barriers: conlist(shared_schema.Barrier, min_items=1, max_items=5)
    rf_evaporation: shared_schema.RfEvaporation
    lasers: conlist(shared_schema.Laser, min_items=1, max_items=1)


class Paint1DCreateInput(job_schema.InputWithoutOutput):
    values: Paint1DInputValues
    output: None


class Paint1DCompleteInput(job_schema.Input):
    values: Paint1DInputValues
    output: job_schema.BarrierOutput


class Paint1DCreateJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.PAINT_1D] = job_schema.JobType.PAINT_1D
    inputs: conlist(Paint1DCreateInput, min_items=1, max_items=1)


class Paint1DCompleteJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.PAINT_1D] = job_schema.JobType.PAINT_1D
    inputs: conlist(Paint1DCompleteInput, min_items=1, max_items=1)


class Paint1DCreateBatchJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.PAINT_1D] = job_schema.JobType.PAINT_1D
    inputs: conlist(Paint1DCreateInput, min_items=2, max_items=30)


class Paint1DCompleteBatchJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.PAINT_1D] = job_schema.JobType.PAINT_1D
    inputs: conlist(Paint1DCompleteInput, min_items=2, max_items=30)


class Paint1DCreateJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.PAINT_1D] = job_schema.JobType.PAINT_1D
    inputs: conlist(Paint1DCreateInput, min_items=1, max_items=1)


class Paint1DCompleteJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.PAINT_1D] = job_schema.JobType.PAINT_1D
    inputs: conlist(Paint1DCompleteInput, min_items=1, max_items=1)


class Paint1DCreateBatchJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.PAINT_1D] = job_schema.JobType.PAINT_1D
    inputs: conlist(Paint1DCreateInput, min_items=2, max_items=30)


class Paint1DCompleteBatchJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.PAINT_1D] = job_schema.JobType.PAINT_1D
    inputs: conlist(Paint1DCompleteInput, min_items=2, max_items=30)
