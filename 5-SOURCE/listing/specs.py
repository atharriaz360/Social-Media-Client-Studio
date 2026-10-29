"""Image specs: plate id, scale, canvas offset, devices in component order (largest green area first)."""
LAPTOP_OCC = dict(top=(.2, .8), bot=(.1, .6), lef=(.2, .8), rig=(.08, .25))   # laptop screen partly hidden by phone at bottom-right
SPECS = {
 '01-Hero':            dict(plate=1, S=1.75, ox=546, oy=-10,
                            dev=[dict(kind='laptop', route='approvals', q=LAPTOP_OCC), dict(kind='phone', route='approvals')]),
 '03-Content-Board':   dict(plate=7, S=2.0, ox=760, oy=-100,
                            dev=[dict(kind='laptop', route='content', layout='board', q=LAPTOP_OCC), dict(kind='phone', route='content')]),
 '05-Calendar-Reports':dict(plate=5, S=2.1, ox=160, oy=-250,
                            dev=[dict(kind='tablet', route='calendar'), dict(kind='phone', route='reports')]),
 '06-Phone':           dict(plate=4, S=2.373, ox=0, oy=-250,
                            dev=[dict(kind='phone', route='overview'), dict(kind='phone', route='approvals', theme='dark')]),
 '10-Private-Offline': dict(plate=5, S=1.7, ox=880, oy=-20,
                            dev=[dict(kind='tablet', route='overview', theme='dark'), dict(kind='phone', route='settings', theme='dark')]),
}

for r in ['overview', 'content', 'calendar', 'approvals', 'brief', 'reports']:
    SPECS['v_' + r] = dict(plate=1, S=1.75, ox=546, oy=-10, dev=[dict(kind='laptop', route=r, q=LAPTOP_OCC), dict(kind='phone', route=r)])
SPECS['v_dark'] = dict(plate=1, S=1.75, ox=546, oy=-10, dev=[dict(kind='laptop', route='overview', theme='dark', q=LAPTOP_OCC), dict(kind='phone', route='overview', theme='dark')])
# v3 hero: bigger devices, richest real screen (overview) on both devices
SPECS['01-Hero-v3'] = dict(plate=1, S=1.98, ox=178, oy=-196,
    dev=[dict(kind='laptop', route='overview', q=LAPTOP_OCC), dict(kind='phone', route='overview')])
