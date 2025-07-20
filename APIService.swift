//
//  APIService.swift
//  VISTA
//
//  Created by Tony Yang on 7/20/25.
//

import Foundation
import UIKit

class APIService {
    private let apiKey = 
    private let apiEndpoint = "https://api.openai.com/v1/chat/completions"

    func fetchDescription(image: UIImage, locationText: String, completion: @escaping (Result<String, Error>) -> Void) {
        print("📤 Starting OpenAI API call...")

        guard let imageData = image.jpegData(compressionQuality: 0.7) else {
            print("❌ Couldn't convert image to JPEG")
            completion(.failure(NSError(domain: "InvalidImage", code: -1, userInfo: nil)))
            return
        }

        let base64String = imageData.base64EncodedString()

        let payload: [String: Any] = [
            "model": "gpt-4o",
            "messages": [
                [
                    "role": "user",
                    "content": [
                        [
                            "type": "text",
                            "text": "Describe this image and its surrounding location: \(locationText)"
                        ],
                        [
                            "type": "image_url",
                            "image_url": [
                                "url": "data:image/jpeg;base64,\(base64String)"
                            ]
                        ]
                    ]
                ]
            ],
            "temperature": 1.0
        ]

        guard let url = URL(string: apiEndpoint) else {
            print("❌ Invalid URL")
            completion(.failure(NSError(domain: "InvalidURL", code: -1, userInfo: nil)))
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: payload, options: [])
        } catch {
            print("❌ Couldn't serialize payload: \(error)")
            completion(.failure(error))
            return
        }

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("❌ Network error: \(error.localizedDescription)")
                completion(.failure(error))
                return
            }

            guard let data = data else {
                print("❌ No data received")
                completion(.failure(NSError(domain: "NoData", code: -1, userInfo: nil)))
                return
            }

            print("✅ Response received")

            do {
                if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any],
                   let choices = json["choices"] as? [[String: Any]],
                   let message = choices.first?["message"] as? [String: Any],
                   let description = message["content"] as? String {
                    print("📦 Description parsed: \(description)")
                    completion(.success(description))
                } else {
                    let raw = String(data: data, encoding: .utf8) ?? "Unknown response"
                    print("❌ Failed to parse JSON. Raw response: \(raw)")
                    completion(.failure(NSError(domain: "ParseError", code: -2, userInfo: [NSLocalizedDescriptionKey: raw])))
                }
            } catch {
                print("❌ JSON parsing error: \(error.localizedDescription)")
                completion(.failure(error))
            }
        }.resume()
    }
}
