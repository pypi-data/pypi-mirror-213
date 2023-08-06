from datetime import date as date_
from pydantic import condecimal, validator
from sqlalchemy import ForeignKeyConstraint as ForeignKeyConstraint_
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional


def ForeignKeyConstraint(*args, **kwargs):
    return ForeignKeyConstraint_(
        *args,
        **kwargs,
        onupdate="CASCADE",
        ondelete="RESTRICT",
    )


"""
Measurement-level models

"""


class MeasurementDetails(SQLModel, table=True):
    __tablename__ = "measurement_details"

    measurement_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    date: date_ = Field(
        nullable=False,
        description="nominal date for measurement",
    )
    location: str = Field(
        nullable=False,
        description="location of measurement",
    )
    purpose: Optional[str] = Field(
        default=None,
        description="purpose of measurement",
    )
    operator_name: str = Field(
        nullable=False,
        description="operator's name",
    )
    tow_vehicle: str = Field(
        nullable=False,
        description="tow vehicle description",
    )
    target_speed_kph: int = Field(
        nullable=False,
        description="target speed in km/h",
    )
    wheel_track: str = Field(
        nullable=False,
        description="wheel track(s) measured (e.g. 'left', 'right', 'both')",
    )
    hours_since_last_rain: int = Field(
        nullable=False,
        description="hours since last rain event",
    )
    wav_scale: condecimal(decimal_places=1) = Field(
        nullable=False,
        description=(
            "scale factor to apply to the raw wav file data (-1 to + 1 range) "
            "to convert the data back into volts."
        ),
    )
    notes: Optional[str] = Field(
        default=None,
        description="other notes about the measurement",
    )

    results_sets: List["ResultsSet"] = Relationship()
    wheel_bay_details: List["MeasurementWheelBayDetails"] = Relationship()


class MeasurementWheelBayDetails(SQLModel, table=True):
    """
    Measurement-level wheel bay details for a given results set. Each results
    set can have up to two wheel bay entries.
    """

    __tablename__ = "measurement_wheel_bay_details"
    __table_args__ = (
        ForeignKeyConstraint(
            ["measurement_id"],
            ["measurement_details.measurement_id"],
        ),
    )

    measurement_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    wheel_bay_name: str = Field(
        primary_key=True,
        description="wheel bay name ('left' or 'right')",
    )
    wheel_bay_configuration_details: str = Field(
        nullable=False,
        description="description of the wheel bay configuration",
    )
    wheel_bay_calibration_date: date_ = Field(
        nullable=False, description="wheel bay / device correction calibration date"
    )
    tyre: str = Field(
        nullable=False,
        description="tyre type (e.g., P1, H1, etc.)",
    )
    tyre_purchase_date: date_ = Field(
        nullable=False,
        description="purchase date of the tyre",
    )
    hardness: condecimal(decimal_places=1) = Field(
        nullable=False,
        description="tyre hardness in Shore A",
    )
    hardness_date: date_ = Field(
        nullable=False,
        description="date of hardness measurement",
    )

    microphone_details: List["MeasurementMicrophoneDetails"] = Relationship()
    accelerometer_details: List["MeasurementAccelerometerDetails"] = Relationship()
    device_corrections: List["DeviceCorrection"] = Relationship()


class MeasurementMicrophoneDetails(SQLModel, table=True):
    """
    Measurement-level microphone details.
    """

    __tablename__ = "measurement_microphone_details"
    __table_args__ = (
        ForeignKeyConstraint(
            ["measurement_id", "wheel_bay_name"],
            [
                "measurement_wheel_bay_details.measurement_id",
                "measurement_wheel_bay_details.wheel_bay_name",
            ],
        ),
    )

    measurement_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    wheel_bay_name: Optional[str] = Field(
        default=None,
        primary_key=True,
    )
    microphone_position: int = Field(
        primary_key=True,
        description="microphone position (1-6) as per ISO 11819-2:2017",
    )
    microphone_serial_number: str = Field(
        nullable=False,
        description="microphone serial number",
    )
    microphone_sensitivity_mv_pa: condecimal(decimal_places=2) = Field(
        nullable=False,
        description="microphone sensitivity in mV/Pa",
    )
    microphone_calibration_date: date_ = Field(
        nullable=False,
        description="microphone calibration date",
    )
    wav_file_channel_number: int = Field(
        nullable=False,
        description=(
            "channel number in the wav file corresponding to the microphone " "position"
        ),
    )


