import asyncio, sys
from playwright.async_api import async_playwright
LV = int(sys.argv[1]) if len(sys.argv) > 1 else 15
SIZES = [('1920x1080', 1920, 1080, 150, 6), ('800x1200', 800, 1200, 104, 5), ('800x800', 800, 800, 96, 4)]
JS = r"""
(a) => {
  document.querySelectorAll('.ov,.hud,.foot,#tip,#finger,#banner,#toast,#hurt,.loading').forEach(function(e){ e.style.display='none'; });
  var d = document.createElement('div');
  d.innerHTML = '<div style="font-family:Jua;font-size:' + a.fs + 'px;line-height:1.02;color:#fff;text-align:center;-webkit-text-stroke:' + Math.round(a.fs*0.09) + 'px #e0577f;paint-order:stroke fill;text-shadow:0 ' + Math.round(a.fs*0.07) + 'px 0 #b83f63, 0 ' + Math.round(a.fs*0.12) + 'px ' + Math.round(a.fs*0.18) + 'px rgba(90,40,40,.35)">Mongle Farm<br><span style="font-size:' + Math.round(a.fs*0.62) + 'px;color:#fff6c2;-webkit-text-stroke-color:#c8661a;text-shadow:0 ' + Math.round(a.fs*0.06) + 'px 0 #8f4a10">Escape</span></div>';
  d.style.cssText = 'position:fixed;left:0;right:0;top:' + a.top + '%;z-index:99;pointer-events:none';
  document.body.appendChild(d);
}
"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        for name, W, H, fs, top in SIZES:
            ctx = await b.new_context(viewport={'width': W, 'height': H}, locale='en-US')
            await ctx.add_init_script("try{localStorage.setItem('mongle-farm-v1', JSON.stringify({max:40,stars:{},sound:false,music:false,coins:0,hat:'none',owned:['none']}))}catch(e){}")
            await ctx.add_init_script("(function(){var P=CanvasRenderingContext2D.prototype,f=P.fillText,s=P.strokeText;function ok(t){return /Mongle Farm|몽글 목장/.test(String(t))}P.fillText=function(t){if(!ok(t))return;return f.apply(this,arguments)};P.strokeText=function(t){if(!ok(t))return;return s.apply(this,arguments)}})();")
            pg = await ctx.new_page()
            await pg.goto('file:///home/claude/work/mfp/index.html'); await pg.wait_for_timeout(3000)
            await pg.evaluate("(l)=>__game.startLevel(l)", LV); await pg.wait_for_timeout(3500)
            await pg.evaluate(JS, {'fs': fs, 'top': top}); await pg.wait_for_timeout(800)
            await pg.screenshot(path='/home/claude/work/mg/covers/mongle_cover_%s.png' % name)
            await ctx.close()
        await b.close()
asyncio.run(main())
