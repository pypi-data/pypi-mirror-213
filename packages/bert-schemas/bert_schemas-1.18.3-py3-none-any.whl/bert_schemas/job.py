# type: ignore
import warnings
from datetime import datetime
from enum import auto
from typing import Dict, List, Optional
from uuid import UUID

import matplotlib.pyplot as plt
import numpy as np
from fastapi_utils.enums import StrEnum
from pydantic import (
    BaseModel,
    ConstrainedStr,
    confloat,
    conint,
    conlist,
    root_validator,
    validator,
)
from scipy.interpolate import interp1d
from typing_extensions import TypedDict
from .qpu import QPUBase, QPUName


class JobOrigin(StrEnum):
    WEB = auto()
    OQTANT = auto()


class JobType(StrEnum):
    BEC = "BEC"
    BARRIER = "BARRIER"
    BRAGG = "BRAGG"
    TRANSISTOR = "TRANSISTOR"
    PAINT_1D = "PAINT_1D"

    def __str__(self):
        return str(self.value)


class ImageType(StrEnum):
    IN_TRAP = "IN_TRAP"
    TIME_OF_FLIGHT = "TIME_OF_FLIGHT"

    def __str__(self):
        return str(self.value)


class OutputJobType(StrEnum):
    IN_TRAP = "IN_TRAP"
    NON_IN_TRAP = "NON_IN_TRAP"

    def __str__(self):
        return str(self.value)


class JobStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    INCOMPLETE = "INCOMPLETE"

    def __str__(self):
        return str(self.value)


class RfInterpolationType(StrEnum):
    LINEAR = "LINEAR"
    STEP = "STEP"
    OFF = "OFF"
    PREVIOUS = "PREVIOUS"  # assumes value of previous data point

    def __str__(self):
        return str(self.value)


class InterpolationType(StrEnum):
    LINEAR = "LINEAR"
    SMOOTH = "SMOOTH"
    STEP = "STEP"
    OFF = "OFF"
    # native scipy options
    ZERO = "ZERO"  # spline interpolation at zeroth order
    SLINEAR = "SLINEAR"  # spline interpolation at first order
    QUADRATIC = "QUADRATIC"  # spline interpolation at second order
    CUBIC = "CUBIC"  # spline interpolation at third order
    # LINEAR = "LINEAR"         # self explanatory
    NEAREST = "NEAREST"  # assumes value of nearest data point
    PREVIOUS = "PREVIOUS"  # assumes value of previous data point
    NEXT = "NEXT"  # assumes value of next data point

    def __str__(self):
        return str(self.value)


class LaserType(StrEnum):
    TERMINATOR = "TERMINATOR"
    BRAGG = "BRAGG"

    def __str__(self):
        return str(self.value)


class ShapeType(StrEnum):
    GAUSSIAN = "GAUSSIAN"
    LORENTZIAN = "LORENTZIAN"
    SQUARE = "SQUARE"

    def __str__(self):
        return str(self.value)


class JobName(ConstrainedStr):
    min_length = 1
    max_length = 50


class JobNote(ConstrainedStr):
    max_length = 500


class Image(BaseModel):
    pixels: List[float]
    rows: int
    columns: int

    class Config:
        validate_assignment = True


class Point(TypedDict):
    x: float
    y: float


class LineChart(BaseModel):
    points: List[Dict[str, float]]

    class Config:
        validate_assignment = True


