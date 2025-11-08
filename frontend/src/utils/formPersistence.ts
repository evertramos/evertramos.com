// Form data persistence utility for language switching
export interface FormData {
  name: string
  email: string
  phone: string
  amount: string
  currency: string
  paymentType: string
}

const STORAGE_KEY = 'ezyba_form_data'

export const saveFormData = (data: FormData): void => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  } catch (error) {
    console.warn('Failed to save form data:', error)
  }
}

export const loadFormData = (): FormData | null => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    return stored ? JSON.parse(stored) : null
  } catch (error) {
    console.warn('Failed to load form data:', error)
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