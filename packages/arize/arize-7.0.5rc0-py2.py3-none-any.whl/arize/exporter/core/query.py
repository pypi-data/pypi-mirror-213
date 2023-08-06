from typing import Tuple

from arize.utils.logging import logger
from pyarrow import flight

from .session import Session


class Query:
    def __init__(
        self,
        query: str,
        client: flight.FlightClient,
        session: Session,
    ) -> None:
        self.query = query
        self.client = client
        self.headers = session.headers

    def execute_query(self) -> Tuple[flight.FlightStreamReader, int]:
        try:
            options = flight.FlightCallOptions(headers=self.headers)
            flight_info = self.client.get_flight_info(
                flight.FlightDescriptor.for_command(self.query), options
            )
            logger.info("Fetching data...")

            if flight_info.total_records == 0:
                logger.info("Query returns no data")
                return None, 0
            logger.debug("Ticket: %s", flight_info.endpoints[0].ticket)

            # Retrieve the result set as flight stream reader
            reader = self.client.do_get(flight_info.endpoints[0].ticket, options)
            logger.info("Starting exporting...")
            return reader, flight_info.total_records

        except Exception:
            logger.error("There was an error trying to get the data from the endpoint")
            raise