class RfEvaporation(BaseModel):
    # times_ms upper range can be no larger than end_time_ms of job (80.0 ms is upper default)
    times_ms: conlist(confloat(ge=-2000.0, le=80.0), min_items=1, max_items=20) = list(
        range(-1600, 400, 400)
    )
    frequencies_mhz: conlist(confloat(ge=0.0, le=25.0), min_items=1, max_items=20)
    powers_mw: conlist(confloat(ge=0.0, le=1000.0), min_items=1, max_items=20)
    interpolation: RfInterpolationType

    class Config:
        validate_assignment = True

    @root_validator(skip_on_failure=True)
    def cross_validate(cls, values: dict):
        assert (
            len(values["times_ms"])
            == len(values["frequencies_mhz"])
            == len(values["powers_mw"])
        ), "RfEvaporation data lists must have the same length."

        if values["times_ms"] != sorted(values["times_ms"]):
            warnings.warn(
                "Evaporation times_ms list must be naturally ordered, re-ordering.",
                stacklevel=2,
            )
            values["times_ms"], values["frequencies_mhz"], values["powers_mw"] = zip(
                *sorted(
                    zip(
                        values["times_ms"],
                        values["frequencies_mhz"],
                        values["powers_mw"],
                    )
                )
            )
        return values

    def get_frequency(self, time: float) -> float:
        """Get RF evaporation frequency (detuning) at the specified time.

        Args:
            time (float): Time (in ms) at which the RF frequency is calculated.
        Returns:
            float: RF frequency/detuning (in MHz) at the specified time.
        """
        return interpolate_1D(
            self.times_ms, self.frequencies_mhz, time, self.interpolation
        )

    def get_frequencies(self, times: list) -> list:
        """Get RF evaporation frequency (detuning) at the specified list of times.

        Args:
            times (list): Times (in ms) at which the RF frequencies/detunings are calculated.
        Returns:
            list: RF frequencies/detunings (in MHz) at the specified times.
        """
        return interpolate_1D_list(
            self.times_ms, self.frequencies_mhz, times, self.interpolation
        )

    def get_power(self, time: float) -> float:
        """Get RF evaporation power at the specified time.

        Args:
            time (float): Time (in ms) at which the RF power is calculated.
        Returns:
            float: RF power (in mW) at the specified time.
        """
        return interpolate_1D(self.times_ms, self.powers_mw, time, self.interpolation)

    def get_powers(self, times: list) -> list:
        """Get RF evaporation powers at the specified times.

        Args:
            times (list): Times (in ms) at which the RF powers are calculated.
        Returns:
            list: RF powers (in mW) at the specified times.
        """
        return interpolate_1D_list(
            self.times_ms, self.powers_mw, times, self.interpolation
        )

    def get_plot_times(self) -> list:
        """Returns a list of times that are useful for plotting time-dependent parameters.

        Args:
        Returns:
            list: Times in ms
        """
        return np.arange(self.times_ms[0], self.times_ms[-1], 0.1)

    def plot_frequency(self, x_limits: list = None, y_limits: list = None):
        """Plots the frequency/detuning of the RF evaporation over time, along with the underlying data points.

        Args:
            x_limits (list, optional): two-element list of minimum and maximum x (times in ms) to plot over.
            Defaults to limits of defined evaporation times -/+ 100.
            y_limits (list, optional): two-element list of minimum and maximum y (frequencies in MHz) to plot over.
            Defaults to [0, max frequency + 1]
        """
        if x_limits is None:
            x_limits = [self.times_ms[0] - 100, self.times_ms[-1] + 100]
        if y_limits is None:
            y_limits = [0, max(self.frequencies_mhz) + 1]
        times = self.get_plot_times()
        Plotter.plot_points_and_line(
            x_data_points=self.times_ms,
            y_data_points=self.frequencies_mhz,
            x_data_line=times,
            y_data_line=self.get_frequencies(times),
            x_limits=x_limits,
            y_limits=y_limits,
            x_label="time (ms)",
            y_label="frequency/detuning (MHz)",
        )

    def plot_power(self, x_limits: list = None, y_limits: list = None):
        """Plots the power of the RF evaporation over time, along with the underlying data points.

        Args:
            x_limits (list, optional): two-element list of minimum and maximum x (times in ms) to plot over.
            Defaults to limits of defined evaporation times -/+ 100.
            y_limits (list, optional): two-element list of minimum and maximum y (powers in mW) to plot over.
            Defaults to [0, max power + 100]
        """
        if x_limits is None:
            x_limits = [self.times_ms[0] - 100, self.times_ms[-1] + 100]
        if y_limits is None:
            y_limits = [0, max(self.powers_mw) + 100]
        times = self.get_plot_times()
        Plotter.plot_points_and_line(
            x_data_points=self.times_ms,
            y_data_points=self.powers_mw,
            x_data_line=times,
            y_data_line=self.get_powers(times),
            x_limits=x_limits,
            y_limits=y_limits,
            x_label="time (ms)",
            y_label="power (mW)",
        )


class Landscape(BaseModel):
    # time_ms upper range can be no larger than end_time_ms of job (80.0 ms is upper default)
    time_ms: confloat(ge=0.0, le=80.0)
    potentials_khz: conlist(confloat(ge=0.0, le=100.0), min_items=2, max_items=101)
    positions_um: conlist(confloat(ge=-50.0, le=50.0), min_items=2, max_items=101)
    spatial_interpolation: InterpolationType

    @root_validator(skip_on_failure=True)
    def cross_validate(cls, values: dict):
        assert len(values["positions_um"]) == len(
            values["potentials_khz"]
        ), "Landscape data lists must have the same length."

        if values["positions_um"] != sorted(values["positions_um"]):
            warnings.warn(
                "Landscape positions_um list must be naturally ordered, re-ordering.",
                stacklevel=2,
            )
            values["positions_um"], values["potentials_khz"] = zip(
                *sorted(zip(values["positions_um"], values["potentials_khz"]))
            )
        return values

    def __lt__(self, other):
        return self.time_ms < other.time_ms

    def get_potential_at_position(self, position: float) -> float:
        """Samples the potential energy of this Landscape at the specified position (in microns)

        Args:
            position (float): Position (in microns) at which the potential energy is sampled.

        Returns:
            float: Value of potential energy (in kHz) at the specified position.
        """
        return interpolate_1D(
            self.positions_um, self.potentials_khz, position, self.spatial_interpolation
        )

    def get_potential_at_positions(self, positions: list) -> list:
        """Samples the potential energy of this Landscape at the specified positions (in microns)

        Args:
            positions (list): List of positions (in microns) at which to sample the potential energy landscape.

        Returns:
            list: Value of potential energy (in kHz) at the specified positions.
        """
        return interpolate_1D_list(
            self.positions_um,
            self.potentials_khz,
            positions,
            self.spatial_interpolation,
        )

    def plot_potential(self, x_limits: list = None, y_limits: list = None):
        """Plots the potential energy (in kHz) as a function of positions (in microns) for this landscape.

        Args:
            x_limits (list, optional): Plot position range (in microns) as a list of [min, max]. Default is [-101, 101].
            y_limits (list, optional): Plot energy range (in kHz) as a list of [min, max]. Default is [0, 101].
        """
        if x_limits is None:
            x_limits = [-101, 101]
        if y_limits is None:
            y_limits = [0, 101]
        positions = np.arange(-100, 100, 1)
        Plotter.plot_points_and_line(
            x_data_points=self.positions_um,
            y_data_points=self.potentials_khz,
            x_data_line=positions,
            y_data_line=self.get_potential_at_positions(positions),
            x_limits=x_limits,
            y_limits=y_limits,
            x_label=r"position ($\mu$m)",
            y_label="potential energy (kHz)",
        )


