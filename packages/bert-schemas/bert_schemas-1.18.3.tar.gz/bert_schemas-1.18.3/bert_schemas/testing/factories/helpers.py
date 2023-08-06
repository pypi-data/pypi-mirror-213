"""Helper functions for pydantic factories"""

from ..schemas.job import BertJobSchema


def get_input_count(_, values: dict) -> int:
    return len(values["inputs"])


def add_notes(job: BertJobSchema) -> BertJobSchema:
    for number, input in enumerate(job.inputs):
        input.notes = f"test {job.job_type.lower()} note #{number + 1}"
    return job


def set_run(job: BertJobSchema) -> BertJobSchema:
    for i, input in enumerate(job.inputs):
        input.run = i + 1
    return job
