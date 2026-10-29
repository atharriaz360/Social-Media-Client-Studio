import sys, cv2, numpy as np
sys.path.insert(0, '/tmp/claude-0/r')
from comp import load, quad, aspect, phone_screen, tablet_screen, composite, place
from capture import capture
from specs import SPECS
from PIL import Image
R = '/tmp/claude-0/r/'
only = sys.argv[1:] or list(SPECS)
for name in only:
    sp = SPECS[name]
    bg, k, comps = load(sp['plate'], sp['S'])
    comps = comps[:len(sp['dev'])]
    quads, jobs, meta = [], [], []
    dbg = bg.copy()
    for i, (m, d) in enumerate(zip(comps, sp['dev'])):
        q = quad(m, **d.get('q', {})); quads.append(q); a = aspect(q)
        cv2.polylines(dbg, [q.astype(np.int32)], True, (0, 0, 255), 3)
        theme = d.get('theme', 'light'); layout = d.get('layout', 'list')
        # true device screen sizes; the perspective warp does the foreshortening
        if d['kind'] == 'laptop': w, h, dsf = (1512, 950, 2) if d.get('notch', True) else (1440, 900, 2)
        elif d['kind'] == 'phone': w, h, dsf = 393, 852 - 54, 3        # iPhone 15 Pro
        else: w, h, dsf = 1180, 820 - 24, 2                            # iPad Air 11-inch, landscape
        out = R + f'cap_{name}_{i}.png'
        jobs.append((out, d['route'], w, h, dsf, theme, layout)); meta.append((d['kind'], theme, out))
        print(name, i, d['kind'], 'aspect %.3f' % a, 'viewport', w, h)
    cv2.imwrite(R + f'dbg_{name}.jpg', cv2.resize(dbg, None, fx=.4, fy=.4))
    capture(jobs)
    screens = []
    for kind, theme, out in meta:
        if kind == 'phone': screens.append(phone_screen(out, theme == 'dark'))
        elif kind == 'tablet': screens.append(tablet_screen(out, theme == 'dark'))
        else:
            im = Image.open(out).convert('RGB')
            if sp['dev'][len(screens)].get('notch', True):   # notched MacBook Pro, full screen: black band beside the notch
                c = Image.new('RGB', (im.width, im.height + 64), (0, 0, 0)); c.paste(im, (0, 64)); im = c
            screens.append(im)
    img, mask = composite(bg, k, comps, quads, screens, [4 if m['kind']=='phone' else 6 for m in sp['dev']])
    canvas = place(img, mask, 3000, 2250, sp['ox'], sp['oy'])
    cv2.imwrite(R + f'plate_{name}.png', canvas)
    Image.open(R + f'plate_{name}.png').resize((1500, 1125)).save(R + f'pv_{name}.jpg', quality=88)
    print('ok', name)
