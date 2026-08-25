// Service worker du portfolio.
// v3 : ajoute un cache d'images consultable hors ligne et une vraie page de repli,
// là où v2 renvoyait l'accueil pour n'importe quelle navigation échouée.

const VERSION = 'v3';
const SHELL_CACHE = `chromain-shell-${VERSION}`;
const IMAGE_CACHE = `chromain-images-${VERSION}`;
const PAGE_CACHE = `chromain-pages-${VERSION}`;

// Nombre maximum de photos conservées hors ligne (~340 Ko l'unité en moyenne).
const MAX_IMAGES = 250;

const SHELL_ASSETS = [
  '/',
  '/manifest.json',
  '/favicon.png',
  '/favicon-192.png',
  '/404.html'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE)
      // addAll échoue en bloc si une seule ressource manque : on tolère les absences.
      .then((cache) => Promise.allSettled(SHELL_ASSETS.map((u) => cache.add(u))))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  const keep = [SHELL_CACHE, IMAGE_CACHE, PAGE_CACHE];
  event.waitUntil(
    caches.keys()
      .then((names) => Promise.all(
        names.filter((n) => !keep.includes(n)).map((n) => caches.delete(n))
      ))
      .then(() => self.clients.claim())
  );
});

// Garde le cache d'images borné : on supprime les plus anciennes entrées.
async function trimCache(cacheName, maxEntries) {
  const cache = await caches.open(cacheName);
  const keys = await cache.keys();
  if (keys.length <= maxEntries) return;
  await Promise.all(keys.slice(0, keys.length - maxEntries).map((k) => cache.delete(k)));
}

self.addEventListener('fetch', (event) => {
  const { request } = event;

  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  // On ne met en cache que nos propres ressources : ni R2, ni unpkg, ni analytics.
  if (url.origin !== self.location.origin) return;

  // 1) Navigations : réseau d'abord, puis la page en cache, puis la 404 hors ligne.
  if (request.mode === 'navigate') {
    event.respondWith((async () => {
      try {
        const fresh = await fetch(request);
        const cache = await caches.open(PAGE_CACHE);
        cache.put(request, fresh.clone());
        return fresh;
      } catch (e) {
        return (await caches.match(request))
            || (await caches.match('/404.html'))
            || (await caches.match('/'));
      }
    })());
    return;
  }

  // 2) Photos des galeries : cache d'abord, c'est ce qui rend la consultation
  //    hors ligne réellement utile.
  if (url.pathname.startsWith('/gallery/') && /\.(webp|jpe?g|png|avif)$/i.test(url.pathname)) {
    event.respondWith((async () => {
      const cached = await caches.match(request);
      if (cached) return cached;
      try {
        const fresh = await fetch(request);
        if (fresh.ok) {
          const cache = await caches.open(IMAGE_CACHE);
          await cache.put(request, fresh.clone());
          trimCache(IMAGE_CACHE, MAX_IMAGES);
        }
        return fresh;
      } catch (e) {
        return Response.error();
      }
    })());
    return;
  }

  // 3) Le reste (CSS, JS, polices) : cache d'abord avec repli réseau.
  event.respondWith(
    caches.match(request).then((cached) => cached || fetch(request))
  );
});
