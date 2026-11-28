// Copies the game into www/ for the app build and bundles three.js so the game starts offline.
const fs=require('fs'),path=require('path');
const root=path.join(__dirname,'..'),www=path.join(__dirname,'www');
fs.rmSync(www,{recursive:true,force:true});fs.mkdirSync(www);
let html=fs.readFileSync(path.join(root,'index.html'),'utf8');
html=html.replace('https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.min.js','three.min.js')
  .replace(/<script>if\("serviceWorker"[^<]*<\/script>\n?/,'') // no service worker inside the app
  .replace('<link rel="manifest" href="manifest.webmanifest">\n','');
fs.writeFileSync(path.join(www,'index.html'),html);
for(const f of['icon-192.png','icon-512.png','apple-touch-icon.png'])fs.copyFileSync(path.join(root,f),path.join(www,f));
fs.copyFileSync(path.join(__dirname,'vendor','three.min.js'),path.join(www,'three.min.js'));
console.log('www ready');
