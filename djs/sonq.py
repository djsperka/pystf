'''
Created on Jun 1, 2023

@author: dan
'''

import sys
import os
import sonpy

def print_event_sample(smrx, ch):
    # Get one event
    ev = smrx.ReadEvents(ch, 1, -1)
    if len(ev) == 1:
        print(f'ChanID {ch}, found an event:', ev)
        
        # This filter should allow all events through:
        filter_allow_all = sonpy.lib.MarkerFilter()
        print('filter_allow_all mode: ', filter_allow_all.GetMode())
        print('filter_allow_all state: ', filter_allow_all.GetState(0))
        ev_all = smrx.ReadEvents(ch, 1, -1, Filter=filter_allow_all)
        print('result using filter_allow_all: ', ev_all)
        print('\n')
        filter_allow_none = sonpy.lib.MarkerFilter()
        filter_allow_none.SetMode(sonpy.lib.FilterMode.First)
        filter_allow_none.SetItem(0, -1, sonpy.lib.FilterSet.Clear)
        print('filter_allow_none mode: ', filter_allow_none.GetMode())
        print('filter_allow_none state: ', filter_allow_none.GetState(0))

        ev_none = smrx.ReadEvents(ch, 1, -1, Filter=filter_allow_none)
        
        print('result using filter_allow_none: ', ev_none)
        print('\n')
        
        mk_all = smrx.ReadMarkers(ch, 3, -1, Filter=filter_allow_all)
        print('ReadMarkers using filter_allow_all\n: ', mk_all)
        print('\n')

        
    else:
        print(f'ChanID {ch}, no events found\n')


def print_marker_sample(smrx, ch):
    mk = smrx.ReadMarkers(ch, 3, -1)
    if len(mk) > 0:
        print(f'ChanID {ch}, first 3 markers:\n', mk)
        
        # Default marker constructor gives a filter that allows all events through:
        filter_allow_all = sonpy.lib.MarkerFilter()
        print('filter_allow_all mode: ', filter_allow_all.GetMode())
        print('filter_allow_all state: ', filter_allow_all.GetState(0))
        mk_all = smrx.ReadMarkers(ch, 3, -1, Filter=filter_allow_all)
        print('result using filter_allow_all\n: ', mk_all)
        print('\n')
        
        # make a filter that allows nothing through
        filter_allow_none = sonpy.lib.MarkerFilter()
        filter_allow_none.SetMode(sonpy.lib.FilterMode.First)
        filter_allow_none.SetItem(0, -1, sonpy.lib.FilterSet.Clear)
        print('filter_allow_none mode: ', filter_allow_none.GetMode())
        print('filter_allow_none state: ', filter_allow_none.GetState(0))
        
        mk_none = smrx.ReadMarkers(ch, 3, -1, Filter=filter_allow_none)
        print('result using filter_allow_none:\n', mk_none)
        print('\n')

        # Make a filter to select only marker codes 3 and 6 on first level, which is level 0. 
        # To fetch marker 3, set item 3. No zero-index business with the markers. 
        filter_allow_36 = sonpy.lib.MarkerFilter()
        filter_allow_36.SetMode(sonpy.lib.FilterMode.First)
        filter_allow_36.SetItem(0, -1, sonpy.lib.FilterSet.Clear)
        filter_allow_36.SetItem(0, 3, sonpy.lib.FilterSet.Set)
        filter_allow_36.SetItem(0, 6, sonpy.lib.FilterSet.Set)

        print('filter_allow_36 mode: ', filter_allow_36.GetMode())
        print('filter_allow_36 state: ', filter_allow_36.GetState(0))

        mk_36 = smrx.ReadMarkers(ch, 3, -1, Filter=filter_allow_36)
        
        print('result using filter_allow_36:\n', mk_36)
        print('\n')
    else:
        print(f'ChanID {ch}, no markers found\n')
        
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: python sonq.py <smrx-file-with-EventBoth-channels>')
        exit(-1)    
    elif not os.path.isfile(sys.argv[1]):
        print(f'Cannot find file {sys.argv[1]}\nusage: python sonq.py <smrx-file-with-EventBoth-channels>')
        exit(-1)    
        
            
    # open smrx read-only
    smrx = sonpy.lib.SonFile(sys.argv[1], True)
    if smrx.GetOpenError() != 0:
        print('Error opening file (%s): %s' % (sys.argv[1], sonpy.lib.GetErrorString(smrx.GetOpenError())))
        exit(-1)
        
    # file opened, iterate through channels. If type==EventBoth, try to read some events
    for i in range(smrx.MaxChannels()):
        if smrx.ChannelType(i) == sonpy.lib.DataType.EventBoth:
            print(10*'*', i, smrx.ChannelType(i), 10*'*', '\n')
            print_event_sample(smrx, i)
        elif smrx.ChannelType(i) == sonpy.lib.DataType.Marker:
            print(10*'*', i, smrx.ChannelType(i), 10*'*', '\n')
            print_marker_sample(smrx, i)
