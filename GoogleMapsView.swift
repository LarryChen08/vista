import SwiftUI
import GoogleMaps

struct GoogleMapsView: UIViewRepresentable {
    
    // UPenn coordinates
    private let upennLatitude: Double = 39.9522
    private let upennLongitude: Double = -75.1932
    private let defaultZoom: Float = 15.0
    
    // Optional properties for customization
    var zoomLevel: Float
    var showUserLocation: Bool
    var markers: [MapMarker]
    
    init(zoomLevel: Float = 15.0, showUserLocation: Bool = true, markers: [MapMarker] = []) {
        self.zoomLevel = zoomLevel
        self.showUserLocation = showUserLocation
        self.markers = markers
    }
    
    func makeUIView(context: Context) -> GMSMapView {
        // Create camera position centered at UPenn
        let camera = GMSCameraPosition.camera(
            withLatitude: upennLatitude,
            longitude: upennLongitude,
            zoom: zoomLevel
        )
        
        // Create map view
        let mapView = GMSMapView.map(withFrame: CGRect.zero, camera: camera)
        
        // Configure map settings
        mapView.isMyLocationEnabled = showUserLocation
        mapView.settings.myLocationButton = showUserLocation
        mapView.settings.compassButton = true
        mapView.settings.zoomGestures = true
        mapView.settings.scrollGestures = true
        mapView.settings.rotateGestures = true
        mapView.settings.tiltGestures = true
        
        // Add UPenn marker by default
        let upennMarker = GMSMarker()
        upennMarker.position = CLLocationCoordinate2D(latitude: upennLatitude, longitude: upennLongitude)
        upennMarker.title = "University of Pennsylvania"
        upennMarker.snippet = "Campus Center"
        upennMarker.map = mapView
        
        // Add custom markers if provided
        for marker in markers {
            let gmsMarker = GMSMarker()
            gmsMarker.position = CLLocationCoordinate2D(latitude: marker.latitude, longitude: marker.longitude)
            gmsMarker.title = marker.title
            gmsMarker.snippet = marker.snippet
            gmsMarker.map = mapView
        }
        
        return mapView
    }
    
    func updateUIView(_ uiView: GMSMapView, context: Context) {
        // Update the map if needed
        let camera = GMSCameraPosition.camera(
            withLatitude: upennLatitude,
            longitude: upennLongitude,
            zoom: zoomLevel
        )
        uiView.camera = camera
    }
}

// Data structure for custom markers
struct MapMarker {
    let latitude: Double
    let longitude: Double
    let title: String
    let snippet: String?
    
    init(latitude: Double, longitude: Double, title: String, snippet: String? = nil) {
        self.latitude = latitude
        self.longitude = longitude
        self.title = title
        self.snippet = snippet
    }
}

// Main view that can be used in the app
struct MapViewController: View {
    @State private var zoomLevel: Float = 15.0
    @State private var showUserLocation: Bool = true
    
    // Sample UPenn building markers
    private let upennBuildings: [MapMarker] = [
        MapMarker(latitude: 39.9537, longitude: -75.1932, title: "Van Pelt Library", snippet: "Main Library"),
        MapMarker(latitude: 39.9515, longitude: -75.1925, title: "Houston Hall", snippet: "Student Union"),
        MapMarker(latitude: 39.9529, longitude: -75.1921, title: "College Hall", snippet: "Historic Building"),
        MapMarker(latitude: 39.9512, longitude: -75.1937, title: "Franklin Field", snippet: "Stadium"),
        MapMarker(latitude: 39.9542, longitude: -75.1901, title: "Engineering Building", snippet: "School of Engineering")
    ]
    
    var body: some View {
        NavigationView {
            VStack {
                // Map view
                GoogleMapsView(
                    zoomLevel: zoomLevel,
                    showUserLocation: showUserLocation,
                    markers: upennBuildings
                )
                .ignoresSafeArea(.all, edges: .top)
                
                // Control panel
                VStack(spacing: 10) {
                    HStack {
                        Text("Zoom Level:")
                        Slider(value: $zoomLevel, in: 10...20, step: 1)
                        Text("\(Int(zoomLevel))")
                    }
                    .padding(.horizontal)
                    
                    Toggle("Show User Location", isOn: $showUserLocation)
                        .padding(.horizontal)
                }
                .padding(.vertical, 10)
                .background(Color(.systemBackground))
                .cornerRadius(10)
                .shadow(radius: 5)
                .padding()
            }
            .navigationTitle("UPenn Campus Map")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

// Preview for SwiftUI canvas
struct GoogleMapsView_Previews: PreviewProvider {
    static var previews: some View {
        MapViewController()
    }
}

// Extension to help with Google Maps API key configuration
extension GoogleMapsView {
    static func configureGoogleMaps() {
        // This should be called in your App delegate or main app file
        // Make sure to set your Google Maps API key
        guard let path = Bundle.main.path(forResource: "GoogleService-Info", ofType: "plist"),
              let plist = NSDictionary(contentsOfFile: path),
              let apiKey = plist["API_KEY"] as? String else {
            fatalError("Google Maps API key not found. Please add your API key to GoogleService-Info.plist")
        }
        GMSServices.provideAPIKey(apiKey)
    }
    
    // Alternative method if you want to set the API key directly
    static func configureGoogleMaps(with apiKey: String) {
        GMSServices.provideAPIKey(apiKey)
    }
} 