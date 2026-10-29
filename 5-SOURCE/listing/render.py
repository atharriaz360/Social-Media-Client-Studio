import sys
from playwright.sync_api import sync_playwright
from PIL import Image
src,out=sys.argv[1],sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':3000,'height':2250})
    pg.goto('file://'+src); pg.wait_for_timeout(600)
    pg.screenshot(path='/tmp/claude-0/w/_r.png'); b.close()
im=Image.open('/tmp/claude-0/w/_r.png').convert('RGB'); im.save(out,quality=92,subsampling=0)
im.resize((1500,1125)).save('/tmp/claude-0/w/view.jpg',quality=90)
w,h=im.size; cw=int(h*4/5); x=(w-cw)//2
im.crop((x,0,x+cw,h)).resize((240,300),Image.LANCZOS).save('/tmp/claude-0/w/t45.png')
x=(w-h)//2; im.crop((x,0,x+h,h)).resize((220,220),Image.LANCZOS).save('/tmp/claude-0/w/tsq.png')
