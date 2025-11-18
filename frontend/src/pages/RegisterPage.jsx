import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    fullName: '',
    password: '',
    confirmPassword: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      return
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }

    setLoading(true)

    const result = await register(
      formData.email,
      formData.username,
      formData.password,
      formData.fullName
    )

    if (result.success) {
      navigate('/dashboard')
    } else {
      setError(result.error)
    }

    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-vader-black via-vader-gray to-vader-black flex items-center justify-center px-4 py-12">
      <div className="card-vader max-w-md w-full">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold mb-4 vader-glow">VADER AI</h1>
          <h2 className="text-2xl font-semibold mb-2">Join the Empire</h2>
          <p className="text-gray-400">Begin your journey to unlimited power</p>
        </div>

        {error && (
          <div className="bg-red-900 border border-red-700 text-red-200 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-semibold mb-2" htmlFor="fullName">
              Full Name
            </label>
            <input
              type="text"
              id="fullName"
              name="fullName"
              className="input-vader w-full"
              value={formData.fullName}
              onChange={handleChange}
              placeholder="Anakin Skywalker"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2" htmlFor="username">
              Username *
            </label>
            <input
              type="text"
              id="username"
              name="username"
              className="input-vader w-full"
              value={formData.username}
              onChange={handleChange}
              required
              placeholder="darth_vader"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2" htmlFor="email">
              Email *
            </label>
            <input
              type="email"
              id="email"
              name="email"
              className="input-vader w-full"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="sith.lord@empire.com"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2" htmlFor="password">
              Password *
            </label>
            <input
              type="password"
              id="password"
              name="password"
              className="input-vader w-full"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="••••••••"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2" htmlFor="confirmPassword">
              Confirm Password *
            </label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              className="input-vader w-full"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            className="btn-vader w-full"
            disabled={loading}
          >
            {loading ? 'Joining the Empire...' : 'Join the Empire'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-400">
            Already part of the Empire?{' '}
            <Link to="/login" className="text-vader-red hover:underline font-semibold">
              Sign In
            </Link>
          </p>
          <Link to="/" className="text-gray-500 hover:text-gray-300 text-sm mt-2 inline-block">
            ← Back to Home
          </Link>
        </div>
      </div>
    </div>
  )
}
