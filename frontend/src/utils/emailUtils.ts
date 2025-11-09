/**
 * Utility functions for handling email addresses securely
 */

// Get email addresses from environment variables
const getFinancialEmail = () => import.meta.env.PUBLIC_FINANCIAL_EMAIL || 'finance@ezyba.com'
const getLegalEmail = () => import.meta.env.PUBLIC_LEGAL_EMAIL || 'legal@ezyba.com'

/**
 * Create a bot-protected email link
 * @param email - Email address
 * @param displayText - Text to display (optional)
 * @returns Object with onclick handler and display text
 */
export const createProtectedEmailLink = (email: string, displayText?: string) => {
  const [localPart, domain] = email.split('@')
  return {
    onclick: `location.href='mailto:'+['${localPart}','${domain}'].join('@')`,
    display: displayText || email, // Show full email to users
    email: email
  }
}

/**
 * Get protected financial email link
 */
export const getProtectedFinancialEmail = () => {
  return createProtectedEmailLink(getFinancialEmail())
}

/**
 * Get protected legal email link  
 */
export const getProtectedLegalEmail = () => {
  return createProtectedEmailLink(getLegalEmail())
}

/**
 * Email types for different contexts
 */
export const EMAIL_TYPES = {
  FINANCIAL: 'financial', // Payments, refunds, billing
  LEGAL: 'legal',         // Privacy, terms, compliance
} as const

/**
 * Get appropriate email for context
 */
export const getContextualEmail = (type: keyof typeof EMAIL_TYPES) => {
  switch (type) {
    case 'FINANCIAL':
      return getProtectedFinancialEmail()
    case 'LEGAL':
      return getProtectedLegalEmail()
    default:
      return getProtectedFinancialEmail()
  }
}