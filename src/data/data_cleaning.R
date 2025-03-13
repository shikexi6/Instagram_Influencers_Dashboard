library(dplyr)
library(readr)
library(stringr)

# Read data
data_path <- "data/raw/influencers_data.csv"
data <- read_csv(data_path, col_types = cols(.default = "c"))  # Read all as characters initially

# Replace empty cells with "Not Listed"
data[is.na(data)] <- "Not Listed"

# Convert '60_day_eng_rate' from percentage to decimal (e.g., 1.1% → 0.011)
data <- data %>%
  mutate(eng_rate = as.numeric(str_remove(`60_day_eng_rate`, "%")) / 100) %>%
  select(-`60_day_eng_rate`)  # Remove old column

# Function to convert formatted numbers (e.g., 2.0k → 2000, 1.2m → 1200000)
convert_to_number <- function(value) {
  if (str_detect(value, "k")) {
    return(as.numeric(str_replace(value, "k", "")) * 1000)
  } else if (str_detect(value, "m")) {
    return(as.numeric(str_replace(value, "m", "")) * 1000000)
  } else if (str_detect(value, "b")) {
    return(as.numeric(str_replace(value, "b", "")) * 1000000000)
  }
  return(as.numeric(value))
}

# Identify numeric columns for conversion
numeric_columns <- c("posts", "followers", "avg_likes", "new_post_avg_like", "total_likes", "eng_rate")

# Apply conversion function to numeric columns
data[numeric_columns] <- lapply(data[numeric_columns], function(col) sapply(col, convert_to_number))

# Display first few rows
print(head(data))

# Save processed data
processed_data_path <- "data/processed/influencers.csv"
write_csv(data, processed_data_path)

print("Processed data saved successfully!")
