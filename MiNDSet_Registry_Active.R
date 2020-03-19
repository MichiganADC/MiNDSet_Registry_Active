# MiNDSet_Registry_Active.R

# Import packages

library(dplyr)
library(lubridate)


# Source configs
source("~/Box/Documents/R_helpers/config.R")
source("~/Box/Documents/R_helpers/helpers.R")


# Extract MiNDSet Registry data from REDCap

fields_ms_raw <- 
  c(
    "subject_id",
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
    "date", # RVF date at top of RVF
    "rvf_date_completed", # RVF date at bottom of RVF
    "nolonger_interested" # Date pt. expressed no long interested in research
  )
fields_ms <- 
  fields_ms_raw %>% paste(collapse = ",")

json_ms <- 
  export_redcap_records(uri = REDCAP_API_URI,
                        token = REDCAP_API_TOKEN_MINDSET,
                        fields = fields_ms)


# Transform MiNDSet Registry data

df_ms <-
  json_ms %>% 
  jsonlite::fromJSON() %>% 
  na_if("")

df_ms_cln <-
  df_ms %>% 
  mutate(rvf_date = as_date(coalesce(date, rvf_date_completed))) %>% 
  mutate(birth_date = as_date(birth_date),
         nolonger_interested = as_date(nolonger_interested)) %>%
  select(-date, -rvf_date_completed) %>% 
  select(subject_id, rvf_date, everything()) %>% 
  filter(!is.na(rvf_date))

df_ms_cln_flt <-
  df_ms_cln %>% 
  # RVF filled out with last 5 years
  filter(rvf_date >= (today() - years(5))) %>% 
  # Referral not deceased (as far as we know)
  filter(is.na(pt_deceased) | pt_deceased == "1") %>% 
  # Referral is still interested in study participation (as far as we know)
  filter(is.na(nolonger_interested) | nolonger_interested >= today()) %>% 
  # # Referral is older than 50
  # filter(birth_date <= (today() - years(50))) %>% 
  # Referral lives in Michigan or Ohio
  filter(state %in% c("MI", "Michigan", "Mich", "Mi", "OH", "Ohio", "Oh"))
