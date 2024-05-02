#!/bin/bash

# Input and output files
input="pluvial_rainfall.csv-e"
output="rainfall-aggregated.csv"

# Use awk to process and aggregate data
awk -F, 'BEGIN {OFS=","}
NR == 1 {
    print "GRID_NO", "LATITUDE", "LONGITUDE", "AVG_TEMPERATURE_MAX", "AVG_TEMPERATURE_MIN", "AVG_WINDSPEED", "SUM_PRECIPITATION"
} # Print the new header
NR > 1 {
    # Round latitude and longitude
    lat = sprintf("%.1f", $2)
    lon = sprintf("%.1f", $3)
    key = lat "," lon

    # Aggregate data
    temp_max[key] += $6; count_max[key]++
    temp_min[key] += $7; count_min[key]++
    windspeed[key] += $8; count_ws[key]++
    precipitation[key] += $10

    # Keep track of the first occurring GRID_NO for each coordinate for reference
    if (grid_no[key] == "") grid_no[key] = $1
}
END {
    # Output the aggregated results
    for (k in temp_max) {
        avg_temp_max = temp_max[k] / count_max[k]
        avg_temp_min = temp_min[k] / count_min[k]
        avg_windspeed = windspeed[k] / count_ws[k]
        sum_precipitation = precipitation[k]
        split(k, coords, ",")
        print grid_no[k], coords[1], coords[2], avg_temp_max, avg_temp_min, avg_windspeed, sum_precipitation
    }
}' $input > $output
