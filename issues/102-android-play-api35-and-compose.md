# Issue #102: Google Play Target SDK 35 (Android 15) & Jetpack Compose Cleanup

- **Labels**: `android`, `google-play-policy`, `jetpack-compose`
- **Target**: `apps/android` (`minSdk = 29`, `targetSdk = 35`)

## Problem
1. Google Play requires `targetSdk = 35` (Android 15) for new app updates.
2. `MainActivity.kt` and `OrderSyncService.kt` still contain `Build.VERSION.SDK_INT` checks for API 26 (`O`), 28 (`P`), and 29 (`Q`) even though `minSdk` is already `29`.
3. `CatalogScreen.kt` and `build.gradle.kts` still rely on deprecated `accompanist-swiperefresh` and `accompanist-systemuicontroller` instead of native Material 3 and AndroidX edge-to-edge APIs.
