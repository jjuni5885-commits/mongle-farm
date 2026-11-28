// network-first: always try the newest game, fall back to the last copy when offline
const C='mongle-v1';
self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET')return;
  let q=r;if(r.mode==='navigate'){try{q=new Request(r,{cache:'no-cache'})}catch(x){}} // 게임 페이지는 브라우저 캐시를 건너뛰고 매번 새 버전 확인(안 바뀌면 304)
  e.respondWith(fetch(q).then(res=>{if(res&&(res.ok||res.type==='opaque')){const cp=res.clone();caches.open(C).then(c=>c.put(r,cp))}return res}).catch(()=>caches.match(r,{ignoreSearch:true})))});
