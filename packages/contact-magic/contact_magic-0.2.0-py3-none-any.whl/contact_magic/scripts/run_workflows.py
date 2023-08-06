import datetime

import gspread
import numpy as np
import pandas as pd
import pytz

from contact_magic.helpers import (
    get_personalization_settings_from_sheet,
    prepare_data_for_gsheet,
    worksheet_to_dataframe,
)
from contact_magic.integrations.sheets import (
    bulk_update,
    get_spreadsheet_by_url,
    get_worksheet_from_spreadsheet,
    update_cell,
)
from contact_magic.utils import is_google_workflow_url_valid
from contact_magic.scripts.logger import logger
from contact_magic.conf.settings import SETTINGS


def get_workflows_to_run(sheet):
    """
    Filter for only active workflows & ones with workflows URLs.
    """
    workflow_values = sheet.get_all_values()
    df = pd.DataFrame(data=workflow_values[1:], columns=workflow_values[0]).replace(
        "", np.nan
    )
    workflows_to_run = df.loc[df["RunWorkflow"] == "TRUE"]
    return workflows_to_run[workflows_to_run["WorkflowUrl"].notna()]


def update_date_last_ran(
    worksheet: gspread.Worksheet, row_number: int, col_number: int = 5
):
    """
    Update a cell with the latest date based on the configured timezone.
    """
    timezone = pytz.timezone(SETTINGS.TIMEZONE)
    current_time = datetime.datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")
    cell = worksheet.cell(row=row_number, col=col_number)
    cell.value = current_time
    update_cell(worksheet, cell.row, cell.col, cell.value)


def filter_out_row(row) -> bool:
    if row["is_approved"] == "TRUE":
        return True
    if pd.isnull(row["Website"]):
        return True
    return False


def run_sheets():
    workflows_sheet = get_worksheet_from_spreadsheet(
        get_spreadsheet_by_url(SETTINGS.MASTERSHEET_URL), "Workflows"
    )
    for i, row in get_workflows_to_run(workflows_sheet).iterrows():
        if not is_google_workflow_url_valid(row["WorkflowUrl"]):
            continue
        workflow_sheet = get_spreadsheet_by_url(row["WorkflowUrl"])
        filtered_working_data = worksheet_to_dataframe(workflow_sheet)
        # Don't filter working data since need to maintain
        # index so do spoof check to know if any rows to process.
        if (
            filtered_working_data.loc[filtered_working_data["is_approved"] == "FALSE"]
            .dropna(subset=["Website"])
            .empty
        ):
            continue
        logger.info(
            "running_workflow",
            row_number=i + 2,
            dataset_size=len(filtered_working_data),
            sequence_name=row["WorkflowName"],
            client_name=row["ClientName"],
            status="STARTING",
        )
        if all(
            col in filtered_working_data.columns for col in ["Company Name", "City"]
        ):
            filtered_working_data["search_query"] = filtered_working_data[
                "Company Name"
            ].str.cat(filtered_working_data["City"], sep=" ")
        if all(
            col in filtered_working_data.columns for col in ["City", "State", "Country"]
        ):
            filtered_working_data["location_search_from"] = filtered_working_data[
                "City"
            ].str.cat(
                [filtered_working_data["State"], filtered_working_data["Country"]],
                sep=", ",
            )
        settings = get_personalization_settings_from_sheet(workflow_sheet)
        updated_df = settings.process_from_dataframe(
            filtered_working_data, filter_out_row
        )
        data = prepare_data_for_gsheet(
            updated_df,
            {"is_approved": {"TRUE": True, "FALSE": False}},
            enforced_columns=["Website"],
        )
        working_sheet = get_worksheet_from_spreadsheet(workflow_sheet, "WorkingSheet")
        bulk_update(working_sheet, data)
        update_date_last_ran(workflows_sheet, i + 2)
        logger.info(
            "running_workflow",
            row_number=i + 2,
            dataset_size=len(updated_df),
            sequence_name=row["WorkflowName"],
            client_name=row["ClientName"],
            status="COMPLETE",
        )


if __name__ == "__main__":
    run_sheets()