class OpticalLandscape(BaseModel):
    interpolation: InterpolationType = InterpolationType.LINEAR
    landscapes: conlist(Landscape, min_items=1, max_items=5)

    class Config:
        validate_assignment = True

    @root_validator(skip_on_failure=True)
    def cross_validate(cls, values: dict):
        # ensure the individual Landscape objects are far enough apart in time and naturally (time) ordered
        values["landscapes"] = sorted(values["landscapes"], key=lambda l: l.time_ms)

        dts_ms = [
            values["landscapes"][i + 1].time_ms - values["landscapes"][i].time_ms
            for i in range(len(values["landscapes"]) - 1)
        ]
        assert all(
            dt > 1 for dt in dts_ms
        ), "Constituent Landscape object time_ms values must differ by >= 1 ms"
        return values

    def get_potentials(
        self, time: float, positions: list = np.linspace(-100, 100, 201)
    ) -> list:
        """Calculate OpticalLandscape potential energy at the specified time and list of positions.

        Args:
            time (float): Time (in ms) at which the potential energy landscape is calculated.
            positions (list, optional): Positions at which the potential energy is calculated.
            Defaults to np.linspace(-100, 100, 201).

        Returns:
            list: List of potentials energy (in kHz) at the specified time and positions.
        """
        self.landscapes.sort()  # need landscapes list [] to be naturally ordered for this to work
        landscapes = self.landscapes
        is_active = time >= landscapes[0].time_ms and time < landscapes[-1].time_ms
        potentials = np.zeros_like(positions)
        if not is_active:
            return [0] * len(positions)
        else:
            pre = next(
                landscape
                for landscape in reversed(landscapes)
                if landscape.time_ms <= time
            )
            nex = next(
                landscape for landscape in landscapes if landscape.time_ms > time
            )
            ts = [pre.time_ms, nex.time_ms]
            pre_potentials = pre.get_potential_at_positions(positions)
            nex_potentials = nex.get_potential_at_positions(positions)
            potentials = [
                interpolate_1D(ts, [p1, p2], time, self.interpolation)
                for p1, p2 in zip(pre_potentials, nex_potentials)
            ]
            current = Landscape(
                time_ms=time,
                positions_um=list(positions),
                potentials_khz=list(potentials),
                spatial_interpolation=self.interpolation,
            )
            return current.get_potential_at_positions(positions)

    def plot_potential(self, time: float, x_limits: list = None, y_limits: list = None):
        """Plots the potential energy (in kHz) as a function of positions (in microns) at the specified time.

        Args:
            x_limits (list, optional): Plot position range (in microns) as a list of [min, max]. Default is [-101, 101].
            y_limits (list, optional): Plot energy range (in kHz) as a list of [min, max]. Default is [0, 101].
        """
        if x_limits is None:
            x_limits = [-101, 101]
        if y_limits is None:
            y_limits = [0, 101]
        positions = np.linspace(-50, 50, 101)
        Plotter.plot_points_and_line(
            x_data_points=[],
            y_data_points=[],
            x_data_line=positions,
            y_data_line=self.get_potentials(time, positions),
            x_limits=x_limits,
            y_limits=y_limits,
            x_label=r"position ($\mu$m)",
            y_label="potential energy (kHz)",
            title="t = " + str(time) + " ms",
        )


class TofFit(BaseModel):
    gaussian_od: float
    gaussian_sigma_x: float
    gaussian_sigma_y: float
    tf_od: float
    tf_x: float
    tf_y: float
    x_0: float
    y_0: float
    offset: float

    class Config:
        validate_assignment = True


