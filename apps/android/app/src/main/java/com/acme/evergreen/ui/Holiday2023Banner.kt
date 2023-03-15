package com.acme.evergreen.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

@Composable
fun Holiday2023Banner(
    promoCode: String = "WINTER2023",
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .background(Color(0xFFB71C1C))
            .padding(12.dp)
    ) {
        Text(
            text = "2023 Holiday Doorbuster! Use code $promoCode at checkout.",
            color = Color.White
        )
    }
}
