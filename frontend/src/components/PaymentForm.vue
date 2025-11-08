<template>
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
          Informações do Cartão *
        </label>
        <div id="card-element" class="p-4 border border-gray-300 rounded-lg bg-white">
          <!-- Stripe Elements will create form elements here -->
        </div>
        <div v-if="cardError" class="text-red-600 text-sm mt-2">{{ cardError }}</div>
      </div>
      
      <!-- Cloudflare Turnstile -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Verificação de Segurança *
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
            Li e aceito os 
            <a :href="props.lang === 'pt' ? '/termos' : '/en/terms'" target="_blank" class="text-blue-600 hover:underline font-medium">Termos de Uso</a>
            e a 
            <a :href="props.lang === 'pt' ? '/privacidade' : '/en/privacy'" target="_blank" class="text-blue-600 hover:underline font-medium">Política de Privacidade</a>
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
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { loadStripe } from '@stripe/stripe-js'
import { saveFormData, loadFormData, clearFormData, type FormData } from '../utils/formPersistence'

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

const BACKEND_URL = import.meta.env.PUBLIC_BACKEND_URL || 'https://pay.ezyba.com'

// Initialize Turnstile
const initializeTurnstile = () => {
  if (window.turnstile) {
    turnstile = window.turnstile.render('#turnstile-widget', {
      sitekey: '1x00000000000000000000AA', // Test key - always passes
      callback: (token: string) => {
        turnstileToken.value = token
        turnstileError.value = ''
      },
      'error-callback': () => {
        turnstileError.value = 'Erro na verificação de segurança. Tente novamente.'
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
    // Get Stripe config from backend
    const response = await fetch(`${BACKEND_URL}/api/v1/payments/config`)
    const config = await response.json()
    
    stripe = await loadStripe(config.publishable_key)
    elements = stripe.elements()
    
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
      },
    })
    
    cardElement.mount('#card-element')
    
    // Handle real-time validation errors from the card Element
    cardElement.on('change', ({ error }: any) => {
      cardError.value = error ? error.message : ''
    })
    
  } catch (error) {
    console.error('Error initializing Stripe:', error)
    showError('Erro ao carregar sistema de pagamento. Tente novamente.')
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
    errors.name = 'Nome deve ter pelo menos 2 caracteres'
    isValid = false
  }
  
  if (!form.email || !form.email.includes('@')) {
    errors.email = 'Email inválido'
    isValid = false
  }
  
  const amount = parseFloat(form.amount)
  if (!amount || amount < 1.0) {
    errors.amount = 'Valor mínimo é $1.00 ou R$1.00'
    isValid = false
  }
  
  if (!turnstileToken.value) {
    turnstileError.value = 'Verificação de segurança obrigatória'
    isValid = false
  }
  
  if (!termsAccepted.value) {
    termsError.value = 'Você deve aceitar os termos de uso'
    isValid = false
  }
  
  return isValid
}

// Handle form submission
const handleSubmit = async () => {
  if (!stripe || !cardElement) {
    showError('Sistema de pagamento não carregado. Recarregue a página.')
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
      turnstile_token: turnstileToken.value
    }
    
    // Create payment on backend
    const response = await fetch(`${BACKEND_URL}/api/v1/payments/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ezyba-secure-api-key-2024'
      },
      body: JSON.stringify(paymentData)
    })
    
    const result = await response.json()
    
    if (!result.success) {
      throw new Error(result.message || 'Erro ao processar pagamento')
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
    
    showSuccess()
    resetForm()
    
  } catch (error: any) {
    console.error('Payment error:', error)
    showError(error.message || 'Erro ao processar pagamento. Tente novamente.')
  }
  
  loading.value = false
}

// Helper functions
const showSuccess = () => {
  success.value = true
  message.value = t('success.payment')
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
  initializeStripe()
  initializeTurnstile() // Auto-bypassed for development
  fillFormFromURL()
})
</script>