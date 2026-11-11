"""Fresh real screens from the latest build.
python3 capture_all.py -> screens/{desktop,tablet,phone}-{light,dark}-{view}.png (Etsy _Screens-Latest set)
                        + /tmp/claude-0/v/ss/*  real interaction states for video.py (with tap targets in ss/taps.json)"""
import json
from playwright.sync_api import sync_playwright
APP = 'file:///tmp/claude-0/b/1-SELL-THIS/Brief-to-Approved.html'
R = '/tmp/claude-0/r/screens/'; V = '/tmp/claude-0/v/ss/'
VIEWS = ['overview', 'content', 'calendar', 'approvals', 'assets', 'brief', 'reports', 'library', 'settings']
SIZES = {'desktop': (1512, 945, 2), 'tablet': (1180, 796, 2), 'phone': (393, 798, 3)}
import sys
ONLY_INTERACTIONS = '--interactions' in sys.argv
SETS = [('desktop', 'light'), ('desktop', 'dark'), ('tablet', 'light'), ('phone', 'light'), ('phone', 'dark')]

def ctx(b, kind, theme='light', layout='list'):
    w, h, dsf = SIZES[kind]; m = kind == 'phone'
    c = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=dsf, is_mobile=m, has_touch=m,
                      color_scheme=theme, reduced_motion='reduce')
    c.add_init_script("try{localStorage.setItem('brief-approved-ui-v5'," + json.dumps(json.dumps({'theme': theme, 'focus': False, 'layout': layout})) + ")}catch(e){}")
    return c

def box(pg, sel):
    bb = pg.locator(sel).first.bounding_box(); return [bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2]

def star(pg):
    pg.locator(':text("Approved now")').first.evaluate("e=>e.scrollIntoView({block:'center'})"); pg.wait_for_timeout(300)

def shot(pg, name, wait=350):
    pg.wait_for_timeout(wait); pg.screenshot(path=V + name + '.png')

with sync_playwright() as p:
    b = p.chromium.launch()
    for kind, theme in SETS:                                   # 1) full real screen set
        if ONLY_INTERACTIONS: continue
        c = ctx(b, kind, theme); pg = c.new_page()
        for v in VIEWS:
            pg.goto(APP + '#' + v); pg.wait_for_timeout(700); pg.screenshot(path=R + f'{kind}-{theme}-{v}.png')
        c.close()
    taps = {}
    def run(kind, record):                                     # 2) real interactions: checks -> approval
        c = ctx(b, kind); pg = c.new_page(); pg.goto(APP + '#overview'); pg.wait_for_timeout(800)
        if record: shot(pg, f'{kind}_ov0')
        sel = '.hero [data-edit], [data-edit]'
        if record: taps[f'{kind}_run'] = box(pg, sel)
        pg.locator(sel).first.click()
        if record: shot(pg, f'{kind}_ed0')
        pg.locator('dialog[open] input[name=facts]').scroll_into_view_if_needed()
        tog = 'dialog[open] label:has(input[name=facts])'
        if record: shot(pg, f'{kind}_ed1'); taps[f'{kind}_facts'] = box(pg, tog)
        pg.locator(tog).first.click()
        if record: shot(pg, f'{kind}_ed2'); taps[f'{kind}_save'] = box(pg, 'dialog[open] button[type=submit]')
        pg.locator('dialog[open] button[type=submit]').first.click()
        if record: shot(pg, f'{kind}_saved', 250); taps['toast1'] = pg.locator('#toast').inner_text()
        pg.goto(APP + '#approvals'); pg.wait_for_timeout(700)
        if record: shot(pg, f'{kind}_ap0'); taps[f'{kind}_rec'] = box(pg, '[data-approve]')
        pg.locator('[data-approve]').first.click(); pg.wait_for_timeout(350)
        if record: shot(pg, f'{kind}_dlg0'); taps[f'{kind}_ev'] = box(pg, 'dialog[open] input[name=evidence]')
        ev = pg.locator('dialog[open] input[name=evidence]').first; ev.click()
        msg = 'Email from Avery, 2 Nov'
        for i in range(0, len(msg), 3):
            ev.type(msg[i:i + 3])
            if record: shot(pg, f'{kind}_type{i // 3:02d}', 60)
        if record: taps[f'{kind}_typeN'] = (len(msg) + 2) // 3; taps[f'{kind}_recbtn'] = box(pg, '#approval-form button.btn-primary')
        pg.locator('#approval-form button.btn-primary').first.click()
        if record: shot(pg, f'{kind}_ap1', 250); taps['toast2'] = pg.locator('#toast').inner_text()
        pg.goto(APP + '#overview'); pg.wait_for_timeout(800)
        if kind == 'tablet': star(pg)
        shot(pg, f'{kind}_ov1')
        c.close()
    run('phone', True)
    c = ctx(b, 'tablet'); pg = c.new_page(); pg.goto(APP + '#overview'); pg.wait_for_timeout(800); star(pg)
    shot(pg, 'tablet_ov0'); taps['tablet_star'] = box(pg, ':text("Approved now")'); c.close()
    run('tablet', False)
    json.dump(taps, open(V + 'taps.json', 'w'), indent=1); print(taps)
    b.close()
