import Foundation
import Combine

// Legacy ObservableObject boilerplate (superseded by Swift @Observable macro on iOS 17+)
final class OrderViewModel: ObservableObject {
    @Published var isLoading: Bool = false
    @Published var items: [String] = ["Organic Matcha", "Cast Iron Teapot"]

    // NON-DRY VIOLATION: Duplicated currency + tax calculation
    func formatCurrencyWithTax(cents: Int, taxRate: Double = 0.0825) -> String {
        let subtotal = Double(cents) / 100.0
        let total = (subtotal * (1.0 + taxRate) * 100.0).rounded() / 100.0
        return String(format: "$%.2f", total)
    }

    func refreshOrders() {
        if #available(iOS 15.0, *) {
            isLoading = true
            isLoading = false
        }
    }
}
