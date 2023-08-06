"""Pytest fixtures for BARRIER jobs"""

import pytest

from .... import job as job_schema
from .... import qpu as qpu_schema
from ...factories.helpers import add_notes, set_run
from ...factories.job import barrier as BarrierFactories


@pytest.fixture
def pending_barrier_job():
    job = BarrierFactories.BarrierJobPendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier job - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_barrier_job():
    job = BarrierFactories.BarrierJobRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier job - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_barrier_job():
    job = BarrierFactories.BarrierJobCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier job - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_barrier_job():
    job = BarrierFactories.BarrierJobFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier job - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job


@pytest.fixture
def pending_barrier_batch_job():
    job = BarrierFactories.BarrierBatchJobPendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier batch job - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_barrier_batch_job():
    job = BarrierFactories.BarrierBatchJobRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier batch job - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_barrier_batch_job():
    job = BarrierFactories.BarrierBatchJobCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier batch job - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_barrier_batch_job():
    job = BarrierFactories.BarrierBatchJobFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier batch job - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job


@pytest.fixture
def pending_barrier_job_response():
    job = BarrierFactories.BarrierJobResponsePendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier job response - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_barrier_job_response():
    job = BarrierFactories.BarrierJobResponseRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier job response - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_barrier_job_response():
    job = BarrierFactories.BarrierJobResponseCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier job response - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_barrier_job_response():
    job = BarrierFactories.BarrierJobResponseFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier job response - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job


@pytest.fixture
def pending_barrier_batch_job_response():
    job = BarrierFactories.BarrierBatchJobResponsePendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier batch job response - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_barrier_batch_job_response():
    job = BarrierFactories.BarrierBatchJobResponseRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier batch job response - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_barrier_batch_job_response():
    job = BarrierFactories.BarrierBatchJobResponseCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier batch job response - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_barrier_batch_job_response():
    job = BarrierFactories.BarrierBatchJobFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test barrier batch job response - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job
