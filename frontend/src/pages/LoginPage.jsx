import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    const result = await login(email, password)

    if (result.success) {
      navigate('/dashboard')
    } else {
      setError(result.error)
    }

    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-vader-black via-vader-gray to-vader-black flex items-center justify-center px-4">
      <div className="card-vader max-w-md w-full">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold mb-4 vader-glow">VADER AI</h1>
          <h2 className="text-2xl font-semibold mb-2">Welcome Back</h2>
          <p className="text-gray-400">The Dark Side awaits your return</p>
        </div>

        {error && (
          <div className="bg-red-900 border border-red-700 text-red-200 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold mb-2" htmlFor="email">
              Email
            </label>
            <input
              type="email"
              id="email"
              className="input-vader w-full"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="sith.lord@empire.com"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2" htmlFor="password">
              Password
            </label>
            <input
              type="password"
              id="password"
              className="input-vader w-full"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            className="btn-vader w-full"
            disabled={loading}
          >
            {loading ? 'Entering the Dark Side...' : 'Enter the Dark Side'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-400">
            Not yet part of the Empire?{' '}
            <Link to="/register" className="text-vader-red hover:underline font-semibold">
              Join Now
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
