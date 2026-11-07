// NovaCHAT service worker
//  - 離線也能開：網站自己的檔案（index.html、manifest）存在手機裡
//    - index.html：先上網抓最新（3 秒內沒回應就用存的），一更新馬上生效
//    - 其他檔案：先用存的秒開，背景再更新
//  - 聊天後端 /api/* 不快取，照常連網（之後接真後端用）
const CACHE = 'novachat-v1';
const PRECACHE = ['./index.html', './manifest.json'];
const PAGE = new URL('./index.html', self.location).href;

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE).then((c) => c.addAll(PRECACHE.map((u) => new Request(u, { cache: 'reload' })))));
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(caches.keys()
    .then((keys) => Promise.all(keys.filter((k) => k.startsWith('novachat-') && k !== CACHE).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

function timeout(ms) { return new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), ms)); }

async function pageRequest(request) {
  const cache = await caches.open(CACHE);
  try {
    const res = await Promise.race([fetch(request), timeout(3000)]);
    if (res.ok) cache.put(PAGE, res.clone());
    return res;
  } catch {
    const cached = await cache.match(PAGE);
    if (cached) return cached;
    throw new Error('offline and not cached');
  }
}

async function assetRequest(event) {
  const cache = await caches.open(CACHE);
  const cached = await cache.match(event.request, { ignoreSearch: true });
  const update = fetch(event.request).then((res) => { if (res.ok) cache.put(event.request, res.clone()); return res; }).catch(() => null);
  if (cached) { event.waitUntil(update); return cached; }
  return (await update) || Response.error();
}

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin || url.pathname.includes('/api/')) return;
  if (request.headers.has('range')) return;
  if (request.mode === 'navigate' || url.pathname.endsWith('/index.html') || url.pathname.endsWith('/')) {
    event.respondWith(pageRequest(request));
    return;
  }
  event.respondWith(assetRequest(event));
});
