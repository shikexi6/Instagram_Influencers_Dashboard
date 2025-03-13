library(readr)

# Define the relative path to the data file
data_path <- file.path(dirname(rstudioapi::getActiveDocumentContext()$path), "../../data/processed/influencers.csv")

# Load the CSV file
data <- read_csv(data_path)
