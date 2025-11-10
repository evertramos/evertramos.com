// Form data persistence utility for language switching
export interface FormData {
  name: string
  email: string
  phone: string
  amount: string
  currency: string
  paymentType: string
}

interface StoredFormData {
  data: FormData
  timestamp: number
  expiresAt: number
}

const STORAGE_KEY = 'ezyba_form_data'
const EXPIRY_TIME = 10 * 60 * 1000 // 10 minutes in milliseconds

export const saveFormData = (data: FormData): void => {
  try {
    const now = Date.now()
    const storedData: StoredFormData = {
      data,
      timestamp: now,
      expiresAt: now + EXPIRY_TIME
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(storedData))
  } catch (error) {
    console.warn('Failed to save form data:', error)
  }
}

export const loadFormData = (): FormData | null => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return null
    
    const storedData: StoredFormData = JSON.parse(stored)
    const now = Date.now()
    
    // Check if data has expired
    if (now > storedData.expiresAt) {
      localStorage.removeItem(STORAGE_KEY)
      return null
    }
    
    return storedData.data
  } catch (error) {
    console.warn('Failed to load form data:', error)
    // Clear corrupted data
    localStorage.removeItem(STORAGE_KEY)
    return null
  }
}

export const clearFormData = (): void => {
  try {
    localStorage.removeItem(STORAGE_KEY)
  } catch (error) {
    console.warn('Failed to clear form data:', error)
  }
}

// Auto-cleanup expired data on page load
export const cleanupExpiredData = (): void => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return
    
    const storedData: StoredFormData = JSON.parse(stored)
    const now = Date.now()
    
    if (now > storedData.expiresAt) {
      localStorage.removeItem(STORAGE_KEY)
    }
  } catch (error) {
    // Clear corrupted data
    localStorage.removeItem(STORAGE_KEY)
  }
}