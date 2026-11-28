import sys, asyncio, json
from playwright.async_api import async_playwright
HTML = '/home/claude/work/mfp/index.html'
async def run(b, tag, W, H, lang, pre):
    ctx = await b.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, locale=('ko-KR' if lang == 'ko' else 'en-US'))
    if pre: await ctx.add_init_script("try{localStorage.setItem('mongle-farm-v1', JSON.stringify(%s))}catch(e){}" % pre)
    pg = await ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append('PAGE ' + str(e)[:200])); pg.on('console', lambda m: errs.append(m.text[:200]) if m.type == 'error' else None)
    await pg.goto('file://' + HTML); await pg.wait_for_timeout(3500)
    await pg.screenshot(path='/home/claude/work/shots/mg_%s_1.png' % tag)
    out = {'errs': errs}
    if pre:
        for sel in ['#bLevels', '#bLvBack', '#bMis', '#bMisBack', '#bBook', '#bBookBack', '#bShop']:
            await pg.evaluate("(s)=>{var e=document.querySelector(s); if(e) e.click();}", sel); await pg.wait_for_timeout(500)
            await pg.screenshot(path='/home/claude/work/shots/mg_%s_%s.png' % (tag, sel[1:]))
    out['miss'] = await pg.evaluate("window.__mgMissing||[]"); out['lang'] = await pg.evaluate("window.MG_LANG")
    await ctx.close(); return out
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        print('fresh', json.dumps(await run(b, 'fresh', 400, 760, 'en', None), ensure_ascii=False))
        print('title', json.dumps(await run(b, 'title', 400, 760, 'en', '{"max":12,"stars":{"1":3,"2":3},"coins":200,"sound":false,"music":false}'), ensure_ascii=False))
        print('desk', json.dumps(await run(b, 'desk', 1280, 720, 'en', None), ensure_ascii=False))
        await b.close()
asyncio.run(main())