class Barrier(BaseModel):
    # times_ms upper range can be no larger than end_time_ms of job (80.0 ms is upper default)
    times_ms: conlist(confloat(ge=0.0, le=80.0), min_items=1, max_items=20) = list(
        range(11)
    )
    positions_um: conlist(
        confloat(ge=-50.0, le=50.0), min_items=1, max_items=20
    ) = list(range(11))
    heights_khz: conlist(confloat(ge=0.0, le=100.0), min_items=1, max_items=20) = [
        10
    ] * 11
    widths_um: conlist(confloat(ge=1.0, le=50.0), min_items=1, max_items=20) = [1] * 11
    interpolation: InterpolationType = InterpolationType.LINEAR
    shape: ShapeType = ShapeType.GAUSSIAN

    class Config:
        validate_assignment = True

    @root_validator(skip_on_failure=True)
    def cross_validate(cls, values: dict):
        assert (
            len(values["times_ms"])
            == len(values["positions_um"])
            == len(values["heights_khz"])
            == len(values["widths_um"])
        ), "Barrier data lists must have the same length."

        if values["times_ms"] != sorted(values["times_ms"]):
            warnings.warn(
                "Barrier times_ms list must be naturally ordered, re-ordering.",
                stacklevel=2,
            )
            (
                values["times_ms"],
                values["positions_um"],
                values["heights_khz"],
                values["widths_um"],
            ) = zip(
                *sorted(
                    zip(
                        values["times_ms"],
                        values["positions_um"],
                        values["heights_khz"],
                        values["widths_um"],
                    )
                )
            )
        return values

    def is_active(self, time: float) -> bool:
        """Queries if the barrier is active (exists) at the specified time

        Args:
            time (float): Time (in ms) at which the query is evaluated.

        Returns:
            bool: True if the barrier exists at the specified time.  Otherwise False.
        """
        return time > self.times_ms[0] and time < self.times_ms[-1]

    def get_position(self, time: float) -> float:
        r"""Get barrier position during the experiment.

        Args:
            time (float): Time (in ms) at which the barrier position is calculated.
        Returns:
            float: Barrier position (in $\mu$m).
        """
        return interpolate_1D(
            self.times_ms, self.positions_um, time, self.interpolation
        )

    def get_positions(self, times: list) -> list:
        r"""Get barrier positions at the specified list of times

        Args:
            times (float): Times (in ms) at which the barrier positions are calculated.
        Returns:
            list: Barrier positions (in $\mu$m) at desired times.
        """
        return interpolate_1D_list(
            self.times_ms, self.positions_um, times, self.interpolation
        )

    def get_height(self, time: float) -> float:
        """Get barrier height during the experiment.

        Args:
            time (float): Time (in ms) at which the barrier height is calculated.
        Returns:
            float: Barrier height (in kHz).
        """
        return interpolate_1D(self.times_ms, self.heights_khz, time, self.interpolation)

    def get_heights(self, times: list) -> list:
        r"""Get barrier heights at the specified list of times

        Args:
            times (float): Times (in ms) at which the barrier heights are calculated.
        Returns:
            list: Barrier heights (in kHz) at desired times.
        """
        return interpolate_1D_list(
            self.times_ms, self.heights_khz, times, self.interpolation
        )

    def get_width(self, time: float) -> float:
        """Returns the barrier sidth (in microns) at the specified time (in ms)"""
        """Get barrier width during the experiment.

        Args:
            time (float): Time (in ms) at which the barrier width is calculated.
        Returns:
            float: Barrier width (in microns).
        """
        return interpolate_1D(self.times_ms, self.widths_um, time, self.interpolation)

    def get_widths(self, times: list) -> list:
        """Get barrier widths at the specified list of times

        Args:
            times (float): Times (in ms) at which the barrier widths are calculated.
        Returns:
            list: Barrier widths (in microns) at desired times.
        """
        return interpolate_1D_list(
            self.times_ms, self.widths_um, times, self.interpolation
        )

    def get_potentials(
        self, time: float, positions: list = range(-100, 100, 1)
    ) -> list:
        """Returns barrier potential energy over the given positions at the specified time

        Args:
            time_ms (float): Time (in ms) at which the barrier potential is calculated
            positions_um (list, optional): Positions in microns at which the potential energy is evaluated.
                Defaults to range(-100, 100, 1).

        Returns:
            list: Potential energies (in kHz) at the input positions
        """
        height = self.get_height(time)
        position = self.get_position(time)
        width = self.get_width(time)
        if height > 0 and width > 0 and self.is_active(time):
            if self.shape == "SQUARE":  # width = box width

                def f(a, x0, width, x):
                    return 0 if x < x0 - width / 2 or x > x0 + width / 2 else a

            elif self.shape == "LORENTZIAN":  # width = HWHM (half-width half-max)

                def f(a, x0, width, x):
                    return a / (1 + ((x - x0) / width) ** 2)

            elif self.shape == "GAUSSIAN":  # width = sigma (Gaussian width)

                def f(a, x0, width, x):
                    return a * np.exp(-((x - x0) ** 2) / (2 * width**2))

            else:

                def f(a, x0, width, x):
                    return 0

                return [0] * len(positions)
            return [f(height, position, width, p) for p in positions]

    def get_plot_times(self) -> list:
        """Returns a list of times that are useful for plotting time-dependent parameters of this barrier.

        Args:
        Returns:
            list: Times in ms
        """
        return np.arange(self.times_ms[0], self.times_ms[-1], 0.1)

    def plot_position(self, x_limits: list = None, y_limits: list = None):
        """Plots the position of the barrier over time

        Args:
            x_limits (list, optional): two-element list of minimum and maximum x (times) to plot over.
            Defaults to limits of defined barrier times.
            y_limits (list, optional): two-element list of minimum and maximum y (positions) to plot over.
            Defaults to [0, max position + 1]
        """
        if x_limits is None:
            x_limits = [self.times_ms[0] - 1, self.times_ms[-1] + 1]
        if y_limits is None:
            y_limits = [0, max(self.positions_um) + 1]
        times = self.get_plot_times()
        Plotter.plot_points_and_line(
            x_data_points=self.times_ms,
            y_data_points=self.positions_um,
            x_data_line=times,
            y_data_line=self.get_positions(times),
            x_limits=x_limits,
            y_limits=y_limits,
            x_label="time (ms)",
            y_label=r"position ($\mu$m)",
        )

    def plot_height(self, x_limits: list = None, y_limits: list = None):
        """Plots the height of the barrier over time

        Args:
            x_limits (list, optional): two-element list of minimum and maximum x (times) to plot over.
            Defaults to limits of defined barrier times.
            y_limits (list, optional): two-element list of minimum and maximum y (positions) to plot over.
            Defaults to [0, max height + 1]
        """
        if x_limits is None:
            x_limits = [self.times_ms[0] - 1, self.times_ms[-1] + 1]
        if y_limits is None:
            y_limits = [0, max(self.heights_khz) + 1]
        times = self.get_plot_times()
        Plotter.plot_points_and_line(
            x_data_points=self.times_ms,
            y_data_points=self.heights_khz,
            x_data_line=times,
            y_data_line=self.get_heights(times),
            x_limits=x_limits,
            y_limits=y_limits,
            x_label="time (ms)",
            y_label="height (kHz)",
        )

    def plot_width(self, x_limits: list = None, y_limits: list = None):
        """Plots the width of the barrier over time

        Args:
            x_limits (list, optional): two-element list of minimum and maximum x (times) to plot over.
            Defaults to limits of defined barrier times.
            y_limits (list, optional): two-element list of minimum and maximum y (positions) to plot over.
            Defaults to [0, max width + 1]
        """
        if x_limits is None:
            x_limits = [self.times_ms[0] - 1, self.times_ms[-1] + 1]
        if y_limits is None:
            y_limits = [0, max(self.widths_um) + 1]
        times = self.get_plot_times()
        Plotter.plot_points_and_line(
            x_data_points=self.times_ms,
            y_data_points=self.widths_um,
            x_data_line=times,
            y_data_line=self.get_widths(times),
            x_limits=x_limits,
            y_limits=y_limits,
            x_label="time (ms)",
            y_label=r"width ($\mu$m)",
        )

    def plot_potential(self, time: float, x_limits: list = None, y_limits: list = None):
        """Plot the potential energy as a function of position

        Args:
            time (float): time (in ms) at which the potential is calculated.
            x_limits (list, optional): Position limits of plot. Defaults to [-100, 100].
            y_limits (list, optional): Potential energy limits of plot. Defaults to [0, max height + 1].
        """
        if x_limits is None:
            x_limits = [-100, 100]
        if y_limits is None:
            y_limits = [0, max(self.heights_khz) + 1]
        positions = np.arange(min(x_limits), max(x_limits), 0.1)
        Plotter.plot_points_and_line(
            x_data_points=[],
            y_data_points=[],
            x_data_line=positions,
            y_data_line=self.get_potentials(time, positions),
            x_limits=x_limits,
            y_limits=y_limits,
            x_label="time (ms)",
            y_label=r"width ($\mu$m)",
            title="t = " + str(time) + " ms",
        )


