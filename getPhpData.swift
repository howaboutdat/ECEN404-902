//
//  getPhpData.swift
//  GROS
//
//  Created by Amin Reza on 11/17/21.
//

import SwiftUI
import CoreLocation

struct getPhpData: View {
    @State var models: [SensorReading] = []
    
    @State var latitudeFrom: String = ""
    @State var longitudeFrom: String = ""
    @State var latitudeTo: String = ""
    @State var longitudeTo: String = ""
    
    @State var started = false
    
    @State var showNavigationSheet = false
    @State var exitNav = false
    
    @State var navDone = false
    
    var locManager = CLLocationManager()
    var body: some View {
        GeometryReader { geo in
            ZStack {
//                if showNavigationSheet {
//                    NavigationVC(latitudeFrom: self.$latitudeFrom, longitudeFrom: self.$longitudeFrom, latitudeTo: self.$latitudeTo, longitudeTo: self.$longitudeTo).onDisappear{withAnimation{self.showNavigationSheet = false}}
//                } else {
                    VStack {
                        Image("TItleImage")
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                            .frame(width: geo.size.width)
                        Spacer()
                    }
                    VStack {
                        Text("Pick ups remaining: \(models.count)").font(.title)
                        Divider()
                        Button("Start Navigation") {
                            self.updateCoordinateValues()
                            DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
                                self.showNavigationSheet = true
                            }
                            
                            withAnimation{self.showNavigationSheet = true}
                        }.buttonStyle(RoundedRectangleButtonStyle()).padding()
                        
                        Button("Update list") {
                            self.reloadDatabase()
                        }.buttonStyle(RoundedRectangleButtonStyle()).padding()
                        
                    }.frame(width: geo.size.width, height: geo.size.height, alignment: .center)
//                }
            }
            
//            List (self.models) { (model) in
//                HStack {
//                    // they are optional
//                    Text("\(model.Longtitude ?? "0.0")").bold()
//                    Text("\(model.Latitude ?? "0.0")").bold()
//                }
//            }
        }
        .onAppear(perform: {
            // send request to server
            locManager.requestWhenInUseAuthorization()
            var currentLocation: CLLocation!
            if
                CLLocationManager.authorizationStatus() == .authorizedWhenInUse ||
                CLLocationManager.authorizationStatus() == .authorizedAlways
            {
                currentLocation = locManager.location
            }
            self.latitudeFrom = String(currentLocation.coordinate.latitude)
            self.longitudeFrom = String(currentLocation.coordinate.longitude)
            
            self.reloadDatabase()
            if models.count != 0 {
                self.updateCoordinateValues()
            }
        })
        .sheet(isPresented: self.$showNavigationSheet, onDismiss: self.exittingNav) {
            ZStack {

                NavigationVC(latitudeFrom: self.$latitudeFrom, longitudeFrom: self.$longitudeFrom, latitudeTo: self.$latitudeTo, longitudeTo: self.$longitudeTo).onDisappear{self.navDone = true}

                if self.navDone {
                    VStack {
                        Text("Pick ups remaining: \(models.count)").font(.title)
                        Divider()
                        Button("Resume") {
                            self.navDone = false
                            self.showNavigationSheet = false
                            DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                                self.showNavigationSheet = true
                            }
                        }.buttonStyle(RoundedRectangleButtonStyle()).padding()
                        Button("Next") {
                            self.deleteEntry()
                            self.models.removeFirst(1)
                            self.updateCoordinateValues()
                            self.navDone = false
                            self.showNavigationSheet = false
                            DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                                self.showNavigationSheet = true
                            }
                        }.buttonStyle(RoundedRectangleButtonStyle()).padding()
                    }
                }
            }
        }
    }
}

extension getPhpData {
    
    func deleteEntry() {
        
        guard let url: URL = URL(string: "https://a400-50-24-41-54.ngrok.io/delete_entry.php/") else {
            print("invalid URL")
            return
        }
        var urlRequest: URLRequest = URLRequest(url: url)
        urlRequest.httpMethod = "GET"
        URLSession.shared.dataTask(with: urlRequest, completionHandler: { (data, response, error) in
            // check if response is okay
             
        }).resume()
        
    }
    
    func reloadDatabase() {
        guard let url: URL = URL(string: "https://a400-50-24-41-54.ngrok.io/swiftui-get-data-from-api.php") else {
            print("invalid URL")
            return
        }
        var urlRequest: URLRequest = URLRequest(url: url)
        urlRequest.httpMethod = "GET"
        URLSession.shared.dataTask(with: urlRequest, completionHandler: { (data, response, error) in
            // check if response is okay
             
            guard let data = data else {
                print("invalid response")
                return
            }
             
            // convert JSON response into class model as an array
            do {
                self.models = try JSONDecoder().decode([SensorReading].self, from: data)
                print("went through")
                print("AYOO WAS GOOD")
                print(models[0].Latitude ?? "37.76556957793795")
                print(models[0].Longtitude ?? "-122.42409811526268")
                
                self.latitudeTo = models[0].Latitude ?? "37.76556957793795"
                self.longitudeTo = models[0].Longtitude ?? "-122.42409811526268"
                
            } catch {
                print("--------------uh oh------------------")
                print(error.localizedDescription)
            }
             
        }).resume()
    }
    
    func exittingNav() {
//        withAnimation{self.showNavigationSheet = false}
    }
    
    func updateCoordinateValues() {
        self.latitudeTo = models[0].Latitude ?? "37.76556957793795"
        self.longitudeTo = models[0].Longtitude ?? "-122.42409811526268"
    }
}


struct getPhpData_Previews: PreviewProvider {
    static var previews: some View {
        getPhpData()
    }
}

class SensorReading: Codable, Identifiable {
    var ID_module: String? = ""
    var Longtitude: String? = ""
    var Latitude: String? = ""
}

struct mainButton: ButtonStyle {
    @Environment(\.isEnabled) private var isEnabled
    

    func makeBody(configuration: Configuration) -> some View {
        configuration
            .label
            .foregroundColor(configuration.isPressed ? .gray : .white)
            .padding(.vertical, 10)
            .padding(.horizontal, 5)
            .background(configuration.isPressed ? .gray : Color.accentColor)
            .cornerRadius(8)
    }
}

    
struct RoundedRectangleButtonStyle: ButtonStyle {
  func makeBody(configuration: Configuration) -> some View {
    HStack {
      Spacer()
      configuration.label.foregroundColor(.white)
      Spacer()
    }
    .padding(.horizontal, 10).padding(.vertical, 5)
    .background(configuration.isPressed ? .gray : Color.accentColor)
    .cornerRadius(8)
    .scaleEffect(configuration.isPressed ? 0.95 : 1)
    .frame(width: 220, height: 10, alignment: .center)
  }
}
