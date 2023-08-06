"""Pydantic factories for TRANSISTOR jobs"""

from pydantic_factories import ModelFactory, PostGenerated

from ...schemas.job import transistor as TransistorSchema
from ..helpers import get_input_count


class TransistorJobPendingFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCreateJob
    input_count = PostGenerated(get_input_count)


class TransistorJobRunningFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCreateJob
    input_count = PostGenerated(get_input_count)


class TransistorJobCompleteFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCompleteJob
    input_count = PostGenerated(get_input_count)


class TransistorJobFailedFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCreateJob
    input_count = PostGenerated(get_input_count)


class TransistorBatchJobPendingFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCreateBatchJob
    input_count = PostGenerated(get_input_count)


class TransistorBatchJobRunningFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCreateBatchJob
    input_count = PostGenerated(get_input_count)


class TransistorBatchJobCompleteFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCompleteBatchJob
    input_count = PostGenerated(get_input_count)


class TransistorBatchJobFailedFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCreateBatchJob
    input_count = PostGenerated(get_input_count)


class TransistorJobResponsePendingFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCreateJobResponse
    input_count = PostGenerated(get_input_count)


class TransistorJobResponseRunningFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCreateJobResponse
    input_count = PostGenerated(get_input_count)


class TransistorJobResponseCompleteFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCompleteJobResponse
    input_count = PostGenerated(get_input_count)


class TransistorJobResponseFailedFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCreateJobResponse
    input_count = PostGenerated(get_input_count)


class TransistorBatchJobResponsePendingFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCreateBatchJobResponse
    input_count = PostGenerated(get_input_count)


class TransistorBatchJobResponseRunningFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCreateBatchJobResponse
    input_count = PostGenerated(get_input_count)


class TransistorBatchJobResponseCompleteFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCompleteBatchJobResponse
    input_count = PostGenerated(get_input_count)


class TransistorBatchJobResponseFailedFactory(ModelFactory):
    __model__ = TransistorSchema.TransistorCreateBatchJobResponse
    input_count = PostGenerated(get_input_count)
