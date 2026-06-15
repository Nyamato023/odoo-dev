if ("serviceWorker" in navigator) {
	window.addEventListener("load", () => {
		console.log("[PWA] Attempting to register Service Worker...");
		navigator.serviceWorker
			.register("/baano_emergency/static/src/js/service-worker.js")
			.then((registration) => {
				console.log("[PWA] ✅ Service Worker registered:", registration.scope);
			})
			.catch((error) => {
				console.error("[PWA] ❌ Service Worker registration failed:", error);
			});
	});
} else {
	console.warn("[PWA] Service Workers are not supported in this browser.");
}
