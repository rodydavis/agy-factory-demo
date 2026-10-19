package com.acme.evergreen

import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.acme.evergreen.ui.CatalogScreen

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Obsolete SDK_INT check #1: minSdk is already 29 (Android 10), so O (26) is always true
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                "orders",
                "Order Updates",
                NotificationManager.IMPORTANCE_DEFAULT
            )
            getSystemService(NotificationManager::class.java)?.createNotificationChannel(channel)
        }

        // Obsolete SDK_INT check #2: minSdk is already 29 (Q), so else branch is dead code
        val storageMode = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            "scoped-storage"
        } else {
            "legacy-external-storage"
        }

        setContent {
            CatalogScreen(storageMode = storageMode)
        }
    }

    // Deprecated in favor of OnBackInvokedCallback / PredictiveBackHandler
    @Deprecated("Deprecated in Java")
    override fun onBackPressed() {
        super.onBackPressed()
    }

    // DEAD CODE: Unreferenced legacy migration helper from 2021
    private fun legacySqliteMigration2021(): Boolean {
        return false
    }
}
