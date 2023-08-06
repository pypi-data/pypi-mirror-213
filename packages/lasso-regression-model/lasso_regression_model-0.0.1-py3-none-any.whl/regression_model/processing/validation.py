from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from regression_model.config.core import config
from regression_model.processing.datapreprocessor import preprocess_dataframe  # noqa


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    # new_vars_with_na = [
    #     var
    #     for var in config.model_config.features
    #     if var
    #     # not in config.model_config.categorical_vars_with_na_frequent
    #     # + config.model_config.categorical_vars_with_na_missing
    #     + config.model_config.numerical_vars_with_na
    #     and validated_data[var].isnull().sum() > 0
    # ]
    new_vars_with_na = [var
                        for var in config.model_config.features
                        if validated_data[var].isnull().sum() > 0]
    validated_data.dropna(subset=new_vars_with_na, inplace=True)
    return validated_data


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""
    # input_data = pd.DataFrame(input_data, parse_dates=config.model_config.date_features)
    # input_data = preprocess_dataframe(input_data)
    # drop target
    relevant_data = input_data[config.model_config.features].copy()
    # By Passing for now
    # validated_data = drop_na_inputs(input_data=relevant_data)
    validated_data = relevant_data
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class DataInputSchema(BaseModel):
    Location1: Optional[str]
    Type: Optional[str]
    Bedrooms: Optional[float]
    Bathrooms: Optional[float]
    Size_in_SqYds: Optional[float]
    Price_in_millions: Optional[float]
    Parking_Spaces: Optional[int]
    Floors_in_Building: Optional[float]
    Elevators: Optional[float]
    Lobby_in_Building: Optional[int]
    Double_Glazed_Windows: Optional[int]
    Central_Air_Conditioning: Optional[int]
    Central_Heating: Optional[int]
    Waste_Disposal: Optional[int]
    Furnished: Optional[int]
    Service_Elevators_in_Building: Optional[int]
    Flooring: Optional[int]
    Electricity_Backup: Optional[int]
    Servant_Quarters: Optional[int]
    Study_Room: Optional[int]
    Prayer_Room: Optional[int]
    Powder_Room: Optional[int]
    Gym: Optional[int]
    Lounge_or_Sitting_Room: Optional[int]
    Laundry_Room: Optional[int]
    Business_Center_or_Media_Room_in_Building: Optional[int]
    Satellite_or_Cable_TV_Ready: Optional[int]
    Broadband_Internet_Access: Optional[int]
    Intercom: Optional[int]
    Conference_Room_in_Building: Optional[int]
    Community_Swimming_Pool: Optional[int]
    Community_Lawn_or_Garden: Optional[int]
    Community_Gym: Optional[int]
    Community_Center: Optional[int]
    First_Aid_or_Medical_Centre: Optional[int]
    Day_Care_center: Optional[int]
    Kids_Play_Area: Optional[int]
    Mosque: Optional[int]
    Barbeque_Area: Optional[int]
    Lawn_or_Garden: Optional[int]
    Swimming_Pool: Optional[int]
    Sauna: Optional[int]
    Jacuzzi: Optional[int]
    Nearby_Schools: Optional[int]
    Nearby_Hospital: Optional[int]
    Nearby_Shopping_Malls: Optional[int]
    Nearby_Restaurants: Optional[int]
    Nearby_Public_Transport_Service: Optional[int]
    Other_Nearby_Places: Optional[int]
    Security_Staff: Optional[int]
    Maintainance_Staff: Optional[int]
    Laundry_or_Dry_Cleaning_Facility: Optional[int]
    Facilities_for_Disabled: Optional[int]
    # this one is only to calculate temporal variable:
    Built_in_year_year: Optional[float]


class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]
