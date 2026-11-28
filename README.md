# 몽글 목장 대탈출

얼굴이 향한 쪽이 뚫린 목장 친구를 톡! 눌러서 헛간으로 내보내는 3D 캐주얼 퍼즐 게임이에요.

- 플레이: 휴대폰 브라우저에서 `index.html`을 열면 돼요 (three.js 0.149, 설치 필요 없음).
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
