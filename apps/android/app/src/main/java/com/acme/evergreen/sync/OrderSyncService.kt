package com.acme.evergreen.sync

import android.app.Service
import android.content.Intent
import android.os.Build
import android.os.IBinder

class OrderSyncService : Service() {
    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Obsolete SDK_INT check: minSdk is 29, so P (28) is always true
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            performBackgroundOrderSync()
        }
        return START_NOT_STICKY
    }

    private fun performBackgroundOrderSync() {
        // Syncs offline order queue with backend
    }

    // NOTE: Missing override fun onTimeout(startId: Int, fgsType: Int)
    // Required in Android 15 (targetSdk = 35) for dataSync foreground services!
}
