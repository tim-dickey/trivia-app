import { describe, it, expect } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders the app title', () => {
    render(<App />)
    expect(screen.getByText('Trivia App')).toBeInTheDocument()
  })

  it('renders the counter button', () => {
    render(<App />)
    const button = screen.getByTestId('counter-button')
    expect(button).toBeInTheDocument()
    expect(button).toHaveTextContent('Count is 0')
  })

  it('increments counter when button is clicked', () => {
    render(<App />)
    const button = screen.getByTestId('counter-button')
    
    fireEvent.click(button)
    expect(button).toHaveTextContent('Count is 1')
    
    fireEvent.click(button)
    expect(button).toHaveTextContent('Count is 2')
  })
})
