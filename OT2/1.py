from opentrons import protocol_api

def get_values(*names):
    import json
    _all_values = json.loads("""{"pipette_type":"p300_single_gen2","pipette_mount":"left","transfer_csv":"Source Labware,Source Slot,Source Well,Source Aspiration Height Above Bottom (in mm),Dest Labware,Dest Slot,Dest Well,Volume (in ul)\\nfalcon_96_wellplate_320ul,2,A1,1,axygen_96_wellplate_1100ul,1,A01,100\\nfalcon_96_wellplate_320ul,2,A2,1,axygen_96_wellplate_1100ul,1,A02,100\\nfalcon_96_wellplate_320ul,2,A3,1,axygen_96_wellplate_1100ul,1,A03,100\\nfalcon_96_wellplate_320ul,2,A4,1,axygen_96_wellplate_1100ul,1,A04,100\\nfalcon_96_wellplate_320ul,3,A4,1,axygen_96_wellplate_1100ul,1,A05,100\\nfalcon_96_wellplate_320ul,3,A5,1,axygen_96_wellplate_1100ul,1,A06,100\\nfalcon_96_wellplate_320ul,3,A6,1,axygen_96_wellplate_1100ul,1,A07,100\\nfalcon_96_wellplate_320ul,3,A7,1,axygen_96_wellplate_1100ul,1,A08,100\\nfalcon_96_wellplate_320ul,4,A1,1,axygen_96_wellplate_1100ul,1,A09,100\\nfalcon_96_wellplate_320ul,4,A2,1,axygen_96_wellplate_1100ul,1,A10,100\\nfalcon_96_wellplate_320ul,4,A3,1,axygen_96_wellplate_1100ul,1,A11,100\\nfalcon_96_wellplate_320ul,4,A4,1,axygen_96_wellplate_1100ul,1,A12,100\\nfalcon_96_wellplate_320ul,2,B4,1,axygen_96_wellplate_1100ul,1,B01,100\\nfalcon_96_wellplate_320ul,2,D4,1,axygen_96_wellplate_1100ul,1,B02,100\\nfalcon_96_wellplate_320ul,2,E4,1,axygen_96_wellplate_1100ul,1,B03,100\\nfalcon_96_wellplate_320ul,2,G4,1,axygen_96_wellplate_1100ul,1,B04,100\\nfalcon_96_wellplate_320ul,3,B7,1,axygen_96_wellplate_1100ul,1,B05,100\\nfalcon_96_wellplate_320ul,3,C7,1,axygen_96_wellplate_1100ul,1,B06,100\\nfalcon_96_wellplate_320ul,3,D7,1,axygen_96_wellplate_1100ul,1,B07,100\\nfalcon_96_wellplate_320ul,3,E7,1,axygen_96_wellplate_1100ul,1,B08,100\\nfalcon_96_wellplate_320ul,4,B2,1,axygen_96_wellplate_1100ul,1,B09,100\\nfalcon_96_wellplate_320ul,4,C2,1,axygen_96_wellplate_1100ul,1,B10,100\\nfalcon_96_wellplate_320ul,4,D2,1,axygen_96_wellplate_1100ul,1,B11,100\\nfalcon_96_wellplate_320ul,4,E2,1,axygen_96_wellplate_1100ul,1,B12,100\\nfalcon_96_wellplate_320ul,5,E5,1,axygen_96_wellplate_1100ul,1,C01,100\\nfalcon_96_wellplate_320ul,5,G5,1,axygen_96_wellplate_1100ul,1,C02,100\\nfalcon_96_wellplate_320ul,5,H5,1,axygen_96_wellplate_1100ul,1,C03,100\\nfalcon_96_wellplate_320ul,5,B5,1,axygen_96_wellplate_1100ul,1,C04,100\\nfalcon_96_wellplate_320ul,6,C03,1,axygen_96_wellplate_1100ul,1,C05,100\\nfalcon_96_wellplate_320ul,6,H03,1,axygen_96_wellplate_1100ul,1,C06,100\\nfalcon_96_wellplate_320ul,6,B03,1,axygen_96_wellplate_1100ul,1,C07,100\\nfalcon_96_wellplate_320ul,6,D03,1,axygen_96_wellplate_1100ul,1,C08,100\\nfalcon_96_wellplate_320ul,7,B05,1,axygen_96_wellplate_1100ul,1,C09,100\\nfalcon_96_wellplate_320ul,7,C05,1,axygen_96_wellplate_1100ul,1,C10,100\\nfalcon_96_wellplate_320ul,7,D05,1,axygen_96_wellplate_1100ul,1,C11,100\\nfalcon_96_wellplate_320ul,7,E05,1,axygen_96_wellplate_1100ul,1,C12,100\\nfalcon_96_wellplate_320ul,8,B05,1,axygen_96_wellplate_1100ul,1,D01,100\\nfalcon_96_wellplate_320ul,8,C05,1,axygen_96_wellplate_1100ul,1,D02,100\\nfalcon_96_wellplate_320ul,8,D05,1,axygen_96_wellplate_1100ul,1,D03,100\\nfalcon_96_wellplate_320ul,8,E05,1,axygen_96_wellplate_1100ul,1,D04,100\\nfalcon_96_wellplate_320ul,10,B04,1,axygen_96_wellplate_1100ul,1,D05,100\\nfalcon_96_wellplate_320ul,10,C04,1,axygen_96_wellplate_1100ul,1,D06,100\\nfalcon_96_wellplate_320ul,10,D04,1,axygen_96_wellplate_1100ul,1,D07,100\\nfalcon_96_wellplate_320ul,10,E04,1,axygen_96_wellplate_1100ul,1,D08,100"}""")
    return [_all_values[n] for n in names]

