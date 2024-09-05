import streamlit as st
from typing import Literal
from st_aggrid import GridOptionsBuilder

def get_grid_options(
    data,
    page_height: int = 20,
    selection_mode: Literal["single", "multiple", "disabled"] = "disabled",
):
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_selection(
        selection_mode,
        use_checkbox=True,
        header_checkbox=True,
        rowMultiSelectWithClick=True,
    )
    # gb.configure_pagination(
    #     paginationAutoPageSize=False,
    #     paginationPageSize=page_height,
    # )
    grid_options = gb.build()
    return grid_options