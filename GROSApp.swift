//
//  GROSApp.swift
//  GROS
//
//  Created by iMac on 9/9/21.
//

import SwiftUI

@main
struct GROSApp: App {
    let persistenceController = PersistenceController.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, persistenceController.container.viewContext)
        }
    }
}
