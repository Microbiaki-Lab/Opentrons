#!/usr/bin/env python


#PCR Prep: Make the Master Mix 
   
#Setup on Machine: 
#p1000 pipette on left, p300 pipette on right.
#Slots 5 and 6 are 1000mL tip racks
#1 and 3 are SNAPCAP 2ML TUBERACK, Opentrons 24 Tube Rack with Eppendorf 2 mL Safe-Lock Snapcap
#4 is 12 channel reservoir, USA Scientific 12 Well Reservoir 22 mL
    
#modify master_mix_csv accordingly to calculate amounts:
# slot (1, 2) and well (A1 - D6) describe source location of the reagent
#Make sure you do not reuse the same well in the same slot
#Keep the headers, enter the data here in "all_values=json.loads


#need to change the volume here as well
def get_values(*names):
    import json
    _all_values = json.loads("""{"right_pipette":"p1000_single_gen2","left_pipette":"p300_single_gen2","master_mix_csv":"Reagent,Slot,Well,Volume\\nBuffer,1,A2,3\\nMgCl,1,A3,40\\ndnNTPs,2,A2,90\\nddH2O,2,A3,248\\nPrimer_Fwd,1,A4,25\\nPrimer_Rev,1,A5,25\\n"}""")
    return [_all_values[n] for n in names]


metadata = {
    'protocolName': 'PCR Prep',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.2'
}


def run(protocol_context):
    [left_pipette, right_pipette, master_mix_csv] = get_values( 
        "left_pipette", "right_pipette", "master_mix_csv")

    if not left_pipette and not right_pipette:
        raise Exception('You have to define at least 1 pipette.')

    pipette_l = None
    pipette_r = None

    for pip, mount, slot in zip(
            [left_pipette, right_pipette], ['left', 'right'], ['5', '6']):

        if pip:
            range = pip.split('_')[0][1:]
            rack = 'opentrons_96_tiprack_' + range + 'ul'
            tiprack = protocol_context.load_labware(rack, slot)
            if mount == 'left':
                pipette_l = protocol_context.load_instrument(
                    pip, mount, tip_racks=[tiprack])
            else:
                pipette_r = protocol_context.load_instrument(
                    pip, mount, tip_racks=[tiprack])

    # labware setup
    snaprack = protocol_context.load_labware(
        'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap',
        '1',
        'snapcap 2ml tuberack'
    )
    screwrack = protocol_context.load_labware(
        'opentrons_24_tuberack_generic_2ml_screwcap',
        '2',
        'screwcap 2ml tuberack'
    )
    res12 = protocol_context.load_labware( #might need to change this for 
        'usascientific_12_reservoir_22ml', '3', '12-channel reservoir')
    reagents = {
        '1': snaprack,
        '2': screwrack,
        '3': res12
    }

    # determine which pipette has the smaller volume range
    if pipette_l and pipette_r:
        if left_pipette == right_pipette:
            pip_s = pipette_l
            pip_l = pipette_r
        else:
            if pipette_l.max_volume < pipette_r.max_volume:
                pip_s, pip_l = pipette_l, pipette_r
            else:
                pip_s, pip_l = pipette_r, pipette_l
    else:
        pipette = pipette_l if pipette_l else pipette_r

    # destination
    mastermix_dest = res12.wells()[0]

    info_list = [
        [cell.strip() for cell in line.split(',')]
        for line in master_mix_csv.splitlines()[1:] if line
    ]

    for line in info_list[1:]:
        source = reagents[line[1]].wells(line[2].upper())
        vol = float(line[3])
        if pipette_l and pipette_r:
            if vol <= pip_s.max_volume:
                pipette = pip_s
            else:
                pipette = pip_l
        pipette.transfer(vol, source, mastermix_dest)

    #Add the taq manually, then run the next protocol for distributing mastermix in 96 well plate, adding mastermix
    
    
