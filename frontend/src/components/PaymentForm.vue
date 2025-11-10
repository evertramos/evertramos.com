<template>
  <div class="payment-form-container">
    <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8">
    <h2 class="text-3xl font-bold text-gray-900 mb-8 text-center">
      {{ t('payment.title') }}
    </h2>
    
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Customer Information -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
            {{ t('payment.name') }} *
          </label>
          <input
            v-model="form.name"
            type="text"
            id="name"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            :class="{ 'border-red-500': errors.name }"
            placeholder="John Doe"
          />
          <div v-if="errors.name" class="text-red-600 text-sm mt-1">{{ errors.name }}</div>
        </div>
        
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
            {{ t('payment.email') }} *
          </label>
          <input
            v-model="form.email"
            type="email"
            id="email"
            required
            @blur="validateEmail"
            @input="clearEmailError"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            :class="{ 'border-red-500': errors.email }"
            placeholder="john@example.com"
          />
          <div v-if="errors.email" class="text-red-600 text-sm mt-1">{{ errors.email }}</div>
        </div>
      </div>
      
      <div>
        <label for="phone" class="block text-sm font-medium text-gray-700 mb-2">
          {{ t('payment.phone') }}
        </label>
        <input
          v-model="form.phone"
          type="tel"
          id="phone"
          class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
          placeholder="+55 11 99999-9999"
        />
      </div>
      
      <!-- Payment Information -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label for="amount" class="block text-sm font-medium text-gray-700 mb-2">
            {{ t('payment.amount') }} *
          </label>
          <input
            v-model="form.amount"
            type="number"
            id="amount"
            required
            min="1.00"
            step="0.01"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            :class="{ 'border-red-500': errors.amount }"
            placeholder="10.00"
          />
          <div v-if="errors.amount" class="text-red-600 text-sm mt-1">{{ errors.amount }}</div>
        </div>
        
        <div>
          <label for="currency" class="block text-sm font-medium text-gray-700 mb-2">
            {{ t('payment.currency') }} *
          </label>
          <select
            v-model="form.currency"
            id="currency"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
          >
            <option value="usd">USD ($)</option>
            <option value="brl">BRL (R$)</option>
          </select>
        </div>
        
        <div>
          <label for="payment-type" class="block text-sm font-medium text-gray-700 mb-2">
            {{ t('payment.type') }} *
          </label>
          <select
            v-model="form.paymentType"
            id="payment-type"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
          >
            <option value="one_time">{{ t('payment.type.one_time') }}</option>
            <option value="monthly">{{ t('payment.type.monthly') }}</option>
            <option value="yearly">{{ t('payment.type.yearly') }}</option>
          </select>
        </div>
      </div>
      
      <!-- Stripe Elements Container -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ t('payment.card_info') }} *
        </label>
        <div id="card-element" class="p-4 border border-gray-300 rounded-lg bg-white">
          <!-- Stripe Elements will create form elements here -->
        </div>
        <div v-if="cardError" class="text-red-600 text-sm mt-2">{{ cardError }}</div>
      </div>
      
      <!-- Cloudflare Turnstile -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ t('payment.security_check') }} *
        </label>
        <div id="turnstile-widget" class="flex justify-center">
          <!-- Turnstile widget will be rendered here -->
        </div>
        <div v-if="turnstileError" class="text-red-600 text-sm mt-2">{{ turnstileError }}</div>
      </div>
      
      <!-- Terms Acceptance -->
      <div>
        <div class="flex items-start space-x-3">
          <input
            v-model="termsAccepted"
            type="checkbox"
            id="terms"
            class="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            :class="{ 'border-red-500': termsError }"
          />
          <label for="terms" class="text-sm text-gray-700">
            {{ t('payment.terms_accept') }} 
            <a :href="props.lang === 'pt' ? '/termos' : '/en/terms'" target="_blank" class="text-blue-600 hover:underline font-medium">{{ t('payment.terms_link') }}</a>
            {{ props.lang === 'pt' ? 'e a' : 'and' }} 
            <a :href="props.lang === 'pt' ? '/privacidade' : '/en/privacy'" target="_blank" class="text-blue-600 hover:underline font-medium">{{ t('payment.privacy_link') }}</a>
            *
          </label>
        </div>
        <div v-if="termsError" class="text-red-600 text-sm mt-1 ml-7">{{ termsError }}</div>
      </div>
      
      <!-- Submit Button -->
      <button
        type="submit"
        :disabled="loading"
        class="w-full bg-blue-600 text-white py-4 px-6 rounded-lg text-lg font-semibold hover:bg-blue-700 focus:ring-4 focus:ring-blue-200 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="!loading">{{ t('payment.submit') }}</span>
        <span v-else class="flex items-center justify-center">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ t('payment.processing') }}
        </span>
      </button>
    </form>
    
    <!-- Success/Error Messages -->
    <div v-if="message" class="mt-6">
      <div v-if="success" class="bg-green-50 border border-green-200 rounded-lg p-4">
        <div class="flex">
          <svg class="w-5 h-5 text-green-400 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-green-800">{{ message }}</h3>
          </div>
        </div>
      </div>
      
      <div v-else class="bg-red-50 border border-red-200 rounded-lg p-4">
        <div class="flex">
          <svg class="w-5 h-5 text-red-400 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
          </svg>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">{{ message }}</h3>
          </div>
        </div>
      </div>
    </div>
    </div>
    
    <!-- Processing Overlay -->
    <div v-if="loading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl p-8 max-w-sm mx-4 text-center">
        <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <h3 class="text-lg font-semibold text-gray-900 mb-2">
          {{ t('payment.processing_title') }}
        </h3>
        <p class="text-gray-600 text-sm">
          {{ t('payment.processing_message') }}
        </p>
        <div class="mt-4 text-xs text-gray-500">
          {{ t('payment.processing_wait') }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Disable automatic attribute inheritance to prevent warnings
defineOptions({
  inheritAttrs: false
})
import { ref, reactive, onMounted, watch } from 'vue'
import { loadStripe } from '@stripe/stripe-js'
import { saveFormData, loadFormData, clearFormData, cleanupExpiredData, type FormData } from '../utils/formPersistence'
import { generateSuccessToken } from '../utils/successToken'

// Props
interface Props {
  lang: string
  translations: Record<string, string>
}

const props = defineProps<Props>()

// Translation helper
const t = (key: string) => props.translations[key] || key

// Reactive state
const form = reactive({
  name: '',
  email: '',
  phone: '',
  amount: '',
  currency: 'usd',
  paymentType: 'one_time'
})

const errors = reactive({
  name: '',
  email: '',
  amount: ''
})

const loading = ref(false)
const success = ref(false)
const message = ref('')
const cardError = ref('')
const turnstileError = ref('')
const turnstileToken = ref('')
const termsAccepted = ref(false)
const termsError = ref('')

// Stripe
let stripe: any = null
let elements: any = null
let cardElement: any = null

// Turnstile - Disabled for development
let turnstile: any = null

// Backend URL - will be validated on mount
const BACKEND_URL = ref('')

// Initialize Turnstile
const initializeTurnstile = () => {
  if (window.turnstile) {
    const sitekey = import.meta.env.PUBLIC_TURNSTILE_SITE_KEY
    if (!sitekey) {
      console.error('PUBLIC_TURNSTILE_SITE_KEY environment variable is required')
      return
    }
    
    turnstile = window.turnstile.render('#turnstile-widget', {
      sitekey: sitekey,
      language: props.lang, // Set language based on page language
      callback: (token: string) => {
        turnstileToken.value = token
        turnstileError.value = ''
      },
      'error-callback': () => {
        turnstileError.value = t('payment.security_error')
        turnstileToken.value = ''
      }
    })
  } else {
    setTimeout(initializeTurnstile, 100)
  }
}

// Initialize Stripe
const initializeStripe = async () => {
  try {
    // Get Stripe config and session key from backend
    const response = await fetch(`${BACKEND_URL.value}/api/v1/payments/config`)
    const config = await response.json()
    
    // Store session key for API calls
    sessionStorage.setItem('session_key', config.session_key)
    
    stripe = await loadStripe(config.publishable_key)
    elements = stripe.elements({
      locale: props.lang
    })
    
    // Create card element
    cardElement = elements.create('card', {
      style: {
        base: {
          fontSize: '16px',
          color: '#424770',
          '::placeholder': {
            color: '#aab7c4',
          },
        },
      }
    })
    
    cardElement.mount('#card-element')
    
    // Handle real-time validation errors from the card Element
    cardElement.on('change', ({ error }: any) => {
      cardError.value = error ? error.message : ''
    })
    
  } catch (error) {
    console.error('Error initializing Stripe:', error)
    showError(t('payment.stripe_error') || 'Error loading payment system. Please try again.')
  }
}

// Form validation
const validateForm = () => {
  // Clear previous errors
  errors.name = ''
  errors.email = ''
  errors.amount = ''
  turnstileError.value = ''
  termsError.value = ''
  
  let isValid = true
  
  if (!form.name || form.name.length < 2) {
    errors.name = t('validation.name_required')
    isValid = false
  }
  
  // Enhanced email validation
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  if (!form.email || !emailRegex.test(form.email)) {
    errors.email = t('validation.email_invalid')
    isValid = false
  }
  
  const amount = parseFloat(form.amount)
  if (!amount || amount < 1.0) {
    errors.amount = t('validation.amount_minimum')
    isValid = false
  }
  
  if (!turnstileToken.value) {
    turnstileError.value = t('validation.security_required')
    isValid = false
  }
  
  if (!termsAccepted.value) {
    termsError.value = t('validation.terms_required')
    isValid = false
  }
  
  return isValid
}

// Handle form submission
const handleSubmit = async () => {
  if (!stripe || !cardElement) {
    showError(t('error.payment_system_not_loaded'))
    return
  }
  
  if (!validateForm()) {
    return
  }
  
  loading.value = true
  
  try {
    // Prepare payment data
    const paymentData = {
      name: form.name,
      email: form.email,
      phone: form.phone || null,
      amount: Math.round(parseFloat(form.amount) * 100), // Convert to cents
      currency: form.currency,
      payment_type: form.paymentType,
      turnstile_token: turnstileToken.value,
      language: props.lang // Send user's language
    }
    
    // Create payment on backend
    const sessionKey = sessionStorage.getItem('session_key')
    if (!sessionKey) {
      throw new Error('Session expired. Please refresh the page.')
    }
    
    const response = await fetch(`${BACKEND_URL.value}/api/v1/payments/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Session-Key': sessionKey
      },
      body: JSON.stringify(paymentData)
    })
    
    const result = await response.json()
    
    if (!result.success) {
      throw new Error(result.message || 'Payment processing failed')
    }
    
    // Confirm payment with Stripe
    const { error } = await stripe.confirmCardPayment(result.client_secret, {
      payment_method: {
        card: cardElement,
        billing_details: {
          name: form.name,
          email: form.email,
          phone: form.phone
        }
      }
    })
    
    if (error) {
      throw new Error(error.message)
    }
    
    // Extract payment info for success token
    const paymentAmount = Math.round(parseFloat(form.amount) * 100)
    showSuccess(result.payment_id, paymentAmount, form.currency)
    // Don't reset form or stop loading until redirect
    
  } catch (error: any) {
    console.error('Payment error:', error)
    showError(error.message || t('error.payment_failed'))
    loading.value = false // Only stop loading on error
  }
  
  // Don't set loading.value = false on success - let redirect handle it
}

// Email validation functions
const validateEmail = () => {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  if (form.email && !emailRegex.test(form.email)) {
    errors.email = t('validation.email_invalid')
  }
}

const clearEmailError = () => {
  if (errors.email) {
    errors.email = ''
  }
}

// Helper functions
const showSuccess = (paymentId?: string, amount?: number, currency?: string) => {
  // Generate success token with payment info
  const token = generateSuccessToken(paymentId, amount, currency)
  
  // Redirect to success page after 1.5 seconds
  setTimeout(() => {
    const successUrl = props.lang === 'pt' ? '/sucesso' : '/en/success'
    window.location.href = `${successUrl}?token=${token}`
  }, 1500)
}

const showError = (errorMessage: string) => {
  success.value = false
  message.value = errorMessage
}

const resetForm = () => {
  Object.assign(form, {
    name: '',
    email: '',
    phone: '',
    amount: '',
    currency: 'usd',
    paymentType: 'one_time'
  })
  
  if (cardElement) {
    cardElement.clear()
  }
  
  // Clear saved data after successful payment
  clearFormData()
}

// Fill form from URL parameters or localStorage
const fillFormFromURL = () => {
  const urlParams = new URLSearchParams(window.location.search)
  
  // First try URL parameters (higher priority)
  if (urlParams.get('name')) form.name = decodeURIComponent(urlParams.get('name')!)
  if (urlParams.get('email')) form.email = decodeURIComponent(urlParams.get('email')!)
  if (urlParams.get('phone')) form.phone = decodeURIComponent(urlParams.get('phone')!)
  if (urlParams.get('amount')) form.amount = urlParams.get('amount')!
  if (urlParams.get('currency')) form.currency = urlParams.get('currency')!
  if (urlParams.get('type')) form.paymentType = urlParams.get('type')!
  
  // If no URL params, try to load from localStorage
  if (!urlParams.toString()) {
    const savedData = loadFormData()
    if (savedData) {
      form.name = savedData.name
      form.email = savedData.email
      form.phone = savedData.phone
      form.amount = savedData.amount
      form.currency = savedData.currency
      form.paymentType = savedData.paymentType
    }
  }
}

// Watch form changes and save to localStorage
watch(
  () => ({ ...form }),
  (newForm) => {
    // Only save if form has meaningful data
    if (newForm.name || newForm.email || newForm.amount) {
      saveFormData(newForm as FormData)
    }
  },
  { deep: true }
)

// Lifecycle
onMounted(() => {
  // Validate environment variables
  if (!import.meta.env.PUBLIC_BACKEND_URL) {
    console.error('PUBLIC_BACKEND_URL environment variable is required')
    showError('Configuration error: Backend URL not configured')
    return
  }
  
  BACKEND_URL.value = import.meta.env.PUBLIC_BACKEND_URL
  
  // Clean up any expired form data first
  cleanupExpiredData()
  
  initializeStripe()
  initializeTurnstile()
  fillFormFromURL()
})
</script>