const CACHE_NAME = "baano-emergency-cache-v1";
const URLS_TO_CACHE = [
	"/",
	"/web",
	"/baano_emergency/static/description/icon.png",
	// Add here all important static assets, templates, CSS, JS files needed offline
];

self.addEventListener("install", (event) => {
	console.log("[PWA] Service Worker installing...");
	event.waitUntil(
		caches.open(CACHE_NAME).then((cache) => {
			console.log("[PWA] Caching app shell");
			return cache.addAll(URLS_TO_CACHE);
		})
	);
	self.skipWaiting();
});

self.addEventListener("activate", (event) => {
	console.log("[PWA] Service Worker activating...");
	event.waitUntil(
		caches.keys().then((cacheNames) => {
			return Promise.all(
				cacheNames
					.filter((name) => name !== CACHE_NAME)
					.map((name) => caches.delete(name))
			);
		})
	);
	self.clients.claim();
});

self.addEventListener("fetch", (event) => {
	event.respondWith(
		caches.match(event.request).then((response) => {
			if (response) {
				console.log("[PWA] Serving from cache:", event.request.url);
				return response;
			}
			console.log("[PWA] Fetching from network:", event.request.url);
			return fetch(event.request);
		})
	);
});
