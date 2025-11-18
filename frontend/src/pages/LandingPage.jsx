import React from 'react'
import { Link } from 'react-router-dom'
import { FaMicrophone, FaRobot, FaVolumeUp, FaShieldAlt } from 'react-icons/fa'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-vader-black via-vader-gray to-vader-black">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-20">
        <header className="text-center mb-20">
          <h1 className="text-6xl md:text-8xl font-bold mb-6 vader-glow breathing-animation">
            VADER AI
          </h1>
          <p className="text-2xl md:text-3xl text-empire-silver mb-8">
            "You don't know the power of the Dark Side..."
          </p>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto mb-12">
            Experience the commanding presence of Darth Vader in your voice assistant.
            Speak your commands, and the Dark Lord shall respond with the wisdom and authority
            befitting a Sith Lord.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register" className="btn-vader">
              Join the Empire
            </Link>
            <Link to="/login" className="btn-vader-outline">
              Already Enlisted
            </Link>
          </div>
        </header>

        {/* Features Section */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-20">
          <FeatureCard
            icon={<FaMicrophone className="text-5xl text-vader-red" />}
            title="Voice Recognition"
            description="Advanced speech recognition powered by Whisper AI. Vader understands your commands with precision."
          />
          <FeatureCard
            icon={<FaRobot className="text-5xl text-vader-red" />}
            title="AI Intelligence"
            description="Context-aware responses using cutting-edge AI. The Force guides every interaction."
          />
          <FeatureCard
            icon={<FaVolumeUp className="text-5xl text-vader-red" />}
            title="Vader's Voice"
            description="Authentic Darth Vader voice synthesis. Deep, commanding, and unmistakably Sith."
          />
          <FeatureCard
            icon={<FaShieldAlt className="text-5xl text-vader-red" />}
            title="Secure & Private"
            description="Your conversations are protected by the Empire's finest encryption protocols."
          />
        </div>

        {/* How It Works */}
        <section className="card-vader max-w-4xl mx-auto mb-20">
          <h2 className="text-4xl font-bold text-center mb-12 vader-glow">
            How It Works
          </h2>

          <div className="space-y-6">
            <Step
              number="1"
              title="Speak Your Command"
              description="Use your microphone or ESP32 device to issue voice commands to Vader AI."
            />
            <Step
              number="2"
              title="AI Processing"
              description="Your speech is transcribed, processed through our AI, and Vader formulates a response."
            />
            <Step
              number="3"
              title="Vader Responds"
              description="Hear the response in Vader's iconic voice, complete with breathing effects."
            />
            <Step
              number="4"
              title="Execute Actions"
              description="Control smart devices, get information, or simply experience the power of the Dark Side."
            />
          </div>
        </section>

        {/* Use Cases */}
        <section className="text-center mb-20">
          <h2 className="text-4xl font-bold mb-12 vader-glow">
            Command the Dark Side
          </h2>

          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            <UseCase
              title="Smart Home Control"
              description="'Vader, turn on the lights.' - Watch as the Empire illuminates your domain."
            />
            <UseCase
              title="Information Queries"
              description="'Vader, what's the weather?' - The Force reveals all atmospheric conditions."
            />
            <UseCase
              title="Entertainment"
              description="'Vader, play Imperial March.' - Immerse yourself in the sounds of the Empire."
            />
          </div>
        </section>

        {/* CTA Section */}
        <section className="card-vader max-w-3xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-6 vader-glow">
            Unleash Your Inner Sith
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Join thousands who have embraced the power of the Dark Side.
            Your journey to unlimited power begins now.
          </p>
          <Link to="/register" className="btn-vader text-xl">
            Begin Your Training
          </Link>
        </section>
      </div>

      {/* Footer */}
      <footer className="bg-vader-black border-t border-empire-silver py-8">
        <div className="container mx-auto px-4 text-center text-gray-400">
          <p className="mb-2">
            "The Force will be with you... always."
          </p>
          <p className="text-sm">
            © 2024 Vader AI. All rights reserved. May the Force be with you.
          </p>
        </div>
      </footer>
    </div>
  )
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="card-vader text-center hover:border-vader-red transition-colors">
      <div className="flex justify-center mb-4">{icon}</div>
      <h3 className="text-xl font-bold mb-3">{title}</h3>
      <p className="text-gray-400">{description}</p>
    </div>
  )
}

function Step({ number, title, description }) {
  return (
    <div className="flex items-start gap-4">
      <div className="bg-vader-red rounded-full w-12 h-12 flex items-center justify-center font-bold text-xl flex-shrink-0">
        {number}
      </div>
      <div>
        <h3 className="text-xl font-bold mb-2">{title}</h3>
        <p className="text-gray-400">{description}</p>
      </div>
    </div>
  )
}

function UseCase({ title, description }) {
  return (
    <div className="card-vader hover:border-vader-red transition-colors">
      <h3 className="text-xl font-bold mb-3">{title}</h3>
      <p className="text-gray-400 italic">"{description}"</p>
    </div>
  )
}
