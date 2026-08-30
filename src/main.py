import logging

from .extract import extract
from .load import load
from .transform import transform


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def run()-> None:
    logging.info("Extracting weather data")
    payload = extract()

    logging.info("Transforming weather data")
    dataframe = transform(payload)

    logging.info("Loading weather data")
    row_count = load(dataframe)

    logging.info("Loaded %s rows", row_count)


if __name__=="__main__":
    run()