class Pulse(BaseModel):
    # times_ms upper range can be no larger than end_time_ms of job (80.0 ms is upper default)
    times_ms: conlist(confloat(ge=0.0, le=80.0), min_items=1, max_items=10)
    intensities_mw_per_cm2: conlist(
        confloat(ge=0.0, le=1000.0), min_items=1, max_items=10
    )
    detuning_mhz: confloat(ge=-100.0, le=100.0)
    interpolation: InterpolationType

    class Config:
        validate_assignment = True

    @root_validator(skip_on_failure=True)
    def cross_validate(cls, values):
        assert len(values["times_ms"]) == len(
            values["intensities_mw_per_cm2"]
        ), "Pulse data lists must have the same length."
        return values

    @validator("times_ms")
    def naturally_order_times(cls, v):
        assert v == sorted(v), "Pulse times must be naturally ordered."
        return v

    def __lt__(self, other):
        return min(self.times_ms) < min(other.times_ms)

    def get_plot_times(self) -> list:
        """Returns a list of times that are useful for plotting time-dependent parameters of this Pulse.

        Args:
        Returns:
            list: Times in ms
        """
        return np.arange(min(self.times_ms) - 1, max(self.times_ms) + 1, 0.1)

    def get_intensity(self, time_ms: float) -> float:
        """Gets value of pulse intensity at the specified time.

        Args:
            time_ms (float): Time at which to evaluate the Pulse intensity, in ms

        Returns:
            float: Intensity calculated at the specified time, in mW/cm^2.
        """
        interp = interpolate_1D(
            self.times_ms, self.intensities_mw_per_cm2, time_ms, self.interpolation
        )
        return max(interp, 0.0)  # intensity is >= 0

    def get_intensities(self, times_ms: list) -> list:
        """Gets values of pulse intensity at the desired times.

        Args:
            times_ms (list): Times at which the Pulse intensity if evaluated.

        Returns:
            list: Intensities corresponding to the input times.
        """
        interps = interpolate_1D_list(
            self.times_ms, self.intensities_mw_per_cm2, times_ms, self.interpolation
        )
        return [max(x, 0.0) for x in interps]  # intensities are >= 0

    def plot_intensity(self, x_limits: None, y_limits: None):
        """Plots the intensity of this laser Pulse over time.

        Args:
            x_limits (None): Time domain over which to plot.  Defaults to min Pulse time - 1.
            y_limits (None): Intensity range over which to plot.  Defaults to min Pulse time - 1.
        """
        times = self.get_plot_times()
        intensities = self.get_intensities(times)
        if x_limits is None:
            x_limits = [min(self.times_ms) - 1, max(self.times_ms) + 1]
        if y_limits is None:
            y_limits = [-1, max(intensities) + 1]
        Plotter.plot_points_and_line(
            x_data_points=self.times_ms,
            y_data_points=self.intensities_mw_per_cm2,
            x_data_line=times,
            y_data_line=intensities,
            x_limits=x_limits,
            y_limits=y_limits,
            x_label="time (ms)",
            y_label="intensity (mW / cm^2)",
        )