class MeasurementAccelerometerDetails(SQLModel, table=True):
    __tablename__ = "measurement_accelerometer_details"
    __table_args__ = (
        ForeignKeyConstraint(
            ["measurement_id", "wheel_bay_name"],
            [
                "measurement_wheel_bay_details.measurement_id",
                "measurement_wheel_bay_details.wheel_bay_name",
            ],
        ),
    )

    measurement_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    wheel_bay_name: Optional[str] = Field(
        default=None,
        primary_key=True,
    )
    accelerometer_position: str = Field(
        primary_key=True,
        description="accelerometer position ('chassis' or 'axle')",
    )
    accelerometer_serial_number: str = Field(
        nullable=False,
        description="accelerometer serial number",
    )
    accelerometer_sensitivity_mv_g: condecimal(decimal_places=2) = Field(
        nullable=False,
        description="accelerometer sensitivity in mV/g",
    )
    wav_file_channel_number: int = Field(
        nullable=False,
        description=(
            "channel number in the wav file corresponding to the accelerometer"
        ),
    )


class DeviceCorrection(SQLModel, table=True):
    """
    Device corrections used when calculating LCPX (as per ISO 11819-2:2017
    A.2). Each row represents a single wheel bay / frequency combination, so
    there will be multiple rows that apply to each wheel bay.
    """

    __tablename__ = "device_correction"
    __table_args__ = (
        ForeignKeyConstraint(
            ["measurement_id", "wheel_bay_name"],
            [
                "measurement_wheel_bay_details.measurement_id",
                "measurement_wheel_bay_details.wheel_bay_name",
            ],
        ),
    )

    measurement_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    wheel_bay_name: Optional[str] = Field(
        default=None,
        primary_key=True,
    )
    frequency_hz: condecimal(decimal_places=1) = Field(
        primary_key=True,
        description="one-third octave band centre frequency in Hz",
    )
    correction_db: float = Field(
        nullable=False,
        description="device correction in dB",
    )


"""
Session-level (results set) models

These models related to all road segment results from a measurement session.
The top-level model is the ResultsSet model.

"""


class ResultsSet(SQLModel, table=True):
    __tablename__ = "results_set"
    __table_args__ = (
        ForeignKeyConstraint(
            ["measurement_id"],
            ["measurement_details.measurement_id"],
        ),
    )

    measurement_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    results_set_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    software_version: str = Field(
        nullable=False,
        description=("processing software version used to generate the results set"),
    )
    segment_length_m: Optional[condecimal(decimal_places=1)] = Field(
        default=None,
        description=(
            "length of the road segment in metres. Set to None if results use "
            "a variable segment length."
        ),
    )
    reference_speed_kph: int = Field(
        nullable=False,
        description="reference speed in km/h",
    )
    speed_coefficient: condecimal(decimal_places=1) = Field(
        nullable=False,
        description="speed coefficient used to calculate speed correction",
    )
    reference_temperature: condecimal(decimal_places=2) = Field(
        nullable=False,
        description="reference temperature in deg C",
    )
    temperature_correction_type: str = Field(
        nullable=False,
        description="temperature correction basis ('air', 'tyre' or 'road')",
    )
    temperature_coefficient: condecimal(decimal_places=4) = Field(
        nullable=False,
        description=(
            "temperature coefficient used to calculate the temperature " "correction"
        ),
    )
    gps_acceleration_threshold_kph_sec: condecimal(decimal_places=2) = Field(
        nullable=False,
        description=(
            "threshold for determining if the GPS acceleration is valid in " "km/h/sec"
        ),
    )
    rsrp_database: str = Field(
        nullable=False,
        description=("name of the Rs/Rp database used to generate the results set"),
    )
    rsrp_date: date_ = Field(
        nullable=False,
        description="date that the Rs/Rp database was accessed",
    )
    include_in_ramm: bool = Field(
        default=False,
        description="whether or not to include the results set in RAMM",
    )
    include_in_map_viewer: bool = Field(
        default=False,
        description=("whether or not to include the results set in the map service"),
    )
    notes: Optional[str] = Field(
        default=None,
        description="reason for the results set being generated",
    )

    segment_details: List["SegmentDetails"] = Relationship()
    wheel_bay_details: List["ResultsSetWheelBayDetails"] = Relationship()


