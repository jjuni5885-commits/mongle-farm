# 몽글 목장 대탈출

얼굴이 향한 쪽이 뚫린 목장 친구를 톡! 눌러서 헛간으로 내보내는 3D 캐주얼 퍼즐 게임이에요.

- 플레이(지인 링크): https://jjuni5885-commits.github.io/mongle-farm/ (휴대폰 브라우저, 설치 필요 없음, three.js 0.149)
- 게임 모음 첫 화면: https://jjuni5885-commits.github.io/Tower-test/
- 같은 방향으로 줄 선 친구들은 맨 앞 친구를 따라 줄줄이 나가요.
- 부딪히면 하트가 줄고, 하트 3개를 다 쓰면 다시 도전해요.

## 앱 빌드 (Android / iOS)
`app/` 폴더는 Capacitor 앱 프로젝트예요. 게임 코드는 그대로 쓰고, 앱 안에서는 AdMob 광고와 스토어 결제가 켜져요.

```
cd app
npm install
npm run android   # Android Studio가 열려요 → Build > Generate Signed Bundle
npm run ios       # Mac에서 Xcode가 열려요 → Product > Archive
```
출시 전에 꼭 바꿀 것: `app/capacitor.config.json`의 appId, AndroidManifest와 Info.plist의 AdMob 앱 ID, 게임 코드의 `AD_IDS` 광고 단위 ID.
스토어 문구와 스크린샷은 `store/` 폴더에 있어요.

## 포털판 (CrazyGames 등)
`portal/` 폴더. 원본 `index.html`에서 `portal/build.py`로 만들어요(영어, 광고/결제 숨김, 외부 호출 0). 자세한 것은 `portal/README.md`.

## 역할 (2026-11-28 정리)
- 게임 고치기는 이 저장소 `index.html`만. 지인 링크, 앱, 포털판이 모두 여기서 나와요
- PC에만 있는 사본을 원본으로 쓰지 않아요