class Laser(BaseModel):
    type: LaserType
    pulses: conlist(Pulse, min_items=1, max_items=10)

    class Config:
        validate_assignment = True

    @validator("pulses")
    def pulses_overlap(cls, v):
        for index, pulse in enumerate(v):
            if index < len(v) - 1:
                dt_ms = min(v[index + 1].times_ms) - max(v[index].times_ms)
                assert (
                    dt_ms >= 1
                ), "Distinct pulses features too close together in time (< 1 ms)"
        return v

    def get_plot_times(self) -> list:
        """Returns a list of times that are useful for plotting time-dependent parameters of this Laser.

        Args:
        Returns:
            list: Times in ms
        """
        min_time = 0
        max_time = 0
        for pulse in self.pulses:
            min_time = min(min_time, min(pulse.times_ms))
            max_time = max(max_time, max(pulse.times_ms))
        min_time = min_time - 1
        max_time = max_time + 1
        return np.arange(min_time, max_time, 0.1)

    def plot_intensity(self, x_limits: list = None, y_limits: list = None):
        """Plots the laser intensity (all pulses) over the course of the experiment.

        Args:
            x_limits (list, optional): Time domain for plot. Defaults to 1 ms before/after constituent pulses.
            y_limits (list, optional): Intensity range for plot. Defaults to 1 ms before/after constituent pulses.
        """
        plot_times = self.get_plot_times()
        Plotter.plot_intensity(x_limits, y_limits, self.pulses, plot_times)


class NonPlotOutput(BaseModel):
    mot_fluorescence_image: Image
    tof_image: Image
    tof_fit_image: Image
    tof_fit: TofFit
    tof_x_slice: LineChart
    tof_y_slice: LineChart
    total_mot_atom_number: int
    tof_atom_number: int
    thermal_atom_number: int
    condensed_atom_number: int
    temperature_uk: int

    class Config:
        orm_mode = True
        validate_assignment = True


class PlotOutput(BaseModel):
    it_plot: Image

    class Config:
        orm_mode = True
        validate_assignment = True
        extra = "forbid"


class Output(BaseModel):
    input_id: Optional[int]
    values: PlotOutput | NonPlotOutput

    class Config:
        orm_mode = True
        validate_assignment = True


class BecOutput(Output):
    values: NonPlotOutput


class BarrierOutput(Output):
    ...


class TransistorOutput(Output):
    ...


class BraggOutput(Output):
    ...


class Paint1DOutput(Output):
    ...


class InputValues(BaseModel):
    end_time_ms: confloat(ge=0.0, le=80.0)
    image_type: ImageType
    time_of_flight_ms: confloat(ge=2.0, le=15.0)
    rf_evaporation: RfEvaporation
    optical_barriers: Optional[conlist(Barrier, min_items=1, max_items=5)]
    optical_landscape: Optional[OpticalLandscape]
    lasers: Optional[conlist(Laser, min_items=1, max_items=1)]

    @root_validator(skip_on_failure=True)
    def cross_validate(cls, values: dict):
        if list(
            filter(
                lambda time_ms: time_ms > values["end_time_ms"],
                values["rf_evaporation"].times_ms,
            )
        ):
            raise ValueError(
                "rf_evaporation.times_ms max values cannot exceed end_time_ms"
            )
        if values["optical_barriers"]:
            for index, optical_barrier in enumerate(values["optical_barriers"]):
                if list(
                    filter(
                        lambda time_ms: time_ms > values["end_time_ms"],
                        optical_barrier.times_ms,
                    )
                ):
                    raise ValueError(
                        f"optical_barriers[{index}].times_ms max values cannot exceed end_time_ms"
                    )
        if values["optical_landscape"]:
            for index, landscape in enumerate(values["optical_landscape"].landscapes):
                if landscape.time_ms > values["end_time_ms"]:
                    raise ValueError(
                        f"optical_landscape.landscapes[{index}].time_ms max value cannot exceed end_time_ms"
                    )
        if values["lasers"]:
            for laser_index, laser in enumerate(values["lasers"]):
                for pulse_index, pulse in enumerate(laser.pulses):
                    if list(
                        filter(
                            lambda time_ms: time_ms > values["end_time_ms"],
                            pulse.times_ms,
                        )
                    ):
                        raise ValueError(
                            f"lasers[{laser_index}].pulses[{pulse_index}].times_ms max values cannot exceed end_time_ms"
                        )
        return values


