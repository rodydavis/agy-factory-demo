import Foundation
import StoreKit

@available(iOS, deprecated: 16.0, message: "Superseded by StoreKit 2 Transaction APIs")
final class LegacyStoreKit1Bridge: NSObject, SKPaymentTransactionObserver {
    static let shared = LegacyStoreKit1Bridge()

    func startObservingQueue() {
        SKPaymentQueue.default().add(self)
    }

    func stopObservingQueue() {
        SKPaymentQueue.default().remove(self)
    }

    func paymentQueue(
        _ queue: SKPaymentQueue,
        updatedTransactions transactions: [SKPaymentTransaction]
    ) {
        for transaction in transactions {
            switch transaction.transactionState {
            case .purchased, .restored:
                SKPaymentQueue.default().finishTransaction(transaction)
            case .failed:
                SKPaymentQueue.default().finishTransaction(transaction)
            default:
                break
            }
        }
    }
}
