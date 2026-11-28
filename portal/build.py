# 몽글 목장 대탈출 포털판 만들기: python3 build.py <원본 index.html> <three.min.js> <en.tsv> <출력 폴더>
import sys, re, json, base64, os
HERE = os.path.dirname(os.path.abspath(__file__))   # 이 스크립트가 있는 폴더(uniq.json, jua_sub.woff2, mg_i18n.js)
src, three, tsv, outd = sys.argv[1:5]
s = open(src, encoding='utf8').read()
U = json.load(open(os.path.join(HERE, 'uniq.json'), encoding='utf8'))
rows = []
for line in open(tsv, encoding='utf8'):
    line = line.rstrip('\n')
    if not line.strip(): continue
    p = line.split('\t')
    if p[0] == 'K': rows.append([p[1], p[2]])
    else: rows.append([U[int(p[0])]['s'].strip(), p[1]])
def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    if n != cnt: raise SystemExit('바꿀 곳 %d개 (기대 %d): %r' % (n, cnt, old[:80]))
    s = s.replace(old, new)
# 머리: 홈 화면 설치, 서비스 워커, 외부 글꼴, 미리보기 줄 제거
for pat in [r'<link rel="manifest"[^>]*>\n', r'<link rel="icon"[^>]*>\n', r'<link rel="apple-touch-icon"[^>]*>\n', r'<meta name="apple-mobile-web-app-[^>]*>\n', r'<meta name="mobile-web-app-capable"[^>]*>\n',
            r'<script>if\("serviceWorker" in navigator\)[^<]*</script>\n', r'<meta name="claude:viewport-fit-sides"[^>]*>\n', r'<link rel="preconnect" href="https://fonts.googleapis.com">\n', r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n']:
    s, n = re.subn(pat, '', s)
    if not n: print('없음:', pat)
rep('<html lang="ko">', '<html lang="en">')
rep('<title>몽글 목장 대탈출</title>', '<title>Mongle Farm Escape</title>\n<style>@font-face{font-family:\'Jua\';src:url(data:font/woff2;base64,' + base64.b64encode(open(os.path.join(HERE, 'jua_sub.woff2'), 'rb').read()).decode() + ') format(\'woff2\');font-display:block}\n' +
    '#bAdHeart,#bAdDouble,#bAdCoin,#bShare,#bShareWin,#bInstall,#iosTip,#bMove,#kakaoNote,#iapGrid,.shopH{display:none!important}</style>')
# three.js: 외부 CDN 대신 파일 안에
rep('<script src="https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.min.js"></script>', '<script>' + open(three, encoding='utf8').read().replace('</script', '<\\/script') + '</script>\n<script>var MG_DICT=' + json.dumps(rows, ensure_ascii=False) + ';\n' + open(os.path.join(HERE, 'mg_i18n.js'), encoding='utf8').read() + '</script>')
# 카카오 전환 끔, 판 사이 광고 없음, 간판의 광고 문의와 공유 홍보 빼기
rep("const IN_KAKAO=/KAKAOTALK/i.test(navigator.userAgent);", "const IN_KAKAO=false;")
rep("inter(cb){save.adCnt=", "inter(cb){return cb();save.adCnt=")
s, n = re.subn(r"const BILL_ADS=\[\{t:'모자 가게'.*?\];", "const BILL_ADS=[{t:'모자 가게',s:'새 모자 입고!',bg:'#ffc9dc',fg:'#d6336c',ic:'hat'},{t:'오늘의 미션',s:'깨면 코인 듬뿍',bg:'#c8f5b8',fg:'#2e8a1e',ic:'star'}];", s, flags=re.S)
if n != 1: raise SystemExit('BILL_ADS 못 찾음')
rep("const SHARE_URL='https://jjuni5885-commits.github.io/mongle-farm/';", "const SHARE_URL=location.href.split('#')[0];")
# 처음 온 사람은 바로 1레벨
rep("startLevel(Math.max(4,Math.min(save.max,8)));state='menu';$('tip').hidden=true;",
    "if((save.max||1)<=1&&!Object.keys(save.stars||{}).length){show(null);startLevel(1)}else{startLevel(Math.max(4,Math.min(save.max,8)));state='menu';$('tip').hidden=true;}")
os.makedirs(outd, exist_ok=True)
open(os.path.join(outd, 'index.html'), 'w', encoding='utf8').write(s)
print('rows', len(rows), 'bytes', len(s.encode('utf8')))
left = re.findall(r'https?://[^\s"\'<>)]+', s)
print('남은 주소', sorted(set(left))[:20])