class ResultsSetWheelBayDetails(SQLModel, table=True):
    """
    Results set (session) level wheel bay details.
    """

    __tablename__ = "results_set_wheel_bay_details"
    __table_args__ = (
        ForeignKeyConstraint(
            ["measurement_id", "results_set_id"],
            [
                "results_set.measurement_id",
                "results_set.results_set_id",
            ],
        ),
    )

    measurement_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    results_set_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    wheel_bay_name: str = Field(
        primary_key=True,
        description="wheel bay name ('left' or 'right')",
    )
    reference_hardness: condecimal(decimal_places=1) = Field(
        nullable=False,
        description="reference hardness in Shore A",
    )
    hardness_coefficient: condecimal(decimal_places=3) = Field(
        nullable=False,
        description=(
            "hardness coefficient in dB/Shore A used to calculate the "
            "hardness correction"
        ),
    )
    hardness_correction_db: float = Field(
        nullable=False,
        description="hardness correction value in dB",
    )
    microphone_details: List["ResultsSetMicrophoneDetails"] = Relationship()


class ResultsSetMicrophoneDetails(SQLModel, table=True):
    """
    Results set (session) level microphone details.
    """

    __tablename__ = "results_set_microphone_details"
    __table_args__ = (
        ForeignKeyConstraint(
            ["measurement_id", "results_set_id", "wheel_bay_name"],
            [
                "results_set_wheel_bay_details.measurement_id",
                "results_set_wheel_bay_details.results_set_id",
                "results_set_wheel_bay_details.wheel_bay_name",
            ],
        ),
    )

    measurement_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    results_set_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    wheel_bay_name: Optional[str] = Field(
        default=None,
        primary_key=True,
    )
    microphone_position: int = Field(
        primary_key=True,
        description="microphone position (1-6) as per ISO 11819-2:2017",
    )
    used_in_wheel_bay_results: bool = Field(
        nullable=False,
        description="used when calculating the overall results for the wheel bay",
    )


"""
Segment-level (results set) models.

"""


class SegmentDetails(SQLModel, table=True):
    """
    Contains the segment level details associated with the results set.
    """

    __tablename__ = "segment_details"
    __table_args__ = (
        ForeignKeyConstraint(
            ["measurement_id", "results_set_id"],
            [
                "results_set.measurement_id",
                "results_set.results_set_id",
            ],
        ),
    )

    measurement_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    results_set_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )

    segment_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    wav_path: str = Field(
        nullable=False,
        description=(
            "path to the wav file associated with the segment result "
            "(relative to the SharePoint measurement files folder)"
        ),
    )
    run_number: int = Field(
        nullable=False,
        description=(
            "run number as per the measurement files. This cannot be relied "
            "on when determining the number of runs across a given road "
            "segment. Instead, count the number of unique "
            "road_id/start_m/end_m/lane_number combinations associated with "
            "the results set."
        ),
    )
    run_segment_count: int = Field(
        nullable=False,
        description=(
            "the run segment counter as per the measurement files. This "
            "is used to indicate a pause in a run. This cannot be relied "
            "on when determining the number of runs across a given road "
            "segment. Instead, count the number of unique "
            "road_id/start_m/end_m/lane_number combinations associated with "
            "the results set."
        ),
    )
    road_id: int = Field(
        nullable=False,
        description="RAMM road ID",
    )
    start_m: condecimal(decimal_places=1) = Field(
        nullable=False,
        description=(
            "start position of the road segment in metres (Rs/Rp route "
            "position). 'start_m' is always lower than 'end_m'."
        ),
    )
    end_m: condecimal(decimal_places=1) = Field(
        nullable=False,
        description=(
            "end position of the road segment in metres (Rs/Rp route "
            "position). 'end_'m' is always higher than 'start_m'."
        ),
    )
    length_m: condecimal(decimal_places=1) = Field(
        nullable=False,
        description="length of the road segment in metres",
    )
    lane: str = Field(
        nullable=False,
        description="RAMM lane number (e.g. 'L1', 'L2', 'R1', 'R2', etc)",
    )
    start_sample: int = Field(
        nullable=False,
        description=(
            "wav sample number corresponding to the start of the road "
            "segment. This is the same side of the road segment as 'start_m', "
            "meaning that 'start_sample' may be higher than 'end_sample'."
        ),
    )
    end_sample: int = Field(
        nullable=False,
        description=(
            "wav sample number corresponding to the end of the road "
            "segment. This is the same side of the road segment as 'end_m', "
            "meaning that 'end_sample' may be lower than 'start_sample'."
        ),
    )
    speed_kph: float = Field(
        nullable=False,
        description="average speed across the road segment in km/h",
    )
    air_temperature: float = Field(
        nullable=False,
        description="average air temperature across the road segment in deg C",
    )
    speed_correction_db: float = Field(
        nullable=False,
        description="speed correction in dB",
    )
    temperature_correction_db: float = Field(
        nullable=False,
        description="temperature correction in dB",
    )
    start_latitude: float = Field(
        nullable=False,
        description="latitude of segment start point",
    )
    start_longitude: float = Field(
        nullable=False,
        description="longitude of segment start point",
    )
    end_latitude: float = Field(
        nullable=False,
        description="latitude of segment end point",
    )
    end_longitude: float = Field(
        nullable=False,
        description="longitude of segment end point",
    )
    passing_truck_flag: Optional[bool] = Field(
        default=False,
        description="passing truck (true/false)",
    )
    other_flag: Optional[bool] = Field(
        default=False,
        description="other flag (true/false)",
    )
    valid: bool = Field(
        nullable=False,
        description=(
            "indicates whether the road segment results are valid or not, "
            "based on the speed and any event flags"
        ),
    )

    wheel_bay_details: List["SegmentWheelBayDetails"] = Relationship()

    @validator("start_m", "end_m", "length_m", pre=True)
    def round_1(cls, v):
        return round(v, 1) if v is not None else None


