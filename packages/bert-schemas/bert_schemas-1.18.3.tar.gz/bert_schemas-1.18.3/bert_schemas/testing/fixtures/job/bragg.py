"""Pytest fixtures for BRAGG jobs"""

import pytest

from .... import job as job_schema
from .... import qpu as qpu_schema
from ...factories.helpers import add_notes, set_run
from ...factories.job import bragg as BraggFactories


@pytest.fixture
def pending_bragg_job():
    job = BraggFactories.BraggJobPendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg job - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_bragg_job():
    job = BraggFactories.BraggJobRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg job - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_bragg_job():
    job = BraggFactories.BraggJobCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg job - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_bragg_job():
    job = BraggFactories.BraggJobFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg job - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job


@pytest.fixture
def pending_bragg_batch_job():
    job = BraggFactories.BraggBatchJobPendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg batch job - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_bragg_batch_job():
    job = BraggFactories.BraggBatchJobRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg batch job - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_bragg_batch_job():
    job = BraggFactories.BraggBatchJobCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg batch job - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_bragg_batch_job():
    job = BraggFactories.BraggBatchJobFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg batch job - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job


@pytest.fixture
def pending_bragg_job_response():
    job = BraggFactories.BraggJobResponsePendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg job response - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_bragg_job_response():
    job = BraggFactories.BraggJobResponseRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg job response - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_bragg_job_response():
    job = BraggFactories.BraggJobResponseCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg job response - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_bragg_job_response():
    job = BraggFactories.BraggJobResponseFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg job response - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job


@pytest.fixture
def pending_bragg_batch_job_response():
    job = BraggFactories.BraggBatchJobResponsePendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg batch job response - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_bragg_batch_job_response():
    job = BraggFactories.BraggBatchJobResponseRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg batch job response - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_bragg_batch_job_response():
    job = BraggFactories.BraggBatchJobResponseCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg batch job response - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_bragg_batch_job_response():
    job = BraggFactories.BraggBatchJobResponseFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bragg batch job response - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job
