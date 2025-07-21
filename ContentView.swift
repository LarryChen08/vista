//
//  ContentView.swift
//  VISTA
//
//  Created by Tony Yang on 7/20/25.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        TabView {
            CameraView()
                .tabItem {
                    Image(systemName: "camera")
                    Text("Camera")
                }
            
            MapViewController()
                .tabItem {
                    Image(systemName: "map")
                    Text("Map")
                }
        }
    }
}

struct CameraView: View {
    @State private var showImagePicker = false
    @State private var selectedImage: UIImage?
    @State private var descriptionText: String?
    @State private var isLoading = false

    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                if let image = selectedImage {
                    Image(uiImage: image)
                        .resizable()
                        .scaledToFit()
                        .frame(height: 300)
                }

                if isLoading {
                    ProgressView("Analyzing Image...")
                } else if let description = descriptionText {
                    Text(description)
                        .font(.headline)
                        .padding()
                        .background(Color(.systemGray6))
                        .cornerRadius(12)
                }

                Button("Take Photo") {
                    showImagePicker = true
                }
                .padding()
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(10)
            }
            .padding()
            .navigationTitle("UPenn Visual Guide")
        }
        .sheet(isPresented: $showImagePicker, onDismiss: processImage) {
            ImagePicker(selectedImage: $selectedImage)
        }
    }

    func processImage() {
        guard let image = selectedImage else { return }
        isLoading = true
        descriptionText = nil
        
        let apiService = APIService()
        apiService.fetchDescription(image: image, locationText: "University of Pennsylvania, Philadelphia") { result in
            DispatchQueue.main.async {
                switch result {
                case .success(let description):
                    descriptionText = description
                case .failure(let error):
                    descriptionText = "Error: \(error.localizedDescription)"
                }
                isLoading = false
            }
        }
    }
}

#Preview {
    ContentView()
}

