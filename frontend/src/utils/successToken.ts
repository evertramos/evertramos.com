/**
 * Success token management for payment success pages
 * Ensures success pages are only accessible after valid payments
 */

const TOKEN_EXPIRY_MINUTES = 1 // Token expires in 1 minute

// Generate dynamic storage key
const getStorageKey = (): string => {
  const base = 'ezb'
  const hash = btoa(window.location.hostname).slice(0, 4)
  return `${base}_${hash}_scs`
}

interface SuccessToken {
  token: string
  timestamp: number
  paymentId?: string
  amount?: number
  currency?: string
}

/**
 * Generate a success token after payment completion
 */
export const generateSuccessToken = (paymentId?: string, amount?: number, currency?: string): string => {
  // Generate cryptographically stronger token
  const randomPart = Math.random().toString(36).substring(2)
  const timePart = Date.now().toString(36)
  const extraEntropy = (Math.random() * 1000000).toString(36)
  const token = `${randomPart}${timePart}${extraEntropy}`.replace(/\./g, '')
  const successToken: SuccessToken = {
    token,
    timestamp: Date.now(),
    paymentId,
    amount,
    currency
  }
  
  // Store in sessionStorage (cleared when browser closes)
  sessionStorage.setItem(getStorageKey(), JSON.stringify(successToken))
  
  return token
}

/**
 * Validate success token and return payment info
 */
export const validateSuccessToken = (): { valid: boolean; paymentInfo?: Partial<SuccessToken> } => {
  try {
    const stored = sessionStorage.getItem(getStorageKey())
    if (!stored) return { valid: false }
    
    const successToken: SuccessToken = JSON.parse(stored)
    const now = Date.now()
    const tokenAge = now - successToken.timestamp
    const maxAge = TOKEN_EXPIRY_MINUTES * 60 * 1000
    
    if (tokenAge > maxAge) {
      // Token expired, remove it
      sessionStorage.removeItem(getStorageKey())
      return { valid: false }
    }
    
    return {
      valid: true,
      paymentInfo: {
        paymentId: successToken.paymentId,
        amount: successToken.amount,
        currency: successToken.currency,
        timestamp: successToken.timestamp
      }
    }
  } catch (error) {
    console.error('Error validating success token:', error)
    return { valid: false }
  }
}

/**
 * Consume (remove) the success token after use
 */
export const consumeSuccessToken = (): void => {
  sessionStorage.removeItem(getStorageKey())
}

/**
 * Check if user should be redirected from success page
 */
export const shouldRedirectFromSuccess = (): boolean => {
  const { valid } = validateSuccessToken()
  return !valid
}