import asyncio
import re
from asyncio import QueueEmpty
from typing import Any

import numpy as np
import pandas as pd
from pydantic import AnyUrl, BaseModel, Field, validator

from contact_magic.integrations import (
    make_copyfactory_request,
    make_sales_scraper_request,
)
from contact_magic.logger import logger
from contact_magic.utils import get_id_from_url, is_valid_premise_url, replace_keys
from settings import SETTINGS


class DataRow(BaseModel):
    """
    A class to hold a row of data and it's index number
    to sort by after. Converts set data to a dict.
    """

    data: Any
    index: int
    _original_type = None

    @validator("data")
    def validate_data(cls, value):
        if not isinstance(value, pd.Series) and not isinstance(value, dict):
            raise ValueError("Data must be either type pd.Series or Dict.")
        _original_type = pd.Series if isinstance(value, pd.Series) else dict
        return value.to_dict() if isinstance(value, pd.Series) else value

    @property
    def convert_to_original(self):
        return (
            pd.Series(data=self.data) if self._original_type == pd.Series else self.data
        )


class Scraper(BaseModel):
    """
    A reference to a scraper endpoint in SalesScrapers and a Copyfactory premiseURL.
    """

    scraper_name: str | None = Field(
        description="This is the endpoint from sales-scrapers", example="get-case-study"
    )
    premise_url: AnyUrl = Field(
        description="The Copyfactory premise URL you want to use. "
        "The ID is extracted from the URL",
        default=None,
    )
    premise_id: int = Field(
        description="The Copyfactory premise ID you want to use.", default=None
    )
    fallback_template: str = ""
    scraper_mapping: dict = Field(
        description="A mapping where the keys are your column "
        "names and the values are the target parameter "
        "name for SalesScrapers.",
        default={},
    )
    copyfactory_mapping: dict = Field(
        description="A mapping where the keys are your column names and the "
        "values are the target variable name you want to send to Copyfactory.",
        default={},
    )

    @validator("premise_url")
    def validate_premise_url(cls, url):
        return f"{url}/" if not url.endswith("/") else url

    @validator("scraper_name")
    def validate_scraper_name(cls, value):
        if value is None:
            return value
        if not SETTINGS.ALLOWED_SCRAPER_NAMES:
            return value
        if value not in SETTINGS.ALLOWED_SCRAPER_NAMES:
            raise ValueError(
                f"{value} is not an allowed scraper name "
                f"your configured scrapers are {SETTINGS.ALLOWED_SCRAPER_NAMES}."
            )
        return value

    @property
    def is_premise_url_valid(self) -> bool:
        return is_valid_premise_url(self.premise_url)

    def fill_fallback(self, row: DataRow) -> str:
        """
        Fills in the template with row data.
        either returns the filled in template or an empty string.
        """
        list_pot_keys = re.findall(r"\{(.*?)\}", self.fallback_template)
        copy_of_template = self.fallback_template
        filled_all = True
        for key in list_pot_keys:
            value = row.data.get(key)
            if not value:
                filled_all = False
                continue
            copy_of_template = copy_of_template.replace("{" + key + "}", value)
        return copy_of_template if filled_all else ""

    async def run_sales_scraper(self, row: DataRow, col_prefix: str, overwrite=False):
        """
        Runs the scraping and extends the row by adding
        the column name + scraper as a prefix to ensure uniqueness.
        """
        if not self.scraper_name:
            return row
        if not self.scraper_mapping and SETTINGS.SCRAPER_MAPPING:
            self.scraper_mapping = SETTINGS.SCRAPER_MAPPING

        data = (
            replace_keys(row.data, self.scraper_mapping)
            if self.scraper_mapping
            else row.data
        )
        if scrape := await make_sales_scraper_request(self.scraper_name, data=data):
            for key, value in scrape.items():
                if key in row.data and not overwrite:
                    continue
                unique_key = f"{col_prefix}__{self.scraper_name}__{key}"
                row.data[unique_key] = value
            return row
        return row

    async def run_copyfactory(
        self, row: DataRow, content_col_name: str, source_col_name: str
    ):
        """
        Runs Copyfactory using the current row Data.
        If successfully called with Copyfactory returns True to stop iteration
        for that datapoint.
        """
        if not self.premise_url and not self.premise_id:
            return row, False
        if self.premise_url and self.is_premise_url_valid:
            self.premise_id = get_id_from_url(self.premise_url)
        if not self.copyfactory_mapping and SETTINGS.COPYFACTORY_MAPPING:
            self.copyfactory_mapping = SETTINGS.COPYFACTORY_MAPPING

        data = (
            replace_keys(row.data, self.copyfactory_mapping)
            if self.copyfactory_mapping
            else row.data
        )
        if cf := await make_copyfactory_request(self.premise_id, variables=data):
            row.data[content_col_name] = cf["content"]
            source = row.data.get(
                f"{content_col_name}__{self.scraper_name}__scraper_info", {}
            ).get("data_source", "-")
            row.data[source_col_name] = f"{self.scraper_name}, {source}"
            return row, True
        return row, False

    async def execute(
        self, row: DataRow, content_col_name: str, source_col_name: str
    ) -> tuple[DataRow, bool]:
        """
        Executes the scraper and extends the DataRow as it moves along to
        allow for exploding the DF with more
        datapoints from the scraping + personalization.
        """
        if self.scraper_name == "FALLBACK" and self.fallback_template:
            row.data[content_col_name] = self.fill_fallback(row)
            row.data[source_col_name] = "-"
            return row, row.data[content_col_name] is not None
        row = await self.run_sales_scraper(row, col_prefix=content_col_name)
        row, success = await self.run_copyfactory(
            row, content_col_name, source_col_name
        )
        return row, success


