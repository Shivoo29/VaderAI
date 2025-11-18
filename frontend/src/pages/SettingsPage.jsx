import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { FaArrowLeft, FaSave } from 'react-icons/fa'
import axios from 'axios'

export default function SettingsPage() {
  const { user, refreshUser } = useAuth()
  const navigate = useNavigate()
  const [settings, setSettings] = useState({
    full_name: '',
    vader_breathing_enabled: true,
    vader_voice_pitch: -50,
    vader_voice_speed: 90
  })
  const [saving, setSaving] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (user) {
      setSettings({
        full_name: user.full_name || '',
        vader_breathing_enabled: user.vader_breathing_enabled,
        vader_voice_pitch: user.vader_voice_pitch,
        vader_voice_speed: user.vader_voice_speed
      })
    }
  }, [user])

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setSettings({
      ...settings,
      [name]: type === 'checkbox' ? checked : type === 'range' ? parseInt(value) : value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError('')
    setSuccess(false)

    try {
      await axios.put('/api/auth/me', settings)
      await refreshUser()
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (error) {
      console.error('Error saving settings:', error)
      setError(error.response?.data?.detail || 'Error saving settings')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-vader-black via-vader-gray to-vader-black">
      {/* Header */}
      <header className="bg-vader-black border-b border-empire-silver">
        <div className="container mx-auto px-4 py-4">
          <Link to="/dashboard" className="text-vader-red hover:text-red-400 flex items-center gap-2">
            <FaArrowLeft /> Back to Dashboard
          </Link>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8 max-w-3xl">
        <div className="card-vader">
          <h1 className="text-3xl font-bold mb-6 vader-glow">Settings</h1>

          {success && (
            <div className="bg-green-900 border border-green-700 text-green-200 px-4 py-3 rounded-lg mb-6">
              Settings saved successfully!
            </div>
          )}

          {error && (
            <div className="bg-red-900 border border-red-700 text-red-200 px-4 py-3 rounded-lg mb-6">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Profile Settings */}
            <section>
              <h2 className="text-2xl font-semibold mb-4 text-vader-red">Profile</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold mb-2">Username</label>
                  <input
                    type="text"
                    value={user?.username || ''}
                    className="input-vader w-full bg-vader-black cursor-not-allowed"
                    disabled
                  />
                  <p className="text-xs text-gray-500 mt-1">Username cannot be changed</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">Email</label>
                  <input
                    type="email"
                    value={user?.email || ''}
                    className="input-vader w-full bg-vader-black cursor-not-allowed"
                    disabled
                  />
                  <p className="text-xs text-gray-500 mt-1">Email cannot be changed</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2" htmlFor="full_name">
                    Full Name
                  </label>
                  <input
                    type="text"
                    id="full_name"
                    name="full_name"
                    className="input-vader w-full"
                    value={settings.full_name}
                    onChange={handleChange}
                    placeholder="Enter your full name"
                  />
                </div>
              </div>
            </section>

            {/* Voice Settings */}
            <section>
              <h2 className="text-2xl font-semibold mb-4 text-vader-red">Vader Voice Settings</h2>

              <div className="space-y-6">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <label className="text-sm font-semibold">Breathing Sound Effects</label>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        name="vader_breathing_enabled"
                        checked={settings.vader_breathing_enabled}
                        onChange={handleChange}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-vader-red"></div>
                    </label>
                  </div>
                  <p className="text-sm text-gray-400">
                    Enable Darth Vader's iconic breathing sound before responses
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-3">
                    Voice Pitch: {settings.vader_voice_pitch}
                  </label>
                  <input
                    type="range"
                    name="vader_voice_pitch"
                    min="-100"
                    max="0"
                    value={settings.vader_voice_pitch}
                    onChange={handleChange}
                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-vader-red"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Deeper</span>
                    <span>Normal</span>
                  </div>
                  <p className="text-sm text-gray-400 mt-2">
                    Adjust the depth of Vader's voice (-100 = very deep, 0 = normal)
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-3">
                    Voice Speed: {settings.vader_voice_speed}%
                  </label>
                  <input
                    type="range"
                    name="vader_voice_speed"
                    min="50"
                    max="150"
                    value={settings.vader_voice_speed}
                    onChange={handleChange}
                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-vader-red"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Slower</span>
                    <span>Normal</span>
                    <span>Faster</span>
                  </div>
                  <p className="text-sm text-gray-400 mt-2">
                    Control the speaking speed of Vader's voice (90% recommended for dramatic effect)
                  </p>
                </div>
              </div>
            </section>

            {/* ESP32 Device Info */}
            <section>
              <h2 className="text-2xl font-semibold mb-4 text-vader-red">ESP32 Devices</h2>
              <div className="bg-vader-black border border-empire-silver rounded-lg p-4">
                <p className="text-gray-400 mb-2">
                  Connect your ESP32 device to use Vader AI with hardware control.
                </p>
                <p className="text-sm text-gray-500">
                  Device management coming soon. For now, use the WebSocket API directly.
                </p>
              </div>
            </section>

            {/* Save Button */}
            <div className="flex justify-end gap-4">
              <Link to="/dashboard" className="btn-vader-outline py-3 px-8">
                Cancel
              </Link>
              <button
                type="submit"
                className="btn-vader flex items-center gap-2"
                disabled={saving}
              >
                <FaSave />
                {saving ? 'Saving...' : 'Save Settings'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