class SegmentWheelBayDetails(SQLModel, table=True):
    """
    Segment-level (results set) wheel bay details.
    """

    __tablename__ = "segment_wheel_bay_details"
    __table_args__ = (
        ForeignKeyConstraint(
            ["measurement_id", "results_set_id", "segment_id"],
            [
                "segment_details.measurement_id",
                "segment_details.results_set_id",
                "segment_details.segment_id",
            ],
        ),
    )

    measurement_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    results_set_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    segment_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    wheel_bay_name: Optional[str] = Field(
        default=None,
        primary_key=True,
        description="wheel bay name ('left' or 'right')",
    )
    road_temperature: Optional[float] = Field(
        default=None,
        description="Mean road surface temperature for the segment in °C)",
    )
    tyre_temperature: Optional[float] = Field(
        default=None,
        description="Mean tyre temperature for the segment in °C",
    )
    laeq_db: Optional[float] = Field(
        default=None,
        description="LAeq for the wheel bay in dB (no CPX corrections applied)",
    )
    lcpx_db: Optional[float] = Field(
        default=None,
        description="LCPX for the wheel bay in dB",
    )

    microphone_details: List["SegmentMicrophoneDetails"] = Relationship()
    wheel_bay_third_octave_levels: List["WheelBayThirdOctaveLevels"] = Relationship()
    wheel_bay_texture_results: Optional[List["WheelBayTextureResults"]] = Relationship()


class SegmentMicrophoneDetails(SQLModel, table=True):
    """
    Segment-level (results set) microphone details.
    """

    __tablename__ = "segment_microphone_details"
    __table_args__ = (
        ForeignKeyConstraint(
            [
                "measurement_id",
                "results_set_id",
                "segment_id",
                "wheel_bay_name",
            ],
            [
                "segment_wheel_bay_details.measurement_id",
                "segment_wheel_bay_details.results_set_id",
                "segment_wheel_bay_details.segment_id",
                "segment_wheel_bay_details.wheel_bay_name",
            ],
        ),
    )

    measurement_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    results_set_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    segment_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    wheel_bay_name: Optional[str] = Field(
        default=None,
        primary_key=True,
    )
    microphone_position: int = Field(
        primary_key=True,
        description="microphone position (1-6) as per ISO 11819-2:2017)",
    )
    laeq_db: float = Field(
        nullable=False,
        description="LAeq for the microphone position in dB (no CPX corrections applied)",
    )

    microphone_third_octave_levels: List["MicrophoneThirdOctaveLevels"] = Relationship()


