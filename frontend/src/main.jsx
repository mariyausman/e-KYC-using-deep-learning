import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import TestConnection from './Components/TestConnection.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
    <TestConnection/>
  </StrictMode>,
)
