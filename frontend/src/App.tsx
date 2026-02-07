import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-3xl font-bold mb-4 text-gray-800">
          Trivia App
        </h1>
        <p className="text-gray-600 mb-4">
          Multi-tenant trivia application for corporate training and team engagement
        </p>
        <div className="flex items-center gap-4">
          <button
            onClick={() => setCount((count) => count + 1)}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            data-testid="counter-button"
          >
            Count is {count}
          </button>
        </div>
        <p className="text-sm text-gray-500 mt-4">
          Frontend infrastructure ready. Components coming soon!
        </p>
      </div>
    </div>
  )
}

export default App
