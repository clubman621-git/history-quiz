// オフライン用のキャッシュ（保存した分を先に使う方式）
// アプリは端末に保存した分だけで動き、ふだんはほぼ通信しません。
// index.html などを更新したら、必ず VERSION の数字を上げてください。
// そうすると次に開いたときに新しい版をまとめて取り込み、その次の起動から反映されます。
const VERSION = "history-quiz-v7";
const FILES = ["./", "./index.html", "./manifest.webmanifest", "./icons/icon-180.png", "./icons/icon-512.png", "./fonts/dot.woff2"];

self.addEventListener("install", e => {
  // ブラウザの一時保存を通さず、サーバーから最新を取り込む
  e.waitUntil(
    caches.open(VERSION)
      .then(c => c.addAll(FILES.map(f => new Request(f, { cache: "reload" }))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// 保存した分があればそれを使い、なければ（初回など）ネットから取得
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.open(VERSION).then(c =>
      c.match(e.request, { ignoreSearch: true }).then(hit => hit || fetch(e.request))
    )
  );
});
