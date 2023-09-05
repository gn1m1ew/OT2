from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Ethanol Distribution',
    'description': '''This protocol is a simple program that distributes 500uL 
                    of ethanol to each well of four 96-well plates and 275uL of 
                    ethanol to each well in two other plates. It uses an eight tip
                    rack that should be located on the left side.
                    Deck Locations: 
                    1: Reservoir Plate #1
                    2: Reservoir Plate #2
                    3: 500uL Plate #1
                    4: 500uL Plate #2
                    5: 500uL Plate #3
                    6: 500uL Plate #4
                    7: 275uL Plate #1
                    8: 275uL Plate #2 
                    9: Tiprack
                    10: Empty
                    11: Empty ''',
    'author': 'Matthew Meyer'
    }

def run(protocol: protocol_api.ProtocolContext):
    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 9)
    res1 = protocol.load_labware('thermoscientfic_1_reservoir_345000ul', 1)
    res2 = protocol.load_labware('thermoscientfic_1_reservoir_345000ul', 2)

    large_plate1 = protocol.load_labware('kingfisher_96_wellplate_2000ul', 3) 
    large_plate2 = protocol.load_labware('kingfisher_96_wellplate_2000ul', 4)
    large_plate3 = protocol.load_labware('kingfisher_96_wellplate_2000ul', 5)
    large_plate4 = protocol.load_labware('kingfisher_96_wellplate_2000ul', 6)
    small_plate1 = protocol.load_labware('kingfisher_96_wellplate_2000ul', 7)
    small_plate2 = protocol.load_labware('kingfisher_96_wellplate_2000ul', 8)

    large_plates = [large_plate1, large_plate2, large_plate3, large_plate4]
    small_plates = [small_plate1, small_plate2]
    cols = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12']

    pipettes = protocol.load_instrument('p300_multi_gen2', 'left', [tips])

    pipettes.pick_up_tip(tips['A1'])

    # large plates should take 192000uL of ethanol, not enough to drain reservoir
    for plate in large_plates:
        for col in cols:
            pipettes.aspirate(300, res1['A1'])
            pipettes.dispense(300, plate[col])
            pipettes.aspirate(200, res1['A1'])
            pipettes.dispense(200, plate[col])
            
    # small plates will need 52800uL of ethanol, still not enough drain reservoir
    for plate in small_plates:
        for col in cols:
            pipettes.aspirate(275, res1['A1'])
            pipettes.dispense(275, plate[col])