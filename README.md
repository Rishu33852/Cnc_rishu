# CNCVerse Cloud Stream Extension

> **Ad-free fork** — all ad redirects, casino popups, and Telegram nags removed.

---

## ⚡ Quick Install (CloudStream)

Add this URL inside **CloudStream → Extensions → Add Repository**:

```
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/builds/CNC.json
```

> Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` after you fork (see steps below).

---

## 🔧 How to Build on GitHub (Step-by-Step)

### Step 1 — Fork this repository

1. Click **Fork** (top-right on GitHub).
2. Keep the repository name or rename it — your choice.
3. Make sure **"Copy the master branch only"** is checked.

---

### Step 2 — Enable GitHub Actions

1. In your fork, click the **Actions** tab.
2. If you see *"Workflows aren't being run on this forked repository"*, click **"I understand my workflows, go ahead and enable them"**.

---

### Step 3 — Give Actions write permission

1. Go to **Settings → Actions → General**.
2. Scroll to **Workflow permissions**.
3. Select **"Read and write permissions"**.
4. Click **Save**.

---

### Step 4 — (Optional) Add secret API keys

The build works fine without secrets — providers that need keys will simply have empty BuildConfig strings and gracefully fall back or skip those features.

If you have the keys, add them at **Settings → Secrets and variables → Actions → New repository secret**:

| Secret name | Used by |
|---|---|
| `MOVIEBOX_SECRET_KEY_DEFAULT` | MovieBoxProvider |
| `MOVIEBOX_SECRET_KEY_ALT` | MovieBoxProviderIN |
| `CASTLE_SUFFIX` | CastleTvProvider |
| `PIKASHOW_API_KEY` | PikashowProvider |
| `PIKASHOW_HMAC_SECRET` | PikashowProvider |
| `CRICIFY_PROVIDER_SECRET1` | CricifyProvider |
| `CRICIFY_PROVIDER_SECRET2` | CricifyProvider |
| `SKLIVE_KEY` / `SKLIVE_IV` | SKTechProvider |
| `CINETV_AES_KEY` / `CINETV_AES_IV` | CineTvProvider |
| *(see `build.gradle.kts` for full list)* | |

---

### Step 5 — Trigger the build

The build runs automatically on every push to `master`.

To trigger it manually:
1. Click **Actions → Build Extensions**.
2. Click **Run workflow → Run workflow**.

The first run takes ~10–15 minutes (downloads Android SDK, Gradle, dependencies).  
Subsequent runs are faster (~3–5 min) thanks to caching.

---

### Step 6 — Get your install URL

After the build succeeds:

1. Click **Actions → Build Extensions → (latest run) → builds branch**.
2. Your personal install URL is:

```
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/builds/CNC.json
```

---

### Step 7 — Install in CloudStream

1. Open **CloudStream**.
2. Tap the **search icon → Extensions (puzzle piece)**.
3. Tap **➕ Add repository**.
4. Paste your URL from Step 6.
5. Tap **Add** → all plugins appear in the extension list.
6. Tap **Install** next to each plugin you want.

---

## 📦 What gets built

| Plugin | Language | Types |
|---|---|---|
| BilibiliProvider | ta | Anime, Movies, TvSeries, Documentary |
| CNCVerse | ta | Movie, TvSeries |
| CastleTvProvider | ta | Movie, TvSeries |
| CineTvProvider | ta | Movie, TvSeries |
| CricifyProvider | ta | Live |
| DesiSerialsProvider | hi | TvSeries |
| DoFlixProvider | ta | TvSeries, Movie |
| EinthusanProvider | ta | Movie |
| GoldenAudiobook | en | Others |
| HDOProvider | ta | Movies, TvSeries |
| HDrezkaProvider | ru | AsianDrama, Anime, TvSeries, Movie |
| LibriVoxAudiobook | en | Others |
| MLSBDProvider | bn | Movie, TvSeries, AnimeMovie, AsianDrama |
| MovieBoxProvider | ta | Movie, TvSeries |
| MovieBoxProviderIN | ta | Movie, TvSeries |
| MovieLinkBDProvider | bn | Movie, TvSeries, AnimeMovie, AsianDrama |
| MoviezwapProvider | te | Movie |
| PikashowProvider | ta | Movie, TvSeries |
| PlayZTVProvider | ta | Live |
| RadioIndiaProvider | ta | Live |
| Rtally | ta | Movie, TvSeries, Anime, AnimeMovie, AsianDrama |
| SKTechProvider | ta | Live |
| StreamFlixProvider | ta | Movie, TvSeries, Anime |
| TamilDhoolProvider | ta | TvSeries |
| TamilUltraProvider | ta | Live |
| Tamilian | ta | Movies |
| Watch32 | en | Movie, TvSeries |
| XonProvider | ta | TvSeries, Movie, Anime |

---

## 🛠 Build System

- **Gradle 8.13** + **Android Gradle Plugin 8.13.2**
- **Kotlin 2.3.0**
- **CloudStream Gradle Plugin** (`com.github.recloudstream.gradle`)
- **JDK 17** (Temurin, via GitHub Actions)
- Outputs: `.cs3` plugin files + `CNC.json` repo manifest → pushed to `builds` branch

---

## 🔄 Automatic Rebuilds

Every `git push` to `master` triggers the workflow automatically.  
You can also go to **Actions → Build Extensions → Run workflow** at any time.

---

## 📄 License

GNU GPL v3 — see [LICENSE](LICENSE).

## ⚠️ DMCA

These extensions function like a browser — they do not host any content.  
All content is served by third-party websites. Users are solely responsible for compliance with their local laws.