def require_time_of_flight(image_type: ImageType) -> ImageType:
    if image_type != ImageType.TIME_OF_FLIGHT:
        raise ValueError(f"image_type must be {ImageType.TIME_OF_FLIGHT}")
    return image_type


def require_optical_barriers(
    optical_barriers: List[Barrier] | None,
) -> List[Barrier] | None:
    if not optical_barriers:
        raise ValueError("optical_barriers is required")
    return optical_barriers


def require_optical_landscape(
    optical_landscape: OpticalLandscape | None,
) -> OpticalLandscape | None:
    if not optical_landscape:
        raise ValueError("optical_landscape is required")
    return optical_landscape


def require_lasers(lasers: List[Laser] | None) -> List[Laser] | None:
    if not lasers:
        raise ValueError("lasers is required")
    return lasers


class BecInputValues(InputValues):
    optical_barriers: None
    optical_landscape: None
    lasers: None

    _require_time_of_flight = validator("image_type", allow_reuse=True)(
        require_time_of_flight
    )


class BarrierInputValues(InputValues):
    optical_landscape: None
    lasers: None

    _require_optical_barriers = validator("optical_barriers", allow_reuse=True)(
        require_optical_barriers
    )


class TransistorInputValues(InputValues):
    _require_optical_barriers = validator("optical_barriers", allow_reuse=True)(
        require_optical_barriers
    )
    _require_optical_landscape = validator("optical_landscape", allow_reuse=True)(
        require_optical_landscape
    )
    _require_lasers = validator("lasers", allow_reuse=True)(require_lasers)


class BraggInputValues(InputValues):
    optical_barriers: None
    optical_landscape: None

    _require_lasers = validator("lasers", allow_reuse=True)(require_lasers)


class Paint1DInputValues(InputValues):
    _require_optical_barriers = validator("optical_barriers", allow_reuse=True)(
        require_optical_barriers
    )
    _require_optical_landscape = validator("optical_landscape", allow_reuse=True)(
        require_optical_landscape
    )
    _require_lasers = validator("lasers", allow_reuse=True)(require_lasers)


class Input(BaseModel):
    job_id: Optional[int]
    run: Optional[int]
    values: InputValues
    output: Optional[Output]
    notes: Optional[JobNote]

    class Config:
        validate_assignment = True
        orm_mode = True


class InputWithoutOutput(Input):
    class Config:
        fields = {"output": {"exclude": True}}


class BecInput(Input):
    values: BecInputValues
    output: Optional[BecOutput]


class BarrierInput(Input):
    values: BarrierInputValues
    output: Optional[BarrierOutput]


class TransistorInput(Input):
    values: TransistorInputValues
    output: Optional[TransistorOutput]


class BraggInput(Input):
    values: BraggInputValues
    output: Optional[BraggOutput]


class Paint1DInput(Input):
    values: Paint1DInputValues
    output: Optional[Paint1DOutput]


class JobBase(BaseModel):
    name: JobName
    job_type: JobType
    origin: Optional[JobOrigin]
    status: JobStatus = JobStatus.PENDING
    display: bool = True
    qpu_name: QPUName = QPUName.UNDEFINED
    input_count: Optional[conint(ge=1, le=30)]
    inputs: conlist(
        Input,
        min_items=1,
        max_items=30,
    )

    class Config:
        orm_mode = True
        use_enum_values = True
        validate_assignment = True


class JobCreate(JobBase):
    name: JobName
    job_type: JobType
    inputs: conlist(
        Input,
        min_items=1,
        max_items=30,
    )

    @root_validator
    def set_input_count_and_run(cls, values):
        """
        set the correct input count and run number
        """
        if "inputs" in values:
            input_len = len(values["inputs"])
            if values.get("input_count") is None or input_len > 1:
                values["input_count"] = input_len

            for i, input_value in enumerate(values["inputs"]):
                if input_len > 1 or not input_value.run:
                    input_value.run = i + 1
        return values

    @validator("inputs")
    def validate_inputs_match_job_type(cls, v, values):
        schema_validation_map = {
            JobType.TRANSISTOR: TransistorInput,
            JobType.PAINT_1D: Paint1DInput,
            JobType.BARRIER: BarrierInput,
            JobType.BRAGG: BraggInput,
            JobType.BEC: BecInput,
        }
        for job_input in v:
            schema_validation_map.get(values["job_type"], Input)(**job_input.dict())
        return v


class ResponseInput(BaseModel):
    job_id: Optional[int]
    run: Optional[int]
    values: object
    output: Optional[object]
    notes: Optional[JobNote]

    class Config:
        orm_mode = True


class JobResponse(JobBase):
    external_id: UUID
    status: JobStatus
    qpu: Optional[QPUBase]
    time_submit: datetime
    inputs: List[ResponseInput]
    failed_inputs: List[int] = []


class JobInputsResponse(JobBase):
    external_id: UUID
    status: JobStatus
    qpu_name: QPUName = QPUName.UNDEFINED
    time_submit: datetime
    inputs: List[InputWithoutOutput]
    failed_inputs: List[int] = []


class PaginatedJobsResponse(BaseModel):
    name: JobName
    job_type: JobType
    origin: Optional[JobOrigin]
    external_id: UUID
    qpu_name: QPUName = QPUName.UNDEFINED
    status: JobStatus
    time_submit: datetime

    class Config:
        orm_mode = True
        use_enum_values = True