class DataPoint(BaseModel):
    """
    A reference to a datapoint to create for a given contact
    targeting a column and a list of allowed scrapers.
    """

    col_name: str = Field(
        description="The column name you want for the datapoint.",
        example="Personalization1",
    )
    allowed_scrapers: list[Scraper]

    @property
    def get_col_name_as_source(self) -> str:
        return f"source__{self.col_name}"

    async def build_datapoint(self, row: DataRow):
        for scraper in self.allowed_scrapers:
            logger.info(
                "processing_row",
                row_number=row.index + 2,
                scraper_name=scraper.scraper_name,
                column_name=self.col_name,
                status="STARTING",
            )
            row, did_succeed = await scraper.execute(
                row, self.col_name, self.get_col_name_as_source
            )
            if did_succeed:
                logger.info(
                    "processing_row",
                    row_number=row.index + 2,
                    scraper_name=scraper.scraper_name,
                    column_name=self.col_name,
                    status="SUCCESS",
                )
                break
            else:
                logger.info(
                    "processing_row",
                    row_number=row.index + 2,
                    scraper_name=scraper.scraper_name,
                    column_name=self.col_name,
                    status="FAILED",
                )
        return row


class PersonalizationSettings(BaseModel):
    """
    A reference to a list of datapoints to generate for a given contact.
    """

    datapoints: list[DataPoint]

    @property
    def get_datapoint_column_names(self) -> list:
        """
        Returns a list of column names and a source field.
        """
        return [dp.col_name for dp in self.datapoints] + [
            dp.get_col_name_as_source for dp in self.datapoints
        ]

    def extend_dataframe_with_settings_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.assign(
            **{
                c: np.nan
                for c in self.get_datapoint_column_names
                if c not in df.columns
            }
        )

    def process_from_dataframe(
        self, df: pd.DataFrame, exclude_filter_func: callable = None
    ):
        """
        Process a dataframe and extend it's rows based on the
        personalization settings.
        Also accepts a callable which takes as its only argument
        the row from the dataframe to filter on.
        This function must resolve to a boolean and rows that are
        True are not processed.
        """
        df = self.extend_dataframe_with_settings_columns(df)
        untouched_rows = []
        jobs = []
        for i, row in df.iterrows():
            if exclude_filter_func and exclude_filter_func(row):
                untouched_rows.append(DataRow(data=row, index=i))
                continue
            jobs.append(DataRow(data=row, index=i))
        return pd.DataFrame(
            data=[
                row.convert_to_original
                for row in sorted(
                    untouched_rows + self.process_data_rows(jobs),
                    key=lambda dp: dp.index,
                )
            ],
            columns=df.columns,
        )

    def process_data_rows(self, data: list[DataRow]):
        """
        Process DataRows async.
        :param data:
        :return:
        """
        return asyncio.run(do_bulk([(self.build_row, {"row": row}) for row in data]))

    async def build_row(self, row: DataRow):
        """
        Iterate over all personalization datapoints and their
        allowed scrapers to extend a row of contact data
        with enrichment and personalized sentences.
        """
        for datapoint in self.datapoints:
            row = await datapoint.build_datapoint(row)
        return row


async def do_bulk(ops: list, max_workers: int = SETTINGS.MAX_WORKERS) -> list[DataRow]:
    """
    Bulk operation
    This function can be used to run bulk operations
    using a limited number of concurrent requests.
    """
    results = [None for _ in range(len(ops))]

    queue = asyncio.Queue()

    for job in enumerate(ops):
        await queue.put(job)

    workers = [_worker(queue, results) for _ in range(max_workers)]

    await asyncio.gather(*workers)

    return results


async def _worker(queue, results):
    while True:
        try:
            index, op = queue.get_nowait()
        except QueueEmpty:
            break

        try:
            response = await op[0](**op[1])
            results[index] = response
        except Exception:
            results[index] = None
        queue.task_done()
