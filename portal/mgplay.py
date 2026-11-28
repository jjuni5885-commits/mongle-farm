import asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = await b.new_context(viewport={'width': 400, 'height': 760}, locale='en-US'); pg = await ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append('PAGE ' + str(e)[:200]))
        await pg.goto('file:///home/claude/work/mfp/index.html'); await pg.wait_for_timeout(3000)
        for lv in (1, 2, 3):
            for i in range(40):
                if await pg.evaluate("!document.getElementById('ovWin').hidden"): break
                await pg.evaluate("()=>{ var G=__game.G; if(!G||G.done) return; var f=G.animals.filter(a=>a.state==='idle'&&!a.sleep&&__game.checkFree(a).free); if(f.length) __game.tapAnimal(f[0]); }")
                await pg.wait_for_timeout(450)
            await pg.wait_for_timeout(2600)
            await pg.screenshot(path='/home/claude/work/shots/mg_win%d.png' % lv)
            await pg.evaluate("()=>{var b=document.getElementById('bNext'); if(b) b.click();}"); await pg.wait_for_timeout(1500)
        # 실패: 막힌 친구를 계속 누름
        for i in range(12):
            if await pg.evaluate("!document.getElementById('ovFail').hidden"): break
            await pg.evaluate("()=>{ var G=__game.G; if(!G||G.done) return; var f=G.animals.filter(a=>a.state==='idle'&&!__game.checkFree(a).free); if(f.length) __game.tapAnimal(f[0]); }")
            await pg.wait_for_timeout(700)
        await pg.wait_for_timeout(1500); await pg.screenshot(path='/home/claude/work/shots/mg_fail.png')
        print('level', await pg.evaluate("__game.G&&__game.G.L"), 'fail', await pg.evaluate("!document.getElementById('ovFail').hidden"))
        print('miss', json.dumps([m for m in await pg.evaluate("window.__mgMissing") ], ensure_ascii=False)); print('errs', errs)
        await b.close()
asyncio.run(main())
