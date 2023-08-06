"""Pydantic factories for BEC jobs"""

from pydantic_factories import ModelFactory, PostGenerated

from ...schemas.job import bec as BecSchema
from ..helpers import get_input_count


class BecJobPendingFactory(ModelFactory):
    __model__ = BecSchema.BecCreateJob
    input_count = PostGenerated(get_input_count)


class BecJobRunningFactory(ModelFactory):
    __model__ = BecSchema.BecCreateJob
    input_count = PostGenerated(get_input_count)


class BecJobCompleteFactory(ModelFactory):
    __model__ = BecSchema.BecCompleteJob
    input_count = PostGenerated(get_input_count)


class BecJobFailedFactory(ModelFactory):
    __model__ = BecSchema.BecCreateJob
    input_count = PostGenerated(get_input_count)


class BecBatchJobPendingFactory(ModelFactory):
    __model__ = BecSchema.BecCreateBatchJob
    input_count = PostGenerated(get_input_count)


class BecBatchJobRunningFactory(ModelFactory):
    __model__ = BecSchema.BecCreateBatchJob
    input_count = PostGenerated(get_input_count)


class BecBatchJobCompleteFactory(ModelFactory):
    __model__ = BecSchema.BecCompleteBatchJob
    input_count = PostGenerated(get_input_count)


class BecBatchJobFailedFactory(ModelFactory):
    __model__ = BecSchema.BecCreateBatchJob
    input_count = PostGenerated(get_input_count)


class BecJobResponsePendingFactory(ModelFactory):
    __model__ = BecSchema.BecCreateJobResponse
    input_count = PostGenerated(get_input_count)


class BecJobResponseRunningFactory(ModelFactory):
    __model__ = BecSchema.BecCreateJobResponse
    input_count = PostGenerated(get_input_count)


class BecJobResponseCompleteFactory(ModelFactory):
    __model__ = BecSchema.BecCompleteJobResponse
    input_count = PostGenerated(get_input_count)


class BecJobResponseFailedFactory(ModelFactory):
    __model__ = BecSchema.BecCreateJobResponse
    input_count = PostGenerated(get_input_count)


class BecBatchJobResponsePendingFactory(ModelFactory):
    __model__ = BecSchema.BecCreateBatchJobResponse
    input_count = PostGenerated(get_input_count)


class BecBatchJobResponseRunningFactory(ModelFactory):
    __model__ = BecSchema.BecCreateBatchJobResponse
    input_count = PostGenerated(get_input_count)


class BecBatchJobResponseCompleteFactory(ModelFactory):
    __model__ = BecSchema.BecCompleteBatchJobResponse
    input_count = PostGenerated(get_input_count)


class BecBatchJobResponseFailedFactory(ModelFactory):
    __model__ = BecSchema.BecCreateBatchJobResponse
    input_count = PostGenerated(get_input_count)
