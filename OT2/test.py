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
            if row['Source Well'] == '**RELOAD':  # Skip reload lines
                writer.writerow(row)
                continue
            if row['Dest Well'] == '**RELOAD':  # Skip reload lines
                writer.writerow(row)
                continue
            
            # Update the volume
            row['Volume (in ul)'] = '200'
            
            # Write the updated row
            writer.writerow(row)


metadata = {
    'protocolName': 'Cherrypicking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.3'
}

def run(ctx):
    transfer_csv = convert_csv('/Users/MingW/SARL/GitLab/OT2/new/test_run_2.csv', 'test_2.csv')
    with open('test_2.csv', 'r') as f:
        transfer_csv = f.read()


    pipette_type = "p300_single_gen2"
    pipette_mount = "left"
    
    tiprack_map = {
        'p10_single': 'opentrons_96_tiprack_10ul',
        'p50_single': 'opentrons_96_tiprack_300ul',
        'p300_single_gen1': 'opentrons_96_tiprack_300ul',
        'p1000_single_gen1': 'opentrons_96_tiprack_1000ul',
        'p20_single_gen2': 'opentrons_96_tiprack_20ul',
        'p300_single_gen2': 'opentrons_96_tiprack_300ul',
        'p1000_single_gen2': 'opentrons_96_tiprack_1000ul'
    }

    # load labware
    res1 = ctx.load_labware('nest_12_reservoir_15ml', 6)
    transfer_info = [[val.strip().lower() for val in line.split(',')]
                     for line in transfer_csv.splitlines()
                     if line.split(',')[0].strip()][1:]
    for line in transfer_info:
        s_lw, s_slot, d_lw, d_slot = line[:2] + line[4:6]
        for slot, lw in zip([s_slot, d_slot], [s_lw, d_lw]):
            if not int(slot) in ctx.loaded_labwares and int(slot) != 6:
                ctx.load_labware(lw.lower(), slot)

    # load tipracks in remaining slots
    tiprack_type = tiprack_map[pipette_type]
    tipracks = []
    for slot in range(1, 13):
        if slot not in ctx.loaded_labwares:
            tipracks.append(ctx.load_labware(tiprack_type, str(slot)))

    # load pipette
    pip = ctx.load_instrument(pipette_type, pipette_mount, tip_racks=tipracks)

    tip_count = 0
    tip_max = len(tipracks*96)
    
    # Add speed changes for the mix process
    original_aspirate_rate = pip.flow_rate.aspirate
    original_dispense_rate = pip.flow_rate.dispense

    def pick_up():
        nonlocal tip_count
        if tip_count == tip_max:
            ctx.pause('Please refill tipracks before resuming.')
            pip.reset_tipracks()
            tip_count = 0
        pip.pick_up_tip()
        tip_count += 1

    def parse_well(well):
        letter = well[0]
        number = well[1:]
        return letter.upper() + str(int(number))

    # Modify the loop that goes through the transfer_info
    for line in transfer_info:
        _, s_slot, s_well, h, _, d_slot, d_well, vol = line[:8]
        
        if s_well.lower() == 'reload':
            ctx.pause('Please refill source labware in slot {} before resuming.'.format(s_slot))
            continue
        if d_well.lower() == 'reload':
            ctx.pause('Please refill destination labware in slot {} before resuming.'.format(d_slot))
            continue
        
    for line in transfer_info:
        _, s_slot, s_well, h, _, d_slot, d_well, vol = line[:8]

        if s_well.lower() == '**reload':
            ctx.pause('Please refill source labware in slot {} before resuming.'.format(s_slot))
            ctx.comment("Pausing for 2 minutes before resuming.")
            ctx.delay(seconds=120)
            continue
        if d_well.lower() == '**reload':
            ctx.pause('Please refill destination labware in slot {} before resuming.'.format(d_slot))
            ctx.comment("Pausing for 2 minutes before resuming.")
            ctx.delay(seconds=120)
            continue
        
        # If the source slot is 6, assume it is a reservoir
        if int(s_slot) == 6:
            source = ctx.loaded_labwares[int(s_slot)].wells_by_name()['A1'].bottom(float(h))
        else:
            source = ctx.loaded_labwares[int(s_slot)].wells_by_name()[parse_well(s_well)].bottom(float(h))
        
        # If the destination slot is 6, assume it is a reservoir
        if int(d_slot) == 6:
            dest = ctx.loaded_labwares[int(d_slot)].wells_by_name()['A1']
        else:
            dest = ctx.loaded_labwares[int(d_slot)].wells_by_name()[parse_well(d_well)]

        pick_up()

        # Step 2: Aspirate 100ul liquid from reservoir
        pip.aspirate(100, res1['A1'])

        # Step 3: Dispense the liquid aspirated from reservoir into source well
        pip.dispense(100, source)

        # Change speeds for mix
        pip.flow_rate.aspirate = 50  # Set new rate
        pip.flow_rate.dispense = 50  # Set new rate

        # Step 4: Mix the combined liquid in source well 2-3 times
        pip.mix(2, 100, source)  # Mixing step

        # Restore original speeds
        pip.flow_rate.aspirate = original_aspirate_rate
        pip.flow_rate.dispense = original_dispense_rate

        # Step 5: Aspirate from source and Step 6: Dispense to destination
        pip.transfer(float(vol), source, dest, new_tip='never')
        
        pip.drop_tip()



