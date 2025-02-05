import os
from datetime import datetime, timedelta

# Set start and stop dates
start_date = "2009-03-29"
stop_date = "2009-03-30"

# Convert string dates to datetime objects
start = datetime.strptime(start_date, "%Y-%m-%d")
stop = datetime.strptime(stop_date, "%Y-%m-%d")

# Generate a list of days to process
day_list = []
while start <= stop:
    formatted_day = f"{start:%y%m%d}"  # Format as YYMMDD
    day_list.append(formatted_day)
    start += timedelta(days=1)

# Collect catalogs obtained using different templates to provide a daily catalog
for day in day_list:
    print(f"Processing day {day}...")
    
    # Concatenate all matching files into a single daily catalog
    acat_filename = f"{day}Acat"
    matching_files = [f for f in os.listdir(".") if f.endswith(f".{day}.cat")]
    
    if matching_files:
        with open(acat_filename, "w") as outfile:
            for fname in matching_files:
                with open(fname) as infile:
                    outfile.write(infile.read())
        print(f"Catalog {acat_filename} created.")
    else:
        print(f"No catalog found for {day}.")
        continue
    
    # Filter and cut daily catalog to select maximum threshold events
    try:
        os.rename(acat_filename, "dcat")  # Temporary file for processing
        os.system("python process_detections.py")  # Process the catalog
        os.rename("dcatf1f2", f"{day}Acatf1f2")  # Rename filtered catalog
        os.remove("dcat")  # Clean up temporary files
        print(f"Filtered catalog {day}Acatf1f2 created.")
    except FileNotFoundError:
        print("Filtering failed. Temporary files not found.")
        continue

# Combine all cleaned catalogs into a single file called outcat
with open("outcat", "w") as outfile:
    for file in os.listdir("."):
        if file.endswith("Acatf1f2"):
            with open(file) as infile:
                outfile.write(infile.read())
print("Final catalog written to outcat.")
