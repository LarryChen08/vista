//
//  VISTAApp.swift
//  VISTA
//
//  Created by Tony Yang on 7/20/25.
//

import SwiftUI
import GoogleMaps

@main
struct VISTAApp: App {
    
    init() {
        // Initialize Google Maps SDK
        configureGoogleMaps()
    }
    
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
    
    private func configureGoogleMaps() {
        // Get API key from environment or Info.plist
        if let apiKey = Bundle.main.object(forInfoDictionaryKey: "GOOGLE_MAPS_API_KEY") as? String {
            GMSServices.provideAPIKey(apiKey)
        } else {
            // Fallback: try to get from environment variable during development
            print("⚠️ Google Maps API key not found in Info.plist")
            print("Please add GOOGLE_MAPS_API_KEY to your Info.plist file")
            print("You can get an API key from: https://developers.google.com/maps/documentation/ios-sdk/get-api-key")
        }
    }
}