metadata = {
    'protocolName': 'Cherrypicking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.3'
}


def run(ctx):

    pipette_type, pipette_mount, transfer_csv = get_values(  # noqa: F821
        "pipette_type", "pipette_mount", "transfer_csv")

    tiprack_map = {
        'p10_single': 'opentrons_96_tiprack_10ul',
        'p50_single': 'opentrons_96_tiprack_300ul',
        'p300_single_gen1': 'opentrons_96_tiprack_300ul',
        'p1000_single_gen1': 'opentrons_96_tiprack_1000ul',
        'p20_single_gen2': 'opentrons_96_tiprack_20ul',
        'p300_single_gen2': 'opentrons_96_tiprack_300ul',
        'p1000_single_gen2': 'opentrons_96_tiprack_1000ul'
    }

    # # load labware
    transfer_info = [[val.strip().lower() for val in line.split(',')]
                     for line in transfer_csv.splitlines()
                     if line.split(',')[0].strip()][1:]
    
    
    # res1 = ctx.load_labware('nest_12_reservoir_15ml', 6)
    
    # for line in transfer_info:
    #     s_lw, s_slot, d_lw, d_slot = line[:2] + line[4:6]
    #     for slot, lw in zip([s_slot, d_slot], [s_lw, d_lw]):
    #         if not int(slot) in ctx.loaded_labwares:
    #             ctx.load_labware(lw.lower(), slot)
                

    # # load tipracks in remaining slots
    # tiprack_type = tiprack_map[pipette_type]
    # tipracks = []
    # for slot in range(1, 13):
    #     if slot not in ctx.loaded_labwares:
    #         tipracks.append(ctx.load_labware(tiprack_type, str(slot)))

    # # load pipette
    # pip = ctx.load_instrument(pipette_type, pipette_mount, tip_racks=tipracks)
    
    # Labware Setup
    tip_rack = ctx.load_labware('opentrons_96_filtertiprack_200ul', '9')
    res1 = ctx.load_labware('usascientific_12_reservoir_22ml', '6')
    dest = ctx.load_labware('axygen_96_wellplate_1100ul', '1')
    source_plates_slots = ['2', '3', '4', '5', '7', '8', '10', '11']
    source = {slot: ctx.load_labware('falcon_96_wellplate_320ul', slot) for slot in source_plates_slots}
    
    # Pipette Setup
    pip = ctx.load_instrument('p300_single_gen2', 'right', tip_racks=[tip_rack])

    # tip_count = 0
    # tip_max = len(tip_rack*96)

    def pick_up():
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace the tips")
            pip.reset_tipracks()
            pip.pick_up_tip()

    def parse_well(well):
        letter = well[0]
        number = well[1:]
        return letter.upper() + str(int(number))
    
    for line in transfer_info:
        _, s_slot, s_well, h, _, d_slot, d_well, vol = line[:8]
        source = ctx.loaded_labwares[
            int(s_slot)].wells_by_name()[parse_well(s_well)].bottom(float(h))
        dest = ctx.loaded_labwares[
            int(d_slot)].wells_by_name()[parse_well(d_well)]
        
        
        # pick_up()
        # pip.transfer(float(vol), source, dest, new_tip='never')
        # pip.drop_tip()
        pick_up()

        # Step 2: Aspirate 100ul liquid from reservoir
        pip.aspirate(100, res1['A1'])

        # Step 3: Dispense the liquid aspirated from reservoir into source well
        pip.dispense(100, source)

        # Step 4: Mix the combined liquid in source well 2-3 times
        # pip.mix(3, 100, source)

        # Step 5: Aspirate from source and Step 6: Dispense to destination
        pip.transfer(float(vol), source, dest, new_tip='never')
        
        pip.drop_tip()
