"""Capture real app screens at an exact viewport. Usage from python: capture(jobs) with jobs=[(out, route, w, h, dsf, theme, layout)]"""
import json
from playwright.sync_api import sync_playwright
APP = 'file:///tmp/claude-0/b/1-SELL-THIS/Brief-to-Approved.html'
def capture(jobs):
    with sync_playwright() as p:
        b = p.chromium.launch()
        for out, route, w, h, dsf, theme, layout in jobs:
            mobile = w < 600
            ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=dsf, is_mobile=mobile, has_touch=mobile,
                                color_scheme=theme)
            ctx.add_init_script(f"try{{localStorage.setItem('brief-approved-ui-v5',{json.dumps(json.dumps({'theme': theme, 'focus': False, 'layout': layout}))})}}catch(e){{}}")
            pg = ctx.new_page(); pg.goto(APP + '#' + route); pg.wait_for_timeout(900)
            pg.screenshot(path=out); ctx.close()
        b.close()
