//
//  ContentView.swift
//  auto-ticketing
//
//  Created by Ulises Lugo Fletes on 31/07/25.
//

import SwiftUI
import AudioToolbox

struct ContentView: View {
    @State private var timeRemaining: TimeInterval = 0
    @State private var timer: Timer?
    @State private var isTimerRunning = false
    
    var body: some View {
        VStack {
            Text("Time Remaining: \(timeString(time: timeRemaining))")
                .font(.largeTitle)
                .padding()
            
            DatePicker("Set Timer", selection: Binding(get: {
                Date(timeIntervalSinceReferenceDate: self.timeRemaining)
            }, set: {
                self.timeRemaining = $0.timeIntervalSinceReferenceDate
            }), displayedComponents: .hourAndMinute)
            .labelsHidden()
            .datePickerStyle(WheelDatePickerStyle())
            
            HStack {
                Button(action: {
                    self.startTimer()
                }) {
                    Text("Start")
                        .font(.title)
                        .padding()
                        .background(Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .disabled(isTimerRunning)
                
                Button(action: {
                    self.stopTimer()
                }) {
                    Text("Stop")
                        .font(.title)
                        .padding()
                        .background(Color.red)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .disabled(!isTimerRunning)
            }
            .padding()
        }
    }
    
    private func timeString(time: TimeInterval) -> String {
        let hours = Int(time) / 3600
        let minutes = Int(time) / 60 % 60
        let seconds = Int(time) % 60
        return String(format: "%02i:%02i:%02i", hours, minutes, seconds)
    }
    
    private func startTimer() {
        isTimerRunning = true
        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
            if self.timeRemaining > 0 {
                self.timeRemaining -= 1
            } else {
                self.stopTimer()
                self.playAlarm()
            }
        }
    }
    
    private func stopTimer() {
        isTimerRunning = false
        timer?.invalidate()
        timer = nil
    }

    private func playAlarm() {
        AudioServicesPlaySystemSound(1005)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

