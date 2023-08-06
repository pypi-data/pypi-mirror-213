"""Pytest fixtures for PAINT_1D jobs"""

import pytest

from .... import job as job_schema
from .... import qpu as qpu_schema
from ...factories.helpers import add_notes, set_run
from ...factories.job import paint_1d as Paint1DFactories


@pytest.fixture
def pending_paint_1d_job():
    job = Paint1DFactories.Paint1DJobPendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d job - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_paint_1d_job():
    job = Paint1DFactories.Paint1DJobRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d job - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_paint_1d_job():
    job = Paint1DFactories.Paint1DJobCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d job - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_paint_1d_job():
    job = Paint1DFactories.Paint1DJobFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d job - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job


@pytest.fixture
def pending_paint_1d_batch_job():
    job = Paint1DFactories.Paint1DBatchJobPendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d batch job - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_paint_1d_batch_job():
    job = Paint1DFactories.Paint1DBatchJobRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d batch job - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_paint_1d_batch_job():
    job = Paint1DFactories.Paint1DBatchJobCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d batch job - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_paint_1d_batch_job():
    job = Paint1DFactories.Paint1DBatchJobFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d batch job - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job


@pytest.fixture
def pending_paint_1d_job_response():
    job = Paint1DFactories.Paint1DJobResponsePendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d job response - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_paint_1d_job_response():
    job = Paint1DFactories.Paint1DJobResponseRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d job response - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_paint_1d_job_response():
    job = Paint1DFactories.Paint1DJobResponseCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d job response - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_paint_1d_job_response():
    job = Paint1DFactories.Paint1DJobResponseFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d job response - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job


@pytest.fixture
def pending_paint_1d_batch_job_response():
    job = Paint1DFactories.Paint1DBatchJobResponsePendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d batch job response - pending")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.PENDING
    job.display = True
    yield job


@pytest.fixture
def running_paint_1d_batch_job_response():
    job = Paint1DFactories.Paint1DBatchJobResponseRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d batch job response - running")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.RUNNING
    job.display = True
    yield job


@pytest.fixture
def complete_paint_1d_batch_job_response():
    job = Paint1DFactories.Paint1DBatchJobResponseCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d batch job response - complete")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.COMPLETE
    job.display = True
    yield job


@pytest.fixture
def failed_paint_1d_batch_job_response():
    job = Paint1DFactories.Paint1DBatchJobResponseFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    job.name = job_schema.JobName("test paint_1d batch job response - failed")
    job.qpu_name = qpu_schema.QPUName.BIGBERT
    job.status = job_schema.JobStatus.FAILED
    job.display = True
    yield job