# from opentrons import protocol_api
# import csv
# import time

# metadata = {
#     'protocolName': 'CSV Protocol Example',
#     'author': 'Your Name',
#     'apiLevel': '2.10'
# }

# def read_csv_to_dict(filepath):
#     with open(filepath, mode='r', encoding='utf-8-sig') as file:
#         reader = csv.DictReader(file)
#         data = [row for row in reader]
#     return data


# # def run(protocol: protocol_api.ProtocolContext):

# #     # ... [snip] ...

# #     filepath = '/Users/MingW/SARL/GitLab/OT2/8.3.23 janes copy for manual extraction_ DRF_RNA_set1_pick list_.2023JULY31.csv'  # Replace with the path to your actual CSV file
# #     csv_data = read_csv_to_dict(filepath)

# #     # Print out the keys of the first row to debug
# #     if csv_data:
# #         print(f"CSV keys: {csv_data[0].keys()}")

# #     # ... [rest of your code]


# def run(protocol: protocol_api.ProtocolContext):

#     # labware setup
#     tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '11')
#     source_plate = protocol.load_labware('falcon_96_wellplate_320ul', '1')
#     dest_plate = protocol.load_labware('axygen_96_wellplate_1100ul', '2')

#     # pipette setup
#     pip = protocol.load_instrument('p300_single', 'left', tip_racks=[tiprack])

#     filepath = '/Users/MingW/SARL/GitLab/OT2/8.3.23 janes copy for manual extraction_ DRF_RNA_set1_pick list_.2023JULY31.csv'  # Replace with the path to your actual CSV file
#     csv_data = read_csv_to_dict(filepath)

#     # Iterate through the rows in the CSV
#     for row in csv_data:
#         source_labware = row['Source Labware']
#         source_slot = row['Source Slot']
#         source_well = row['Source Well'].replace('0', '')  # Remove '0' from well name

#         if not source_well:  # Skip iteration if source_well is empty
#             continue

#         source_height_str = row['Source Aspiration Height Above Bottom (in mm)']
#         source_height = int(source_height_str) if source_height_str else None  # Handle empty string

#         dest_labware = row['Dest Labware']
#         dest_slot = row['Dest Slot']
#         dest_well = row['Dest Well'].replace('0', '')  # Remove '0' from well name

#         if not dest_well:  # Skip iteration if dest_well is empty
#             continue
        
#         volume_str = row['Volume (in ul)']
#         volume = float(volume_str) if volume_str else None  # Handle empty string

#         # Check for "**reload" flag and pause if present
#         if '**reload' in row.values():
#             protocol.comment("Pausing for 2 minutes before resuming.")
#             protocol.delay(seconds=120)

#         # Set custom mix speed
#         original_aspirate_speed = pip.flow_rate.aspirate
#         original_dispense_speed = pip.flow_rate.dispense
#         pip.flow_rate.aspirate = 50  # Replace with desired value
#         pip.flow_rate.dispense = 50  # Replace with desired value

#         pip.pick_up_tip()
#         pip.aspirate(volume, source_plate[source_well].bottom(source_height))
#         pip.dispense(volume, dest_plate[dest_well])
#         pip.drop_tip()

#         # Reset mix speed to original values
#         pip.flow_rate.aspirate = original_aspirate_speed
#         pip.flow_rate.dispense = original_dispense_speed
