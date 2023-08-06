"""Pydantic factories for PAINT_1D jobs"""

from pydantic_factories import ModelFactory, PostGenerated

from ...schemas.job import paint_1d as Paint1DSchema
from ..helpers import get_input_count


class Paint1DJobPendingFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCreateJob
    input_count = PostGenerated(get_input_count)


class Paint1DJobRunningFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCreateJob
    input_count = PostGenerated(get_input_count)


class Paint1DJobCompleteFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCompleteJob
    input_count = PostGenerated(get_input_count)


class Paint1DJobFailedFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCreateJob
    input_count = PostGenerated(get_input_count)


class Paint1DBatchJobPendingFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCreateBatchJob
    input_count = PostGenerated(get_input_count)


class Paint1DBatchJobRunningFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCreateBatchJob
    input_count = PostGenerated(get_input_count)


class Paint1DBatchJobCompleteFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCompleteBatchJob
    input_count = PostGenerated(get_input_count)


class Paint1DBatchJobFailedFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCreateBatchJob
    input_count = PostGenerated(get_input_count)


class Paint1DJobResponsePendingFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCreateJobResponse
    input_count = PostGenerated(get_input_count)


class Paint1DJobResponseRunningFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCreateJobResponse
    input_count = PostGenerated(get_input_count)


class Paint1DJobResponseCompleteFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCompleteJobResponse
    input_count = PostGenerated(get_input_count)


class Paint1DJobResponseFailedFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCreateJobResponse
    input_count = PostGenerated(get_input_count)


class Paint1DBatchJobResponsePendingFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCreateBatchJobResponse
    input_count = PostGenerated(get_input_count)


class Paint1DBatchJobResponseRunningFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCreateBatchJobResponse
    input_count = PostGenerated(get_input_count)


class Paint1DBatchJobResponseCompleteFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCompleteBatchJobResponse
    input_count = PostGenerated(get_input_count)


class Paint1DBatchJobResponseFailedFactory(ModelFactory):
    __model__ = Paint1DSchema.Paint1DCreateBatchJobResponse
    input_count = PostGenerated(get_input_count)
