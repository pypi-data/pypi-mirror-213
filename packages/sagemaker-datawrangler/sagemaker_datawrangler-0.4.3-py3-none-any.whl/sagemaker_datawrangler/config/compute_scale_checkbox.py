import logging

import ipywidgets as widgets
import pandas as pd

from ..datawrangler import DataWranglerWidget
from .config import COMPUTE_ON_ALL_ROWS, DEFAULT_MAX_COMPUTE_ROW_COUNT


def get_checkbox(dw_widget: DataWranglerWidget, df: pd.DataFrame):
    checkbox = widgets.Checkbox(
        value=False,
        description="Use all of the rows in the data frame for data insights. By default, data insights is computed on the first 10,000 rows of the data frame.",
        disabled=False,
        indent=False,
    )
    checkbox.add_class("dw-widget-checkbox")

    def changed(checkbox):
        if checkbox and checkbox.old == False and checkbox.new == True:
            logging.info("Checked the checkbox: compute on all rows.")

            COMPUTE_ON_ALL_ROWS = "True"
            dw_widget.update_compute_row_count(df)

        elif checkbox and checkbox.old == True and checkbox.new == False:
            logging.info("Unchecked the checkbox: compute on all rows.")

            COMPUTE_ON_ALL_ROWS = "False"
            dw_widget.update_compute_row_count(df, DEFAULT_MAX_COMPUTE_ROW_COUNT)

    checkbox.observe(changed)

    return checkbox
