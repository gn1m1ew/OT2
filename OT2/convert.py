import csv

def convert_csv(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8-sig') as infile, open(output_filename, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames  # Get the fieldnames (header)
        
        # Create a writer object
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()
        
        for row in reader:
            if row['Source Labware'] == '**RELOAD':  # Skip reload lines
                writer.writerow(row)
                continue
            
            # Update the volume
            row['Volume (in ul)'] = '100'
            
            # Write the updated row
            writer.writerow(row)

# Example usage
convert_csv('/Users/MingW/SARL/GitLab/OT2/4.csv', '4_modified.csv')

# import csv

# def convert_csv(input_file_path):
#     # Read the input CSV file
#     with open(input_file_path, 'r', encoding='utf-8-sig') as infile:
#         reader = csv.DictReader(infile)
#         input_data = [row for row in reader]
    
#     # Prepare the output data
#     output_data = []
#     dest_well_count = 0
#     for row in input_data:
#         # Skip the row if it is a reload indicator
#         if 'reload' in row.values():
#             continue
        
#         # Convert the 'Well' format from X01 to X1
#         source_well = row['Source Well'].lstrip("0")
        
#         # Generate the destination well in the format 'A01'
#         dest_well_row = chr(ord('A') + (dest_well_count // 12))
#         dest_well_col = (dest_well_count % 12) + 1
#         dest_well = f"{dest_well_row}{dest_well_col:02}"
        
#         output_data.append({
#             'Source Labware': row['Source Labware'],
#             'Source Slot': row['Source Slot'],
#             'Source Well': source_well,
#             'Source Aspiration Height Above Bottom (in mm)': 1,  # Default value
#             'Dest Labware': 'axygen_96_wellplate_1100ul',  # Default value
#             'Dest Slot': 1,  # Default value
#             'Dest Well': dest_well,
#             'Volume (in ul)': 100  # Default value
#         })
        
#         dest_well_count += 1



    
#     # Print the output data
#     fieldnames = [
#         'Source Labware', 'Source Slot', 'Source Well', 
#         'Source Aspiration Height Above Bottom (in mm)', 
#         'Dest Labware', 'Dest Slot', 'Dest Well', 'Volume (in ul)'
#     ]
    
#     print(",".join(fieldnames))
#     for row in output_data:
#         print(",".join(str(row[field]) for field in fieldnames))

# # Example usage
# convert_csv('/Users/MingW/SARL/GitLab/OT2/8.3.23 janes copy for manual extraction_ DRF_RNA_set1_pick list_.2023JULY31.csv')
# # import csv
# # import json

# # def convert_csv_to_json(csv_file_path):
# #     csv_data = []

# #     # Read the CSV file
# #     with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
# #         reader = csv.DictReader(file)
        
# #         # Read each row from the CSV and add it to the list
# #         for row in reader:
# #             csv_data.append(row)
            
# #     # Convert the list of dictionaries to a single string
# #     header = ["Source Labware", "Source Slot", "Source Well", "Source Aspiration Height Above Bottom (in mm)", "Dest Labware", "Dest Slot", "Dest Well", "Volume (in ul)"]
# #     lines = []

# #     for row in csv_data:
# #         row_str = f"{row['Source Labware']},{row['Source Slot']},{row['Source Well']},{row['Source Aspiration Height Above Bottom (in mm)']},{row['Dest Labware']},{row['Dest Slot']},{row['Dest Well']},{row['Volume (in ul)']}"
# #         lines.append(row_str)

# #     # csv_string = "\\n".join(lines)
# #     # csv_string = f"{','.join(header)}\\n{csv_string}"

# #     # # Create the JSON object
# #     # result = json.dumps({"transfer_csv": csv_string})
# #     # return result

# # # Usage example:
# # csv_file_path = '/Users/MingW/SARL/GitLab/OT2/8.3.23 janes copy for manual extraction_ DRF_RNA_set1_pick list_.2023JULY31.csv'  # Replace with your actual CSV file path
# # result = convert_csv_to_json(csv_file_path)
# # print(result)


# # # import csv

# # # def format_well(well):
# # #     row, col = well[:-2], well[-2:]
# # #     col = str(int(col))  # Remove leading zeros
# # #     return row + col

# # # def create_transfer_info(data_lines):
# # #     transfer_info = []
# # #     for line in data_lines:
# # #         parts = line.split('\t')
# # #         source_plate, source_plate_id, source_well, source_tip, dest_plate, dest_plate_id, dest_well, volume = parts
# # #         formatted_row = [
# # #             source_plate, 
# # #             source_plate_id, 
# # #             format_well(source_well), 
# # #             int(source_tip), 
# # #             dest_plate, 
# # #             dest_plate_id, 
# # #             format_well(dest_well), 
# # #             int(volume)
# # #         ]
# # #         transfer_info.append(formatted_row)
# # #     return transfer_info

# # # # Your data as a list of lines
# # # data_lines = [
# # #     "falcon_96_wellplate_320ul\t2\tA01\t2\taxygen_96_wellplate_1100ul\t1\tA01\t100",
# # #     "falcon_96_wellplate_320ul\t2\tA02\t2\taxygen_96_wellplate_1100ul\t1\tA02\t100",
# # #     # ... add all your other lines here
# # # ]

# # # # Create the transfer_info list
# # # transfer_info = create_transfer_info(data_lines)

# # # # Print the first few entries to check
# # # for row in transfer_info[:10]:
# # #     print(row)
