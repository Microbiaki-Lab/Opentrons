#!/usr/bin/env python

#test custom pcr plates, move water from first row to second

from opentrons import protocol_api
metadata = {'apiLevel': '2.11'}

def run(protocol: protocol_api.ProtocolContext):
    protocol.home()
    plate = protocol.load_labware('tethystestrun2', 1)
    tiprack_multi = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
    pipette_multi = protocol.load_instrument('p300_multi', mount = 'right', tip_racks=[tiprack_multi])
    
    pipette_multi.transfer(100, plate.wells_by_name()['A1'], plate.wells_by_name()['A2'])
