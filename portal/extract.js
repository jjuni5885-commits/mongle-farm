// 몽글 index.html의 한글: HTML 글자/속성, 스크립트 문자열/템플릿. node extract.js index.html > lits.json
const fs = require('fs');
const acorn = require('/home/claude/work/tools/node_modules/acorn'), walk = require('/home/claude/work/tools/node_modules/acorn-walk');
const src = fs.readFileSync(process.argv[2], 'utf8');
const HAN = /[ᄀ-ᇿㄱ-ㆎ가-힣]/;
const out = [];
// 스크립트 블록
const re = /<script>([\s\S]*?)<\/script>/g; let m;
while ((m = re.exec(src))) {
  const code = m[1]; if (!HAN.test(code)) continue;
  let ast; try { ast = acorn.parse(code, { ecmaVersion: 2022, locations: true }); } catch (e) { console.error('parse', e.message); continue; }
  walk.full(ast, n => {
    if (n.type === 'Literal' && typeof n.value === 'string' && HAN.test(n.value)) out.push({ k: 'lit', s: n.value, l: n.loc.start.line });
    if (n.type === 'TemplateLiteral') {
      const q = n.quasis.map(x => x.value.cooked); if (!q.some(x => HAN.test(x))) return;
      let key = q[0]; const ex = [];
      for (let i = 0; i < n.expressions.length; i++) { const e = n.expressions[i]; ex.push(code.slice(e.start, e.end)); key += '{' + i + '}' + q[i + 1]; }
      out.push({ k: 'tpl', s: key, ex, l: n.loc.start.line });
    }
  });
}
// HTML 글자와 속성(스크립트, 스타일 밖)
const body = src.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<style[\s\S]*?<\/style>/g, '');
const tx = body.replace(/<svg[\s\S]*?<\/svg>/g, '');
(tx.match(/>([^<]+)</g) || []).forEach(t => { const s = t.slice(1, -1).trim(); if (HAN.test(s)) out.push({ k: 'html', s }); });
(tx.match(/(aria-label|placeholder|title|content)="([^"]*)"/g) || []).forEach(a => { const s = a.replace(/^[^"]*"|"$/g, ''); if (HAN.test(s)) out.push({ k: 'attr', s }); });
process.stdout.write(JSON.stringify(out));
