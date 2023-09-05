def get_values(*names):
    import json
    _all_values = json.loads("""{"pipette_type":"p300_single_gen2","pipette_mount":"left","transfer_csv":"Source Labware,Source Slot,Source Well,Source Aspiration Height Above Bottom (in mm),Dest Labware,Dest Slot,Dest Well,Volume (in ul)\\nfalcon_96_wellplate_320ul,2,A01,1,axygen_96_wellplate_1100ul,1,A01,200\\nfalcon_96_wellplate_320ul,2,A02,1,axygen_96_wellplate_1100ul,1,A02,200\\nfalcon_96_wellplate_320ul,2,A03,1,axygen_96_wellplate_1100ul,1,A03,200\\nfalcon_96_wellplate_320ul,2,A04,1,axygen_96_wellplate_1100ul,1,A04,200\\nfalcon_96_wellplate_320ul,3,A04,1,axygen_96_wellplate_1100ul,1,A05,200\\nfalcon_96_wellplate_320ul,3,A05,1,axygen_96_wellplate_1100ul,1,A06,200\\nfalcon_96_wellplate_320ul,3,A06,1,axygen_96_wellplate_1100ul,1,A07,200\\nfalcon_96_wellplate_320ul,3,A07,1,axygen_96_wellplate_1100ul,1,A08,200\\nfalcon_96_wellplate_320ul,4,A01,1,axygen_96_wellplate_1100ul,1,A09,200\\nfalcon_96_wellplate_320ul,4,A02,1,axygen_96_wellplate_1100ul,1,A10,200\\nfalcon_96_wellplate_320ul,4,A03,1,axygen_96_wellplate_1100ul,1,A11,200\\nfalcon_96_wellplate_320ul,4,A04,1,axygen_96_wellplate_1100ul,1,A12,200\\nfalcon_96_wellplate_320ul,2,B04,1,axygen_96_wellplate_1100ul,1,B01,200\\nfalcon_96_wellplate_320ul,2,D04,1,axygen_96_wellplate_1100ul,1,B02,200\\nfalcon_96_wellplate_320ul,2,E04,1,axygen_96_wellplate_1100ul,1,B03,200\\nfalcon_96_wellplate_320ul,2,G04,1,axygen_96_wellplate_1100ul,1,B04,200\\nfalcon_96_wellplate_320ul,3,B07,1,axygen_96_wellplate_1100ul,1,B05,200\\nfalcon_96_wellplate_320ul,3,C07,1,axygen_96_wellplate_1100ul,1,B06,200\\nfalcon_96_wellplate_320ul,3,D07,1,axygen_96_wellplate_1100ul,1,B07,200\\nfalcon_96_wellplate_320ul,3,E07,1,axygen_96_wellplate_1100ul,1,B08,200\\nfalcon_96_wellplate_320ul,4,B02,1,axygen_96_wellplate_1100ul,1,B09,200\\nfalcon_96_wellplate_320ul,4,C02,1,axygen_96_wellplate_1100ul,1,B10,200\\nfalcon_96_wellplate_320ul,4,D02,1,axygen_96_wellplate_1100ul,1,B11,200\\nfalcon_96_wellplate_320ul,4,E02,1,axygen_96_wellplate_1100ul,1,B12,200\\nfalcon_96_wellplate_320ul,5,E05,1,axygen_96_wellplate_1100ul,1,C01,200\\nfalcon_96_wellplate_320ul,5,G05,1,axygen_96_wellplate_1100ul,1,C02,200\\nfalcon_96_wellplate_320ul,5,H05,1,axygen_96_wellplate_1100ul,1,C03,200\\nfalcon_96_wellplate_320ul,5,B05,1,axygen_96_wellplate_1100ul,1,C04,200\\nfalcon_96_wellplate_320ul,6,C03,1,axygen_96_wellplate_1100ul,1,C05,200\\nfalcon_96_wellplate_320ul,6,H03,1,axygen_96_wellplate_1100ul,1,C06,200\\nfalcon_96_wellplate_320ul,6,B03,1,axygen_96_wellplate_1100ul,1,C07,200\\nfalcon_96_wellplate_320ul,6,D03,1,axygen_96_wellplate_1100ul,1,C08,200\\nfalcon_96_wellplate_320ul,7,B05,1,axygen_96_wellplate_1100ul,1,C09,200\\nfalcon_96_wellplate_320ul,7,C05,1,axygen_96_wellplate_1100ul,1,C10,200\\nfalcon_96_wellplate_320ul,7,D05,1,axygen_96_wellplate_1100ul,1,C11,200\\nfalcon_96_wellplate_320ul,7,E05,1,axygen_96_wellplate_1100ul,1,C12,200\\nfalcon_96_wellplate_320ul,8,B05,1,axygen_96_wellplate_1100ul,1,D01,200\\nfalcon_96_wellplate_320ul,8,C05,1,axygen_96_wellplate_1100ul,1,D02,200\\nfalcon_96_wellplate_320ul,8,D05,1,axygen_96_wellplate_1100ul,1,D03,200\\nfalcon_96_wellplate_320ul,8,E05,1,axygen_96_wellplate_1100ul,1,D04,200\\nfalcon_96_wellplate_320ul,10,B04,1,axygen_96_wellplate_1100ul,1,D05,200\\nfalcon_96_wellplate_320ul,10,C04,1,axygen_96_wellplate_1100ul,1,D06,200\\nfalcon_96_wellplate_320ul,10,D04,1,axygen_96_wellplate_1100ul,1,D07,200\\nfalcon_96_wellplate_320ul,10,E04,1,axygen_96_wellplate_1100ul,1,D08,200"}""")
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
        source = ctx.loaded_labwares[
            int(s_slot)].wells_by_name()[parse_well(s_well)].bottom(float(h))
        dest = ctx.loaded_labwares[
            int(d_slot)].wells_by_name()[parse_well(d_well)]
        pick_up()
        pip.transfer(float(vol), source, dest, new_tip='never')
        pip.drop_tip()
