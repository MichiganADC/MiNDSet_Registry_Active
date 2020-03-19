#!/usr/bin/env python3

# mindset_registry_active.py


# Import modules

import pandas as pd
from typing import List

import config as cfg
import helpers as hlps


# Helper function(s)

def str_series_to_date_series(s: pd.Series) -> pd.Series.dt:
    """
    Converts pd.Series[str] of dates to pd.Series.dt of dates
    """
    return pd.to_datetime(s, format="%Y-%m-%d")


###
# Extract MiNDSet Registry data from REDCap

# Define fields to retrieve
fields_ms_raw: List = ["subject_id",
                       # Patient Demographic Entry
                       "first_name",
                       "last_name",
                       "reg_num",
                       "birth_date",
                       "street",
                       "pt_city",
                       "state",
                       "zip_code",
                       "pt_deceased",
                       # Research Volunteer Form
                       "date",  # RVF date at top of RVF
                       "rvf_date_completed",  # RVF date at bottom of RVF
                       "nolonger_interested"  # Date pt. expressed no long interested in research
                       ]
fields_ms: str = ",".join(fields_ms_raw)

# Retrieve data
df_ms: pd.DataFrame = hlps.export_redcap_records(uri=cfg.REDCAP_API_URI,
                                                 token=cfg.REDCAP_API_TOKEN_MINDSET,
                                                 fields=fields_ms)


###
# Transform data

# Copy df_ms
df_ms_cln: pd.DataFrame = df_ms.copy()

# Coalesce RVF dates
df_ms_cln['rvf_date'] = df_ms_cln.date.combine_first(df_ms_cln.rvf_date_completed)
del df_ms_cln['date']
del df_ms_cln['rvf_date_completed']

# Coerce date cols to datetime
df_ms_cln.rvf_date = str_series_to_date_series(df_ms_cln['rvf_date'])
df_ms_cln.birth_date = str_series_to_date_series(df_ms_cln['birth_date'])
df_ms_cln.nolonger_interested = str_series_to_date_series(df_ms_cln['nolonger_interested'])

# Filter out records with missing `rvf_date`
df_ms_cln = df_ms_cln[df_ms_cln['rvf_date'].notna()]

# Copy df_ms_cln
df_ms_cln_flt: pd.DataFrame = df_ms_cln.copy()

# Filter out records with `rvf_date` older than 5 years ago
df_ms_cln_flt = \
    df_ms_cln_flt[(df_ms_cln_flt.rvf_date >= pd.Timestamp.today() - pd.DateOffset(years=5))]

# Filter out records of deceased
df_ms_cln_flt = \
    df_ms_cln_flt.loc[df_ms_cln_flt.pt_deceased.isna() |
                      (df_ms_cln_flt.pt_deceased == "1"), :]

# Filter out records of folks no longer interested
df_ms_cln_flt = \
    df_ms_cln_flt.loc[df_ms_cln_flt.nolonger_interested.isna() |
                      (df_ms_cln_flt.nolonger_interested >= pd.Timestamp.today()), :]

# Filter out records of folks not residing in Michigan or Ohio
df_ms_cln_flt = \
    df_ms_cln_flt.loc[df_ms_cln_flt.state.isin(["MI", "Mi", "Mich", "Michigan", "OH", "Oh", "Ohio"]), :]


###
# Load data

# Write to CSV
df_ms_cln_flt.to_csv("./MiNDSet_Registry_Active.csv", index=False)
