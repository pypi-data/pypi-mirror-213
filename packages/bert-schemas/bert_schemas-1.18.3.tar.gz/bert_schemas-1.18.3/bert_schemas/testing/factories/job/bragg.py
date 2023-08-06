"""Pydantic factories for BRAGG jobs"""

from pydantic_factories import ModelFactory, PostGenerated

from ...schemas.job import bragg as BraggSchema
from ..helpers import get_input_count


class BraggJobPendingFactory(ModelFactory):
    __model__ = BraggSchema.BraggCreateJob
    input_count = PostGenerated(get_input_count)


class BraggJobRunningFactory(ModelFactory):
    __model__ = BraggSchema.BraggCreateJob
    input_count = PostGenerated(get_input_count)


class BraggJobCompleteFactory(ModelFactory):
    __model__ = BraggSchema.BraggCompleteJob
    input_count = PostGenerated(get_input_count)


class BraggJobFailedFactory(ModelFactory):
    __model__ = BraggSchema.BraggCreateJob
    input_count = PostGenerated(get_input_count)


class BraggBatchJobPendingFactory(ModelFactory):
    __model__ = BraggSchema.BraggCreateBatchJob
    input_count = PostGenerated(get_input_count)


class BraggBatchJobRunningFactory(ModelFactory):
    __model__ = BraggSchema.BraggCreateBatchJob
    input_count = PostGenerated(get_input_count)


class BraggBatchJobCompleteFactory(ModelFactory):
    __model__ = BraggSchema.BraggCompleteBatchJob
    input_count = PostGenerated(get_input_count)


class BraggBatchJobFailedFactory(ModelFactory):
    __model__ = BraggSchema.BraggCreateBatchJob
    input_count = PostGenerated(get_input_count)


class BraggJobResponsePendingFactory(ModelFactory):
    __model__ = BraggSchema.BraggCreateJobResponse
    input_count = PostGenerated(get_input_count)


class BraggJobResponseRunningFactory(ModelFactory):
    __model__ = BraggSchema.BraggCreateJobResponse
    input_count = PostGenerated(get_input_count)


class BraggJobResponseCompleteFactory(ModelFactory):
    __model__ = BraggSchema.BraggCompleteJobResponse
    input_count = PostGenerated(get_input_count)


class BraggJobResponseFailedFactory(ModelFactory):
    __model__ = BraggSchema.BraggCreateJobResponse
    input_count = PostGenerated(get_input_count)


class BraggBatchJobResponsePendingFactory(ModelFactory):
    __model__ = BraggSchema.BraggCreateBatchJobResponse
    input_count = PostGenerated(get_input_count)


class BraggBatchJobResponseRunningFactory(ModelFactory):
    __model__ = BraggSchema.BraggCreateBatchJobResponse
    input_count = PostGenerated(get_input_count)


class BraggBatchJobResponseCompleteFactory(ModelFactory):
    __model__ = BraggSchema.BraggCompleteBatchJobResponse
    input_count = PostGenerated(get_input_count)


class BraggBatchJobResponseFailedFactory(ModelFactory):
    __model__ = BraggSchema.BraggCreateBatchJobResponse
    input_count = PostGenerated(get_input_count)
