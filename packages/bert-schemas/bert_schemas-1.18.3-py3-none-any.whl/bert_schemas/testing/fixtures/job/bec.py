"""Pytest fixtures for BEC jobs"""

import pytest

from .... import job as job_schema
from .... import qpu as qpu_schema
from ...factories.helpers import add_notes, set_run
from ...factories.job import bec as BecFactories


@pytest.fixture
def pending_bec_job():
    job = BecFactories.BecJobPendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec job - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_bec_job():
    job = BecFactories.BecJobRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec job - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_bec_job():
    job = BecFactories.BecJobCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec job - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_bec_job():
    job = BecFactories.BecJobFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec job - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job


@pytest.fixture
def pending_bec_batch_job():
    job = BecFactories.BecBatchJobPendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec batch job - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_bec_batch_job():
    job = BecFactories.BecBatchJobRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec batch job - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_bec_batch_job():
    job = BecFactories.BecBatchJobCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec batch job - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_bec_batch_job():
    job = BecFactories.BecBatchJobFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec batch job - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job


@pytest.fixture
def pending_bec_job_response():
    job = BecFactories.BecJobResponsePendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec job response - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_bec_job_response():
    job = BecFactories.BecJobResponseRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec job response - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_bec_job_response():
    job = BecFactories.BecJobResponseCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec job response - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_bec_job_response():
    job = BecFactories.BecJobResponseFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec job response - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job


@pytest.fixture
def pending_bec_batch_job_response():
    job = BecFactories.BecBatchJobResponsePendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec batch job response - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_bec_batch_job_response():
    job = BecFactories.BecBatchJobResponseRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec batch job response - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_bec_batch_job_response():
    job = BecFactories.BecBatchJobResponseCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec batch job response - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_bec_batch_job_response():
    job = BecFactories.BecBatchJobResponseFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test bec batch job response - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job
