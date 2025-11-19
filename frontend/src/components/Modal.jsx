import React from 'react'
import { FaTimes } from 'react-icons/fa'

export default function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black bg-opacity-75"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative bg-vader-gray border border-empire-silver rounded-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-empire-silver">
          <h2 className="text-2xl font-bold">{title}</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-vader-red transition-colors"
          >
            <FaTimes size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">{children}</div>
      </div>
    </div>
  )
}
