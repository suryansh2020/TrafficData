# set working drive
setwd("/home/tbonza/projects/TrafficData/MassDOThack/Road_RTTM_Volume")

# Check out some csv files
pair_definitions <- read.csv("pair_definitions.csv")
pair_definitions_fields <- read.csv("pair_definitions_fields.csv")
massdot_bluetoad_data_fields <- read.csv(
  "massdot_bluetoad_data_fields.csv")

# Get a feel for whats in them
head(massdot_bluetoad_data_fields)
colnames(massdot_bluetoad_data_fields)

head(pair_definitions_fields)
colnames(pair_definitions_fields)

head(pair_definitions)
colnames(pair_definitions)

# this one's a bit larger but let's take a look.
massdot_bluetoad_data <- read.csv(
  "massdot_bluetoad_data/massdot_bluetoad_data.csv")

# and let's check it out
head(massdot_bluetoad_data)
colnames(massdot_bluetoad_data)

# columns are mapped out in Data Structure.ods
