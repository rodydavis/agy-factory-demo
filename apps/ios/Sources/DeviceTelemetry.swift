import Foundation

enum DeviceTelemetry {
    static func recordAppLaunch() {
        // Requires NSPrivacyAccessedAPICategoryUserDefaults (CA92.1) in PrivacyInfo.xcprivacy
        UserDefaults.standard.set(Date().timeIntervalSince1970, forKey: "last_launch_ts")
    }

    static func currentSystemUptimeSeconds() -> TimeInterval {
        // Requires NSPrivacyAccessedAPICategorySystemBootTime (35F9.1) in PrivacyInfo.xcprivacy
        return ProcessInfo.processInfo.systemUptime
    }
}
