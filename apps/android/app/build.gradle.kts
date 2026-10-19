plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.acme.evergreen"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.acme.evergreen"
        minSdk = 29
        // Needs upgrade to 35 for Google Play annual Target API requirement
        targetSdk = 34
        versionCode = 42
        versionName = "2.4.0"
    }

    buildFeatures {
        compose = true
    }
}

dependencies {
    implementation(platform("androidx.compose:compose-bom:2026.05.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.activity:activity-compose:1.9.3")

    // Deprecated Accompanist libraries superseded by Material 3 PullToRefreshBox & enableEdgeToEdge()
    implementation("com.google.accompanist:accompanist-swiperefresh:0.34.0")
    implementation("com.google.accompanist:accompanist-systemuicontroller:0.34.0")
}
