# Issue #103: Apple App Store iOS 18 SDK Readiness & SwiftUI Modernization

- **Labels**: `ios`, `app-store-policy`, `swiftui`
- **Target**: `apps/ios` (`min_os_version = 17.0`, `app_store_target_sdk = 18.0`)

## Problem
1. `CatalogView.swift` and `OrderViewModel.swift` still contain `#available(iOS 15.0, *)` and `#available(iOS 16.0, *)` branches even though our minimum deployment target is iOS `17.0`.
2. Migrate `OrderViewModel` from `ObservableObject` / `@Published` to the Swift `@Observable` macro and replace deprecated `NavigationView`, `.foregroundColor()`, and `.cornerRadius()`.
3. Ensure `PrivacyInfo.xcprivacy` is compliant with Apple App Store Connect `ITMS-91053` Required Reason API checks before submitting with the iOS 18 SDK.
