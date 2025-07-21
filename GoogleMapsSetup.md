# Google Maps Setup Guide for VISTA iOS App

This guide will help you set up Google Maps integration in your iOS app.

## Prerequisites

1. A Google Cloud Platform account
2. Xcode 12.0 or later
3. iOS 12.0 or later target

## Step 1: Get Google Maps API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Maps SDK for iOS** API:
   - Go to APIs & Services > Library
   - Search for "Maps SDK for iOS"
   - Click on it and press "Enable"
4. Create credentials:
   - Go to APIs & Services > Credentials
   - Click "Create Credentials" > "API Key"
   - Copy your API key
5. (Optional but recommended) Restrict your API key:
   - Click on the API key you just created
   - Under "Application restrictions", select "iOS apps"
   - Add your app's bundle identifier

## Step 2: Install Google Maps SDK

### Using CocoaPods (Recommended)

1. Create a `Podfile` in your project root if you don't have one:
```ruby
platform :ios, '12.0'
use_frameworks!

target 'VISTA' do
  pod 'GoogleMaps'
end
```

2. Run the following commands:
```bash
pod install
```

3. Open the `.xcworkspace` file instead of `.xcodeproj` from now on.

### Using Swift Package Manager

1. In Xcode, go to File > Add Package Dependencies
2. Enter the URL: `https://github.com/googlemaps/ios-maps-sdk`
3. Select the latest version and add to your target

## Step 3: Configure API Key

### Method 1: Info.plist (Recommended)

1. Open your `Info.plist` file
2. Add a new key-value pair:
   - Key: `GOOGLE_MAPS_API_KEY`
   - Type: String
   - Value: Your API key from Step 1

### Method 2: Direct Configuration

If you prefer not to store the API key in Info.plist, you can modify the `configureGoogleMaps()` function in `VISTAApp.swift`:

```swift
private func configureGoogleMaps() {
    // Replace with your actual API key
    GMSServices.provideAPIKey("YOUR_API_KEY_HERE")
}
```

## Step 4: Add Required Permissions

Add the following to your `Info.plist` if you want to show user location:

```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>This app needs location access to show your position on the map.</string>
```

## Step 5: Using the Map View

### Basic Usage

To use the Google Maps view in your app, simply import and use `MapViewController`:

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        MapViewController()
    }
}
```

### Custom Usage

You can also use the `GoogleMapsView` directly with custom parameters:

```swift
GoogleMapsView(
    zoomLevel: 16.0,
    showUserLocation: true,
    markers: [
        MapMarker(latitude: 39.9522, longitude: -75.1932, title: "UPenn", snippet: "University of Pennsylvania")
    ]
)
```

## Step 6: Build and Run

1. Make sure you've opened the `.xcworkspace` file (if using CocoaPods)
2. Build and run your project
3. The map should display centered at University of Pennsylvania

## Troubleshooting

### Common Issues

1. **"Google Maps API key not found"**
   - Make sure you've added the API key to Info.plist with the correct key name
   - Verify the API key is valid and the Maps SDK for iOS is enabled

2. **Map not loading**
   - Check your internet connection
   - Verify the API key has the correct bundle identifier restriction
   - Check the console for any error messages

3. **Location not showing**
   - Make sure you've added location permissions to Info.plist
   - Test on a physical device (location doesn't work well in simulator)

### Console Errors

If you see "Google Maps API key not found" in the console:
1. Double-check the key name in Info.plist is exactly `GOOGLE_MAPS_API_KEY`
2. Make sure the value is a String type, not other types

## Features Included

The `GoogleMapsView` includes:
- ✅ Map centered at UPenn coordinates (39.9522°N, 75.1932°W)
- ✅ Default UPenn campus marker
- ✅ Customizable zoom level
- ✅ User location display (with permission)
- ✅ Interactive controls (zoom, rotate, etc.)
- ✅ Custom markers for UPenn buildings
- ✅ Zoom level slider
- ✅ Toggle for user location

## Next Steps

- Integrate with the existing `route_planner.py` for route planning
- Add real-time navigation features
- Customize map styles and themes
- Add more UPenn building markers
- Implement search functionality 