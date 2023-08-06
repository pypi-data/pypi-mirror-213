from datetime import datetime
from typing import Optional, Tuple

import pandas as pd
import pyarrow.parquet as pq
from arize.utils.types import Environments
from pyarrow import flight
from tqdm import tqdm

from ..utils.validation import Validator
from .endpoint import Endpoint
from .session import Session


class ArizeExportClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        arize_profile: Optional[str] = None,
        arize_config_path: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
    ) -> None:
        """
        Initializes the Arize Export Client.

        Arguments:
        ----------
            api_key (str, optional): Arize provided personal API key associated with your user profile,
                located on the API Explorer page. API key is required to initiate a new client, it can
                be passed in explicitly, or set up as an environment variable or in profile file.
            arize_profile (str, optional): profile name for ArizeExportClient credentials and endpoint.
                Defaults to 'default'.
            arize_config_path (str, optional): path to the config file that stores ArizeExportClient
                credentials and endpoint. Defaults to '~/.arize'.
            host (str, optional): URI endpoint host to send your export request to Arize AI. Defaults to
                "https://flight.arize.com".
            port (int, optional): URI endpoint port to send your export request to Arize AI. Defaults to
                443.
        """
        self._session = Session(api_key, arize_profile, arize_config_path, host, port)
        self.done = False

    def __call__(self, query: str) -> flight.FlightStreamReader:
        arize_flight_endpoint = Endpoint(self._session)
        flight_client = arize_flight_endpoint.connect()
        reader = arize_flight_endpoint.execute_query(flight_client, query)
        return reader

    def export_model_to_df(
        self,
        space_id: str,
        model_id: str,
        environment: Environments,
        start_time: datetime,
        end_time: datetime,
        include_actuals: Optional[bool] = False,
        model_version: Optional[str] = "",
        batch_id: Optional[str] = "",
    ) -> pd.DataFrame:
        """
        Exports data of a specific model in the Arize platform to a pandas dataframe for a defined
        time interval and model environment, optionally by model version and/or batch id.

        Arguments:
        ----------
            space_id (str): The id for the space where to export models from, can be retrieved from
                the url of the Space Overview page in the Arize UI.
            model_id (str): The name of the model to export, can be found in the Model Overview
                tab in the Arize UI.
            environment (Environments): The environment for the model to export (can be Production,
                Training, or Validation).
            start_time (datetime): The start time for the data to export for the model, start time
                is inclusive. Time interval has hourly granularity.
            end_time (datetime): The end time for the data to export for the model, end time is not
                inclusive. Time interval has hourly granularity.
            include_actuals (bool, optional): An optional input to indicate whether to include actuals
                / ground truth in the data to export. `include_actuals` only applies to the Production
                environment and defaults to 'False'.
            model_version (str, optional): An optional input to indicate the version of the model to
                export. Model versions for all model environments can be found in the Datasets tab on
                the model page in the Arize UI.
            batch_id (str, optional): An optional input to indicate the batch name of the model to export.
                Batches only apply to the Validation environment, and can be found in the Datasets tab on
                the model page in the Arize UI.

        Returns:
        --------
            A pandas dataframe
        """
        stream_reader, num_recs = self.get_model_stream_reader(
            space_id=space_id,
            model_id=model_id,
            environment=environment,
            start_time=start_time,
            end_time=end_time,
            include_actuals=include_actuals,
            model_version=model_version,
            batch_id=batch_id,
        )
        if stream_reader is None:
            return pd.DataFrame()
        progress_bar = self.get_progress_bar(num_recs)
        list_of_df = []
        while True:
            try:
                flight_batch = stream_reader.read_chunk()
                record_batch = flight_batch.data
                data_to_pandas = record_batch.to_pandas()
                list_of_df.append(data_to_pandas)
                progress_bar.update(data_to_pandas.shape[0])
            except StopIteration:
                self.done = True
                break
        progress_bar.close()
        return pd.concat(list_of_df)

    def export_model_to_parquet(
        self,
        path: str,
        space_id: str,
        model_id: str,
        environment: Environments,
        start_time: datetime,
        end_time: datetime,
        include_actuals: Optional[bool] = False,
        model_version: Optional[str] = "",
        batch_id: Optional[str] = "",
    ) -> None:
        """
        Exports data of a specific model in the Arize platform to a parquet file for a defined time
        interval and model environment, optionally by model version and/or batch id.

        Arguments:
        ----------
            path (str): path to the file to store exported data. File must be in parquet format and
                has a '.parquet' extension.
            space_id (str): The id for the space where to export models from, can be retrieved from
                the url of the Space Overview page in the Arize UI.
            model_id (str): The name of the model to export, can be found in the Model Overview
                tab in the Arize UI.
            environment (Environments): The environment for the model to export (can be Production,
                Training, or Validation).
            start_time (datetime): The start time for the data to export for the model, start time
                is inclusive. Time interval has hourly granularity.
            end_time (datetime): The end time for the data to export for the model, end time is not
                inclusive. Time interval has hourly granularity.
            include_actuals (bool, optional): An optional input to indicate whether to include actuals
                / ground truth in the data to export. `include_actuals` only applies to the Production
                environment and defaults to 'False'.
            model_version (str, optional): An optional input to indicate the version of the model to
                export. Model versions for all model environments can be found in the Datasets tab on
                the model page in the Arize UI.
            batch_id (str, optional): An optional input to indicate the batch name of the model to export.
                Batches only apply to the Validation environment, and can be found in the Datasets tab on
                the model page in the Arize UI.

        Returns:
        --------
            None
        """
        Validator.validate_input_type(path, "path", str)
        stream_reader, num_recs = self.get_model_stream_reader(
            space_id=space_id,
            model_id=model_id,
            environment=environment,
            start_time=start_time,
            end_time=end_time,
            include_actuals=include_actuals,
            model_version=model_version,
            batch_id=batch_id,
        )
        if stream_reader is None:
            return None
        progress_bar = self.get_progress_bar(num_recs)
        with pq.ParquetWriter(path, schema=stream_reader.schema) as writer:
            while True:
                try:
                    flight_batch = stream_reader.read_chunk()
                    record_batch = flight_batch.data
                    writer.write_batch(record_batch)
                    progress_bar.update(record_batch.num_rows)
                except StopIteration:
                    self.done = True
                    break
        progress_bar.close()

    def get_model_stream_reader(
        self,
        space_id: str,
        model_id: str,
        environment: Environments,
        start_time: datetime,
        end_time: datetime,
        include_actuals: Optional[bool] = False,
        model_version: Optional[str] = "",
        batch_id: Optional[str] = "",
    ) -> Tuple[flight.FlightStreamReader, int]:
        Validator.validate_input_type(space_id, "space_id", str)
        Validator.validate_input_type(model_id, "model_id", str)
        Validator.validate_input_type(environment, "environment", Environments)
        Validator.validate_input_type(include_actuals, "include_actuals", bool)
        Validator.validate_input_type(start_time, "start_time", datetime)
        Validator.validate_input_type(end_time, "end_time", datetime)
        Validator.validate_input_type(model_version, "model_version", str)
        Validator.validate_input_type(batch_id, "batch_id", str)

        if environment == Environments.PRODUCTION:
            env = "PRODUCTION"
        elif environment == Environments.TRAINING:
            env = "TRAINING"
        elif environment == Environments.VALIDATION:
            env = "VALIDATION"
        else:
            raise TypeError("Invalid environment")

        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        cmd = (
            f'{{"spaceId":"{space_id}","modelId":"{model_id}", "environment":"{env}", '
            f'"modelVersion":"{model_version}", "batchId":"{batch_id}", "startTime":"{start_time_str}", '
            f'"endTime":"{end_time_str}", "includeActuals": {str(include_actuals).lower()}}}'
        )
        return self(query=cmd)

    def get_progress_bar(self, num_recs):
        return tqdm(
            total=num_recs,
            desc=f"  exporting {num_recs} rows",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}, {rate_fmt}{postfix}]",
            ncols=80,
            colour="#008000",
            unit=" row",
        )
