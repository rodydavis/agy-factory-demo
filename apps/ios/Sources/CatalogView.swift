import SwiftUI

struct CatalogView: View {
    @StateObject private var viewModel = OrderViewModel()

    var body: some View {
        // Obsolete availability check #1: min_os_version is 17.0, so iOS 16 is always available
        if #available(iOS 16.0, *) {
            // Still using deprecated NavigationView inside branch
            NavigationView {
                catalogContent
            }
        } else {
            NavigationView {
                Text("Legacy iOS 15 Catalog")
            }
        }
    }

    private var catalogContent: some View {
        VStack(spacing: 16) {
            // Obsolete availability check #2: iOS 15.0 is always available on iOS 17.0+
            if #available(iOS 15.0, *) {
                Text("Evergreen Storefront")
                    .font(.headline)
                    // Deprecated in iOS 17 in favor of .foregroundStyle()
                    .foregroundColor(.green)
            }

            Text("Total with tax: \(viewModel.formatCurrencyWithTax(cents: 2499))")
                .padding(12)
                // Deprecated in iOS 17 in favor of .clipShape(.rect(cornerRadius: 8))
                .cornerRadius(8)
        }
        .navigationTitle("Catalog")
    }
}

// DEAD CODE VIEW: Unreferenced anywhere in the iOS app
struct LegacyReceiptView: View {
    let rawReceiptText: String

    var body: some View {
        Text(rawReceiptText)
            .foregroundColor(.gray)
    }
}