class MicrophoneThirdOctaveLevels(SQLModel, table=True):
    """
    One-third octave band sound pressure levels for each microphone position
    in the wheel bay, measured across one road segment.
    """

    __tablename__ = "microphone_third_octave_levels"
    __table_args__ = (
        ForeignKeyConstraint(
            [
                "measurement_id",
                "results_set_id",
                "segment_id",
                "wheel_bay_name",
                "microphone_position",
            ],
            [
                "segment_microphone_details.measurement_id",
                "segment_microphone_details.results_set_id",
                "segment_microphone_details.segment_id",
                "segment_microphone_details.wheel_bay_name",
                "segment_microphone_details.microphone_position",
            ],
        ),
    )

    measurement_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    results_set_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    segment_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    wheel_bay_name: Optional[str] = Field(
        default=None,
        primary_key=True,
    )
    microphone_position: int = Field(
        primary_key=True,
    )
    frequency_hz: condecimal(decimal_places=1) = Field(
        primary_key=True,
        description="one-third octave band centre frequency in Hz",
    )
    leq_db: float = Field(
        nullable=False,
        description="microphone Leq in dB across the road segment",
    )
    laeq_db: float = Field(
        nullable=False,
        description="microphone LAeq in dB across the road segment",
    )


class WheelBayThirdOctaveLevels(SQLModel, table=True):
    __tablename__ = "wheel_bay_third_octave_levels"
    __table_args__ = (
        ForeignKeyConstraint(
            [
                "measurement_id",
                "results_set_id",
                "segment_id",
                "wheel_bay_name",
            ],
            [
                "segment_wheel_bay_details.measurement_id",
                "segment_wheel_bay_details.results_set_id",
                "segment_wheel_bay_details.segment_id",
                "segment_wheel_bay_details.wheel_bay_name",
            ],
        ),
    )

    measurement_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    results_set_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    segment_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    wheel_bay_name: Optional[str] = Field(
        default=None,
        primary_key=True,
    )
    frequency_hz: condecimal(decimal_places=1) = Field(
        primary_key=True,
        description="one-third octave band centre frequency in Hz",
    )
    leq_db: float = Field(
        nullable=False,
        description=(
            "energy-based average of the one-third octave Leq of all "
            "microphone positions within the enclosure in dB. Calculated by "
            "subtracting the A weighting from the one-third octave LAeq (see "
            "'laeq_db' field) for the wheel bay."
        ),
    )
    laeq_db: float = Field(
        nullable=False,
        description=(
            "energy-based average of the one-third octave LAeq of all "
            "microphone positions within the enclosure in dB (refer ISO "
            "11819-2:2017 Formula C.1 / C.7)"
        ),
    )
    lcpx_db: float = Field(
        nullable=False,
        description=(
            "one-third octave LCPX with all corrections applied (including "
            "the device-related correction) in dB (refer ISO 11819-2:2017 "
            "Formula C.8 and C.9)"
        ),
    )


class WheelBayTextureResults(SQLModel, table=True):

    """
    Wheel bay texture results for each wheel bay in the enclosure.
    """

    __tablename__ = "wheel_bay_texture_results"
    __table_args__ = (
        ForeignKeyConstraint(
            [
                "measurement_id",
                "results_set_id",
                "segment_id",
                "wheel_bay_name",
            ],
            [
                "segment_wheel_bay_details.measurement_id",
                "segment_wheel_bay_details.results_set_id",
                "segment_wheel_bay_details.segment_id",
                "segment_wheel_bay_details.wheel_bay_name",
            ],
        ),
    )

    measurement_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    results_set_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    segment_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    wheel_bay_name: Optional[str] = Field(
        default=None,
        primary_key=True,
    )
    laser_sample_start: int = Field(
        nullable=False,
        description=(
            "laser sample number corresponding to the start of the road "
            "segment. This is the same side of the road segment as 'start_m', "
            "meaning that 'laser_start_sample' may be higher than "
            "'laser_end_sample'."
        ),
    )
    laser_sample_end: int = Field(
        nullable=False,
        description=(
            "laser sample number corresponding to the end of the road "
            "segment. This is the same side of the road segment as 'end_m', "
            "meaning that 'laser_end_sample' may be lower than "
            "'laser_start_sample'."
        ),
    )
    mpd_mm: float = Field(
        nullable=False,
        description=(
            "mean profile depth for road segment in mm, calculated from all "
            "valid mean segment depth results within the road segment"
        ),
    )
    stdev_mm: float = Field(
        nullable=False,
        description=(
            "standard deviation in mm of all valid mean segment depths within "
            "the road segment"
        ),
    )
    valid: bool = Field(
        nullable=False,
        description="validity of the mean profile depth result for the segment",
    )