class Job(JobBase):
    job_id: UUID
    status: JobStatus = JobStatus.PENDING
    display: bool = True


class ExternalId(BaseModel):
    id: UUID


class UpdateJobDisplay(BaseModel):
    job_external_id: UUID
    display: bool = True

    class Config:
        validate_assignment = True


class JobCreateResponse(BaseModel):
    job_id: UUID
    queue_position: int
    est_time: int


def interpolation_to_kind(interpolation: InterpolationType) -> str:
    """Convert our InterpolationType to something scipy can understand

    Args:
        interpolation (InterpolationType): Job primitive interpolation type

    Returns:
        str: 'kind' string to be used by scipy's interp1d
    """
    if interpolation == "OFF":  # for compatibilty with existing options
        kind = "zero"
    elif interpolation == "STEP":  # ditto
        kind = "previous"
    elif interpolation == "SMOOTH":  # ditto^2
        kind = "cubic"
    else:
        kind = interpolation.lower()
    return kind


def interpolate_1D(
    xs: list,
    ys: list,
    x: float,
    interpolation: InterpolationType = InterpolationType.LINEAR,
) -> float:
    """Interpolates a 1D list of pairs [xs, ys] at the evaluation point x. Extrapolation requests return 0.0.

    Args:
        xs (list): List of x values
        ys (list): List of y values (of the same length as xs)
        x (float): Desired x-coordinate to evaluate the resulting interpolation function.
        interpolation (InterpolationType, optional): Interpolation style. Defaults to InterpolationType.LINEAR.

    Returns:
        float: Interpolation function value at the specified x.
    """
    f = interp1d(
        xs,
        ys,
        kind=interpolation_to_kind(interpolation),
        bounds_error=False,
        fill_value=(0.0, 0.0),
    )
    return f(x)[()]  # extract value


def interpolate_1D_list(
    xs: list,
    ys: list,
    x_values: list,
    interpolation: InterpolationType = InterpolationType.LINEAR,
) -> list:
    """Interpolates a 1D list of pairs [xs, ys] at the evaluation points given by xs. Extrapolation requests return 0.0.

    Args:
        xs (list): List of x values
        ys (list): List of y values (of the same length as xs)
        xs (list): Desired x-coordinates to evaluate the resulting interpolation function.
        interpolation (InterpolationType, optional): Interpolation style. Defaults to InterpolationType.LINEAR.

    Returns:
        list: Floating point values corresponding to evaluation of the interpolation function value at the specified xs.
    """
    f = interp1d(
        xs,
        ys,
        kind=interpolation_to_kind(interpolation),
        bounds_error=False,
        fill_value=(0.0, 0.0),
    )
    return list(f(x_values))


class Plotter:
    def plot_points_and_line(
        x_data_points: list,
        y_data_points: list,
        x_data_line: list,
        y_data_line: list,
        x_limits: list,
        y_limits: list,
        x_label: str = "",
        y_label: str = "",
        title: str = "",
    ):
        """A generic plotting function for common 2D plots

        Args:
            x_data_points (list): List of x-values for which the function plots discrete points.
            y_data_points (list): List of y-values for which the function plots discrete points.
            x_data_line (list): List of x-values for which the function plots a line.
            y_data_line (list): List of y-values for which the function plots a line
            x_limits (list): Two-element array specifying the plot domain [x_min, x_max]
            y_limits (list): Two-element array specifying the plot range [y_min, y_max]
            x_label (str, optional): Label for the x-axis. Defaults to "".
            y_label (str, optional): Label for the y-axis. Defaults to "".
            title (str, optional): Label for plot. Defaults to "".
        """
        ax = plt.gca()
        color = next(ax._get_lines.prop_cycler)["color"]
        plt.plot(x_data_line, y_data_line, color=color)
        plt.plot(x_data_points, y_data_points, ".", color=color)
        plt.xlabel(x_label, labelpad=6)
        plt.ylabel(y_label, labelpad=6)
        plt.title(title)
        plt.xlim(x_limits)
        plt.ylim(y_limits)
        plt.show()

    def plot_intensity(x_limits: list, y_limits: list, pulses: list, plot_times: list):
        # each pulse has independent interpolation styles, so need to independently sum over them...
        pulse_times = []
        pulse_intensities = []
        intensities = [0.0] * len(plot_times)
        print(len(plot_times))
        print(len(intensities))
        for pulse in pulses:
            pulse_times.extend(pulse.times_ms)
            pulse_intensities.extend(pulse.intensities_mw_per_cm2)
            intensities = [
                sum(x) for x in zip(intensities, pulse.get_intensities(plot_times))
            ]
        plt.plot(pulse_times, pulse_intensities, ".")
        plt.plot(plot_times, intensities)
        if x_limits is None:
            x_limits = [min(plot_times) - 1, max(plot_times) + 1]
        if y_limits is None:
            y_limits = [min(intensities) - 1, max(intensities) + 1]
        plt.xlim(x_limits)
        plt.ylim(y_limits)
        plt.xlabel("time (ms)")
        plt.ylabel("intensity (mW / cm^2)")
        plt.show()
