import React, { useState, useRef, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { FaMicrophone, FaStop, FaCog, FaSignOutAlt, FaVolumeUp, FaSpinner } from 'react-icons/fa'
import axios from 'axios'

export default function Dashboard() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [isRecording, setIsRecording] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [transcription, setTranscription] = useState('')
  const [vaderResponse, setVaderResponse] = useState('')
  const [audioUrl, setAudioUrl] = useState(null)
  const [error, setError] = useState('')
  const [conversations, setConversations] = useState([])
  const [currentConversationId, setCurrentConversationId] = useState(null)

  const mediaRecorderRef = useRef(null)
  const chunksRef = useRef([])
  const audioRef = useRef(null)

  useEffect(() => {
    loadConversations()
  }, [])

  const loadConversations = async () => {
    try {
      const response = await axios.get('/api/voice/conversations')
      setConversations(response.data)
    } catch (error) {
      console.error('Error loading conversations:', error)
    }
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })

      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      chunksRef.current = []

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data)
        }
      }

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/wav' })
        await processAudio(audioBlob)

        // Stop all tracks
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      setIsRecording(true)
      setError('')
      setTranscription('')
      setVaderResponse('')
      setAudioUrl(null)
    } catch (error) {
      console.error('Error starting recording:', error)
      setError('Could not access microphone. Please grant permission.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const processAudio = async (audioBlob) => {
    setIsProcessing(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('audio', audioBlob, 'recording.wav')
      if (currentConversationId) {
        formData.append('conversation_id', currentConversationId)
      }

      const response = await axios.post('/api/voice/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      const data = response.data
      setTranscription(data.transcribed_text)
      setVaderResponse(data.vader_response)
      setAudioUrl(data.audio_url)
      setCurrentConversationId(data.conversation_id)

      // Play audio response
      if (audioRef.current) {
        audioRef.current.src = `/api${data.audio_url}`
        audioRef.current.play()
      }

      // Reload conversations
      loadConversations()
    } catch (error) {
      console.error('Error processing audio:', error)
      setError(error.response?.data?.detail || 'Error processing audio. Please try again.')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-vader-black via-vader-gray to-vader-black">
      {/* Header */}
      <header className="bg-vader-black border-b border-empire-silver">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-3xl font-bold vader-glow">VADER AI</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-400">Welcome, {user?.username}</span>
            <Link to="/settings" className="btn-vader-outline py-2 px-4 flex items-center gap-2">
              <FaCog /> Settings
            </Link>
            <button onClick={handleLogout} className="btn-vader py-2 px-4 flex items-center gap-2">
              <FaSignOutAlt /> Logout
            </button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Interaction Area */}
          <div className="lg:col-span-2">
            <div className="card-vader">
              <h2 className="text-2xl font-bold mb-6 text-center">
                Command the Dark Side
              </h2>

              {/* Voice Control */}
              <div className="flex justify-center mb-8">
                {!isRecording ? (
                  <button
                    onClick={startRecording}
                    className="btn-vader w-48 h-48 rounded-full flex flex-col items-center justify-center transform hover:scale-110 transition-transform"
                    disabled={isProcessing}
                  >
                    <FaMicrophone className="text-6xl mb-2" />
                    <span className="text-sm">Press to Speak</span>
                  </button>
                ) : (
                  <button
                    onClick={stopRecording}
                    className="bg-red-700 hover:bg-red-800 w-48 h-48 rounded-full flex flex-col items-center justify-center animate-pulse"
                  >
                    <FaStop className="text-6xl mb-2" />
                    <span className="text-sm">Recording...</span>
                  </button>
                )}
              </div>

              {isProcessing && (
                <div className="flex items-center justify-center gap-3 mb-6">
                  <FaSpinner className="animate-spin text-vader-red text-2xl" />
                  <span className="text-lg">Processing your command...</span>
                </div>
              )}

              {error && (
                <div className="bg-red-900 border border-red-700 text-red-200 px-4 py-3 rounded-lg mb-6">
                  {error}
                </div>
              )}

              {/* Transcription & Response */}
              {transcription && (
                <div className="space-y-4">
                  <div className="bg-vader-black border border-blue-500 rounded-lg p-4">
                    <div className="flex items-start gap-3">
                      <FaMicrophone className="text-blue-500 text-xl mt-1" />
                      <div>
                        <p className="text-sm text-gray-400 mb-1">You said:</p>
                        <p className="text-white">{transcription}</p>
                      </div>
                    </div>
                  </div>

                  {vaderResponse && (
                    <div className="bg-vader-black border border-vader-red rounded-lg p-4">
                      <div className="flex items-start gap-3">
                        <FaVolumeUp className="text-vader-red text-xl mt-1" />
                        <div className="flex-1">
                          <p className="text-sm text-gray-400 mb-1">Vader responds:</p>
                          <p className="text-white mb-3">{vaderResponse}</p>
                          {audioUrl && (
                            <audio ref={audioRef} controls className="w-full">
                              <source src={`/api${audioUrl}`} type="audio/wav" />
                            </audio>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {!transcription && !isProcessing && (
                <div className="text-center text-gray-400 py-12">
                  <p className="text-lg mb-2">Press the button and speak your command</p>
                  <p className="text-sm">
                    Try: "Vader, what is the weather?" or "Vader, tell me about the Force"
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Sidebar - Conversation History */}
          <div className="lg:col-span-1">
            <div className="card-vader">
              <h3 className="text-xl font-bold mb-4">Conversation History</h3>

              {conversations.length > 0 ? (
                <div className="space-y-3">
                  {conversations.slice(0, 10).map((conv) => (
                    <div
                      key={conv.id}
                      className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                        currentConversationId === conv.id
                          ? 'border-vader-red bg-vader-black'
                          : 'border-empire-silver hover:border-vader-red'
                      }`}
                      onClick={() => setCurrentConversationId(conv.id)}
                    >
                      <p className="font-semibold truncate">{conv.title}</p>
                      <p className="text-sm text-gray-400">
                        {conv.message_count} messages
                      </p>
                      <p className="text-xs text-gray-500">
                        {new Date(conv.updated_at).toLocaleDateString()}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-400 text-center py-8">
                  No conversations yet. Start speaking to begin.
                </p>
              )}

              <button
                onClick={() => setCurrentConversationId(null)}
                className="btn-vader-outline w-full mt-4 py-2"
              >
                New Conversation
              </button>
            </div>

            {/* Quick Tips */}
            <div className="card-vader mt-6">
              <h3 className="text-lg font-bold mb-3">Quick Tips</h3>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>• Speak clearly for best results</li>
                <li>• Address Vader directly in commands</li>
                <li>• Check settings for voice customization</li>
                <li>• Connect ESP32 for hardware control</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
