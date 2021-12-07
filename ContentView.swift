//
//  ContentView.swift
//  GROS
//
//  Created by iMac on 9/9/21.
//

import SwiftUI
import CoreData

struct ContentView: View {

    var body: some View {
        getPhpData()
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView().environment(\.managedObjectContext, PersistenceController.preview.container.viewContext)
    }
}
