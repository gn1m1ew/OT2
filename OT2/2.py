def get_values(*names):
    import json
    _all_values = json.loads("""{"pipette_type":"p300_single_gen2","pipette_mount":"right","transfer_csv":"Source Labware,Source Slot,Source Well,Source Aspiration Height Above Bottom (in mm),Dest Labware,Dest Slot,Dest Well,Volume (in ul)\\nfalcon_96_wellplate_320ul,2,A01,2,axygen_96_wellplate_1100ul,1,A01,100\\nfalcon_96_wellplate_320ul,2,A02,2,axygen_96_wellplate_1100ul,1,A02,100\\nfalcon_96_wellplate_320ul,2,A03,2,axygen_96_wellplate_1100ul,1,A03,100\\nfalcon_96_wellplate_320ul,2,A04,2,axygen_96_wellplate_1100ul,1,A04,100\\nfalcon_96_wellplate_320ul,3,A04,2,axygen_96_wellplate_1100ul,1,A05,100\\nfalcon_96_wellplate_320ul,3,A05,2,axygen_96_wellplate_1100ul,1,A06,100\\nfalcon_96_wellplate_320ul,3,A06,2,axygen_96_wellplate_1100ul,1,A07,100\\nfalcon_96_wellplate_320ul,3,A07,2,axygen_96_wellplate_1100ul,1,A08,100\\nfalcon_96_wellplate_320ul,4,A01,2,axygen_96_wellplate_1100ul,1,A09,100\\nfalcon_96_wellplate_320ul,4,A02,2,axygen_96_wellplate_1100ul,1,A10,100\\nfalcon_96_wellplate_320ul,4,A03,2,axygen_96_wellplate_1100ul,1,A11,100\\nfalcon_96_wellplate_320ul,4,A04,2,axygen_96_wellplate_1100ul,1,A12,100"}""")
    return [_all_values[n] for n in names]


metadata = {
    'protocolName': 'Cherrypicking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.3'
}


def run(ctx):
    
    pipette_type, pipette_mount, transfer_csv = get_values(
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

    # load labware
    transfer_info = [[val.strip().lower() for val in line.split(',')]
                     for line in transfer_csv.splitlines()
                     if line.split(',')[0].strip()][1:]
    for line in transfer_info:
        s_lw, s_slot, d_lw, d_slot = line[:2] + line[4:6]
        for slot, lw in zip([s_slot, d_slot], [s_lw, d_lw]):
            if not int(slot) in ctx.loaded_labwares:
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

    for line in transfer_info:
        _, s_slot, s_well, h, _, d_slot, d_well, vol = line[:8]
        source = ctx.loaded_labwares[int(s_slot)].wells_by_name()[parse_well(s_well)].bottom(float(h))
        dest = ctx.loaded_labwares[int(d_slot)].wells_by_name()[parse_well(d_well)]
        
        pick_up()
        pip.aspirate(100, source)  # Aspirate 100ul from reservoir
        pip.dispense(100, source)  # Dispense back to the same reservoir (source well)
        pip.mix(3, 100, source)  # Mix 3 times with 100ul
        pip.aspirate(200, source)  # Aspirate 200ul from source well after mixing
        pip.dispense(float(vol), dest)  # Dispense to the destination well
        pip.drop_tip()
