# 몽글 목장 대탈출 포털판 (CrazyGames 등 게임 포털 제출용)

원본은 하나다: 저장소 맨 위 `index.html`. 지인 링크(https://jjuni5885-commits.github.io/mongle-farm/)와 앱(`app/`)이 이 파일을 쓰고, 포털판은 이 파일에서 `build.py`가 만든다. 포털판을 손으로 고치지 않는다.

## 빌드
```
cd portal
npm pack three@0.149.0 && tar xzf three-0.149.0.tgz          # three.min.js (r149)
python3 build.py ../index.html package/build/three.min.js en.tsv out
# → out/index.html 한 파일(약 860KB). 커밋하지 않고 zip으로 포털에 제출
```
원본에 새 한글 글자를 넣었으면 `font.py`로 `jua_sub.woff2`를 다시 자르고, 새 문구는 `en.tsv`에 영어를 더한다.

## 포털판이 원본과 다른 점 (build.py가 바꿈)
- 홈 화면 설치(manifest, 아이콘), 서비스 워커, 구글 글꼴 외부 호출 제거. Jua 글꼴은 쓰는 글자만 잘라 파일 안에
- three.js r149를 CDN 대신 파일 안에(외부 호출 0)
- 영어: 한국어 사용자는 한국어, 나머지는 영어(`mg_i18n.js`, `en.tsv`)
- 광고 없음, 앱 결제, 공유, 진행 옮기기, 카카오 안내 숨김(포털 1단계 요건)
- 처음 온 사람은 메뉴 없이 1레벨부터

## 이 폴더
- `CrazyGames_요건점검.md`: v1 요건 자체 점검(2026-11-28)
- `covers/`: 포털 표지 3장
- `mgcover.py`, `mgshot.py`, `mgplay.py`, `extract.js`: 표지, 화면, 자동 플레이 시험 도구(작업 공간 경로가 박혀 있어 쓸 때 맞춤)

## 확인 (2026-11-28)
- 이 저장소 `index.html`로 `build.py`를 돌린 결과가 PC2 `C:\Users\jjuni\AI수익사업\몽글목장_포털판\index.html`(v1)과 바이트까지 같음
