"""Schema definitions for BEC jobs"""

from typing import Literal

from pydantic import conlist, confloat

from .... import job as job_schema
from . import shared as shared_schema


class BecInputValues(job_schema.InputValues):
    end_time_ms: confloat(ge=80.0, le=80.0)
    image_type: Literal[
        job_schema.ImageType.TIME_OF_FLIGHT
    ] = job_schema.ImageType.TIME_OF_FLIGHT
    rf_evaporation: shared_schema.RfEvaporation
    optical_landscape: None
    optical_barriers: None
    lasers: None


class BecCreateInput(job_schema.InputWithoutOutput):
    values: BecInputValues
    output: None


class BecCompleteInput(job_schema.Input):
    values: BecInputValues
    output: job_schema.BecOutput


class BecCreateJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.BEC] = job_schema.JobType.BEC
    inputs: conlist(BecCreateInput, min_items=1, max_items=1)


class BecCompleteJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.BEC] = job_schema.JobType.BEC
    inputs: conlist(BecCompleteInput, min_items=1, max_items=1)


class BecCreateBatchJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.BEC] = job_schema.JobType.BEC
    inputs: conlist(BecCreateInput, min_items=2, max_items=30)


class BecCompleteBatchJob(job_schema.Job):
    job_type: Literal[job_schema.JobType.BEC] = job_schema.JobType.BEC
    inputs: conlist(BecCompleteInput, min_items=2, max_items=30)


class BecCreateJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.BEC] = job_schema.JobType.BEC
    inputs: conlist(BecCreateInput, min_items=1, max_items=1)


class BecCompleteJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.BEC] = job_schema.JobType.BEC
    inputs: conlist(BecCompleteInput, min_items=1, max_items=1)


class BecCreateBatchJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.BEC] = job_schema.JobType.BEC
    inputs: conlist(BecCreateInput, min_items=2, max_items=30)


class BecCompleteBatchJobResponse(job_schema.JobResponse):
    job_type: Literal[job_schema.JobType.BEC] = job_schema.JobType.BEC
    inputs: conlist(BecCompleteInput, min_items=2, max_items=30)
