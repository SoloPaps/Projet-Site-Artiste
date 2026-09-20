import asyncio, json, os, sys
from playwright.async_api import async_playwright
import os as _o; SITE=_o.path.dirname(_o.path.dirname(_o.path.abspath(__file__)))
PAGES=["index.html"]+["oeuvres/"+f for f in sorted(os.listdir(SITE+"/oeuvres")) if f.endswith(".html")]
WIDTHS=[(360,740),(768,1024),(1280,800),(1920,1080)]
async def main():
    res=[]; 
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for page_rel in PAGES:
            for w,h in WIDTHS:
                ctx=await b.new_context(viewport={"width":w,"height":h})
                pg=await ctx.new_page()
                js_err=[]; bad=[]
                pg.on("pageerror",lambda e: js_err.append(str(e)))
                pg.on("response",lambda r: bad.append((r.status,r.url)) if r.status>=400 and r.url.startswith("file")==False and "localhost" in r.url else None)
                await pg.route("**/*",lambda route: route.abort() if route.request.url.startswith(("https://fonts.","https://cdnjs","https://formspree","https://tile")) else route.continue_())
                await pg.goto("file://"+SITE+"/"+page_rel, wait_until="load")
                await pg.wait_for_timeout(500)
                m=await pg.evaluate("""()=>{
                    const d=document.documentElement;
                    const over=[...document.querySelectorAll('body *')].filter(e=>{
                        const r=e.getBoundingClientRect(); const cs=getComputedStyle(e);
                        if(r.width===0||cs.display==='none'||cs.visibility==='hidden') return false;
                        if(cs.position==='fixed') return false;
                        if(e.closest('.nav-drawer')||e.closest('.pf-marquee-wrap')||e.closest('#map-modal')) return false;
                        if(e.closest('div[style*="display:none"]')) return false;
                        return r.right>innerWidth+1;
                    }).slice(0,3).map(e=>e.tagName+'.'+(typeof e.className==='string'?e.className:''));
                    const img=document.querySelector('.oeuvre-img-wrap img');
                    const ib=img?img.getBoundingClientRect():null;
                    return {scrollW:d.scrollWidth,clientW:d.clientWidth,over,
                            img: ib?{w:Math.round(ib.width),h:Math.round(ib.height),nat:[img.naturalWidth,img.naturalHeight],ok:img.naturalWidth>0}:null};
                }""")
                res.append((page_rel,w,m,js_err))
                await ctx.close()
        await b.close()
    fails=0
    for page,w,m,je in res:
        issues=[]
        if m["scrollW"]>m["clientW"]+1: issues.append(f"débordement horizontal {m['scrollW']}>{m['clientW']} {m['over']}")
        if m["img"] and not m["img"]["ok"]: issues.append("image principale non chargée")
        if je: issues.append("erreur JS: "+je[0][:80])
        if issues: fails+=1; print(f"✘ {page:46s} {w:>4}px  "+" | ".join(issues))
    print(f"\n{len(res)} rendus testés ({len(PAGES)} pages × {len(WIDTHS)} largeurs) — {fails} problème(s)")
    # taille de l'image principale par largeur (échantillon)
    print("\nImage principale (largeur×hauteur affichées) :")
    for page,w,m,je in res:
        if m["img"] and page.endswith(("cheval-soleil-2026.html","lesprit-du-fauve-2026.html","deux-voiles-2026.html")):
            print(f"  {page.split('/')[-1]:32s} {w:>4}px → {m['img']['w']}×{m['img']['h']}")
asyncio.run(main())
