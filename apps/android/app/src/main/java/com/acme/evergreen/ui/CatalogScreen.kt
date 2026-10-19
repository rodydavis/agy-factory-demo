package com.acme.evergreen.ui

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.google.accompanist.swiperefresh.SwipeRefresh
import com.google.accompanist.swiperefresh.rememberSwipeRefreshState
import kotlin.math.roundToInt

// NON-DRY VIOLATION: Duplicated price + tax formatter
fun formatPriceWithTax(amountCents: Int, taxRate: Double = 0.0825): String {
    val subtotal = amountCents / 100.0
    val total = ((subtotal * (1.0 + taxRate)) * 100.0).roundToInt() / 100.0
    return "$%.2f".format(total)
}

@Composable
fun CatalogScreen(
    storageMode: String,
    show2023Promo: Boolean = false,
    isRefreshing: Boolean = false,
    onRefresh: () -> Unit = {}
) {
    // Deprecated Accompanist SwipeRefresh (superseded by Material 3 PullToRefreshBox)
    val swipeRefreshState = rememberSwipeRefreshState(isRefreshing = isRefreshing)

    Scaffold { _ ->
        // BUG WHEN UPGRADING TO API 35: Ignoring Scaffold innerPadding causes overlap under edge-to-edge
        SwipeRefresh(
            state = swipeRefreshState,
            onRefresh = onRefresh
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(16.dp)
            ) {
                if (show2023Promo) {
                    Holiday2023Banner()
                }
                Text(text = "Evergreen Catalog ($storageMode)")
                Text(text = "Featured Item: ${formatPriceWithTax(1999)}")
                Button(onClick = onRefresh) {
                    Text(text = "Checkout Now")
                }
            }
        }
    }
}

// DEAD CODE COMPOSABLE: Unreferenced anywhere in the app
@Composable
fun LegacyXmlReceiptBridge(receiptXml: String) {
    Text(text = receiptXml)
}
