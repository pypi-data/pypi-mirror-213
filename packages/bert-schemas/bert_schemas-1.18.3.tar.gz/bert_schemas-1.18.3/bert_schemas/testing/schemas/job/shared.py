"""Schema models shared across multiple job types"""

import numpy as np
from pydantic import conlist, confloat, validator

from .... import job as job_schema


class RfEvaporation(job_schema.RfEvaporation):
    # these lists require that they are all the same length
    times_ms: conlist(confloat(ge=-2000.0, le=80.0), min_items=20, max_items=20)
    frequencies_mhz: conlist(confloat(ge=0.0, le=25.0), min_items=20, max_items=20)
    powers_mw: conlist(confloat(ge=0.0, le=1000.0), min_items=20, max_items=20)


class Landscape(job_schema.Landscape):
    # these lists require that they are all the same length
    potentials_khz: conlist(confloat(ge=0.0, le=100.0), min_items=101, max_items=101)
    positions_um: conlist(confloat(ge=-50.0, le=50.0), min_items=101, max_items=101)


class OpticalLandscape(job_schema.OpticalLandscape):
    # use landscape defined here
    landscapes: conlist(Landscape, min_items=1, max_items=5)

    @validator("landscapes", pre=True)
    def set_landscape_time_ms(cls, v):
        for index, landscape in enumerate(v):
            landscape.time_ms = float(index + (index + 1))
        return v


class Barrier(job_schema.Barrier):
    # these lists require that they are all the same length
    times_ms: conlist(confloat(ge=0.0, le=80.0), min_items=20, max_items=20)
    positions_um: conlist(confloat(ge=-50.0, le=50.0), min_items=20, max_items=20)
    heights_khz: conlist(confloat(ge=0.0, le=100.0), min_items=20, max_items=20)
    widths_um: conlist(confloat(ge=1.0, le=50.0), min_items=20, max_items=20)


class Pulse(job_schema.Pulse):
    # these lists require that they are all the same length
    times_ms: conlist(confloat(ge=0.0, le=80.0), min_items=10, max_items=10)
    intensities_mw_per_cm2: conlist(
        confloat(ge=0.0, le=1000.0), min_items=10, max_items=10
    )

    @validator("times_ms", pre=True)
    def order_times_ms(cls, v):
        v.sort()
        return v


class Laser(job_schema.Laser):
    # use pulse defined here
    pulses: conlist(Pulse, min_items=1, max_items=10)

    @validator("pulses", pre=True)
    def set_pulse_times_ms(cls, v):
        for index, pulse in enumerate(v):
            pulse.times_ms = [
                float(value)
                for value in np.linspace(index + (index + 1), index + (index + 2), 10)
            ]
        return v
