#!/usr/bin/env python

#test custom pcr plates, move water from first row to second

from opentrons import protocol_api
metadata = {'apiLevel': '2.11'}

def run(protocol: protocol_api.ProtocolContext):
    protocol.home()
    plate = protocol.load_labware('tethystestrun2', 1) #our_well_plate
    tiprack_multi = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
    pipette_multi = protocol.load_instrument('p300_multi', mount = 'right', tip_racks=[tiprack_multi])
    
    #This loads a Well Plate in slot 1 and an Opentrons 300 µL Tiprack in slot 2 
    #and uses a P300 Multi pipette. can modify to add more pipettes/tips etc.
    
    #basic_transfer with multichannel pipette. #moves first row 100ul to second row
    pipette_multi.transfer(100, plate.wells_by_name()['A1'], plate.wells_by_name()['A2'])
