"""Pydantic factories for BARRIER jobs"""

from pydantic_factories import ModelFactory, PostGenerated

from ...schemas.job import barrier as BarrierSchema
from ..helpers import get_input_count


class BarrierJobPendingFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCreateJob
    input_count = PostGenerated(get_input_count)


class BarrierJobRunningFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCreateJob
    input_count = PostGenerated(get_input_count)


class BarrierJobCompleteFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCompleteJob
    input_count = PostGenerated(get_input_count)


class BarrierJobFailedFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCreateJob
    input_count = PostGenerated(get_input_count)


class BarrierBatchJobPendingFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCreateBatchJob
    input_count = PostGenerated(get_input_count)


class BarrierBatchJobRunningFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCreateBatchJob
    input_count = PostGenerated(get_input_count)


class BarrierBatchJobCompleteFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCompleteBatchJob
    input_count = PostGenerated(get_input_count)


class BarrierBatchJobFailedFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCreateBatchJob
    input_count = PostGenerated(get_input_count)


class BarrierJobResponsePendingFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCreateJobResponse
    input_count = PostGenerated(get_input_count)


class BarrierJobResponseRunningFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCreateJobResponse
    input_count = PostGenerated(get_input_count)


class BarrierJobResponseCompleteFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCompleteJobResponse
    input_count = PostGenerated(get_input_count)


class BarrierJobResponseFailedFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCreateJobResponse
    input_count = PostGenerated(get_input_count)


class BarrierBatchJobResponsePendingFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCreateBatchJobResponse
    input_count = PostGenerated(get_input_count)


class BarrierBatchJobResponseRunningFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCreateBatchJobResponse
    input_count = PostGenerated(get_input_count)


class BarrierBatchJobResponseCompleteFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCompleteBatchJobResponse
    input_count = PostGenerated(get_input_count)


class BarrierBatchJobResponseFailedFactory(ModelFactory):
    __model__ = BarrierSchema.BarrierCreateBatchJobResponse
    input_count = PostGenerated(get_input_count)
