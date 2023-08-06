"""Pytest fixtures for TRANSISTOR jobs"""

import pytest

from .... import job as job_schema
from .... import qpu as qpu_schema
from ...factories.helpers import add_notes, set_run
from ...factories.job import transistor as TransistorFactories


@pytest.fixture
def pending_transistor_job():
    job = TransistorFactories.TransistorJobPendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor job - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_transistor_job():
    job = TransistorFactories.TransistorJobRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor job - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_transistor_job():
    job = TransistorFactories.TransistorJobCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor job - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_transistor_job():
    job = TransistorFactories.TransistorJobFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor job - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job


@pytest.fixture
def pending_transistor_batch_job():
    job = TransistorFactories.TransistorBatchJobPendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor batch job - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_transistor_batch_job():
    job = TransistorFactories.TransistorBatchJobRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor batch job - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_transistor_batch_job():
    job = TransistorFactories.TransistorBatchJobCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor batch job - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_transistor_batch_job():
    job = TransistorFactories.TransistorBatchJobFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor batch job - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job


@pytest.fixture
def pending_transistor_job_response():
    job = TransistorFactories.TransistorJobResponsePendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor job response - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_transistor_job_response():
    job = TransistorFactories.TransistorJobResponseRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor job response - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_transistor_job_response():
    job = TransistorFactories.TransistorJobResponseCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor job response - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_transistor_job_response():
    job = TransistorFactories.TransistorJobResponseFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor job response - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job


@pytest.fixture
def pending_transistor_batch_job_response():
    job = TransistorFactories.TransistorBatchJobPendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor batch job response - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_transistor_batch_job_response():
    job = TransistorFactories.TransistorBatchJobRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor batch job response - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_transistor_batch_job_response():
    job = TransistorFactories.TransistorBatchJobCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor batch job response - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_transistor_batch_job_response():
    job = TransistorFactories.TransistorBatchJobFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test transistor batch job response - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job
