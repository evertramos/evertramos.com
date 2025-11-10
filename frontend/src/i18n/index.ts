export const languages = {
  br: 'Português',
  en: 'English',
};

export const defaultLang = 'br';

export const translations = {
  br: {
    // Navigation
    'nav.home': 'Início',
    'nav.contact': 'Contato',
    'nav.payment': 'Pagamento',
    'nav.manage': 'Gerenciar',
    'nav.privacy': 'Privacidade',
    'nav.terms': 'Termos',
    
    // Home page
    'home.title': 'Desenvolvedor Full Stack',
    'home.subtitle': 'Especialista em Docker, DevSecOps e Desenvolvimento Web',
    'home.cta': 'Contratar Serviços',
    'home.manage': 'Ver Projetos',
    
    // Payment form
    'payment.title': 'Realizar Pagamento',
    'payment.name': 'Nome Completo',
    'payment.email': 'Email',
    'payment.phone': 'Telefone (opcional)',
    'payment.amount': 'Valor',
    'payment.currency': 'Moeda',
    'payment.type': 'Tipo de Pagamento',
    'payment.type.one_time': 'Pagamento Único',
    'payment.type.monthly': 'Mensal',
    'payment.type.yearly': 'Anual',
    'payment.card_info': 'Informações do Cartão',
    'payment.security_check': 'Verificação de Segurança',
    'payment.terms_accept': 'Eu aceito os',
    'payment.terms_link': 'termos de uso',
    'payment.privacy_link': 'política de privacidade',
    'payment.submit': 'Processar Pagamento',
    'payment.processing': 'Processando...',
    'payment.processing_title': 'Processando Pagamento',
    'payment.processing_message': 'Seu pagamento está sendo processado com segurança.',
    'payment.processing_wait': 'Por favor, não feche esta janela.',
    'payment.stripe_error': 'Erro ao carregar sistema de pagamento',
    'payment.security_error': 'Erro na verificação de segurança',
    
    // Validation messages
    'validation.name_required': 'Nome deve ter pelo menos 2 caracteres',
    'validation.email_invalid': 'Email inválido',
    'validation.amount_minimum': 'Valor mínimo é $1.00 ou R$1.00',
    'validation.security_required': 'Verificação de segurança obrigatória',
    'validation.terms_required': 'Você deve aceitar os termos de uso',
    
    // Error messages
    'error.payment_system_not_loaded': 'Sistema de pagamento não carregado. Recarregue a página.',
    'error.payment_processing': 'Erro ao processar pagamento',
    'error.payment_failed': 'Erro ao processar pagamento. Tente novamente.',
    
    // Success messages
    'success.payment': 'Pagamento processado com sucesso!',
    
    // Legacy messages
    'error.payment': 'Erro ao processar pagamento. Tente novamente.',
    'error.required': 'Este campo é obrigatório',
    'error.email': 'Email inválido',
    'error.amount': 'Valor deve ser maior que zero',
    
    // Footer
    'footer.privacy': 'Política de Privacidade',
    'footer.terms': 'Termos de Uso',
    'footer.secure': 'Pagamentos seguros processados pela Stripe',
  },
  en: {
    // Navigation
    'nav.home': 'Home',
    'nav.contact': 'Contact',
    'nav.payment': 'Payment',
    'nav.manage': 'Manage',
    'nav.privacy': 'Privacy',
    'nav.terms': 'Terms',
    
    // Home page
    'home.title': 'Full Stack Developer',
    'home.subtitle': 'Docker, DevSecOps and Web Development Specialist',
    'home.cta': 'Hire Services',
    'home.manage': 'View Projects',
    
    // Payment form
    'payment.title': 'Make Payment',
    'payment.name': 'Full Name',
    'payment.email': 'Email',
    'payment.phone': 'Phone (optional)',
    'payment.amount': 'Amount',
    'payment.currency': 'Currency',
    'payment.type': 'Payment Type',
    'payment.type.one_time': 'One-time Payment',
    'payment.type.monthly': 'Monthly',
    'payment.type.yearly': 'Yearly',
    'payment.card_info': 'Card Information',
    'payment.security_check': 'Security Verification',
    'payment.terms_accept': 'I accept the',
    'payment.terms_link': 'terms of use',
    'payment.privacy_link': 'privacy policy',
    'payment.submit': 'Process Payment',
    'payment.processing': 'Processing...',
    'payment.processing_title': 'Processing Payment',
    'payment.processing_message': 'Your payment is being processed securely.',
    'payment.processing_wait': 'Please do not close this window.',
    'payment.stripe_error': 'Error loading payment system',
    'payment.security_error': 'Security verification error',
    
    // Validation messages
    'validation.name_required': 'Name must be at least 2 characters',
    'validation.email_invalid': 'Invalid email',
    'validation.amount_minimum': 'Minimum amount is $1.00 or R$1.00',
    'validation.security_required': 'Security verification required',
    'validation.terms_required': 'You must accept the terms of use',
    
    // Error messages
    'error.payment_system_not_loaded': 'Payment system not loaded. Please reload the page.',
    'error.payment_processing': 'Error processing payment',
    'error.payment_failed': 'Error processing payment. Please try again.',
    
    // Success messages
    'success.payment': 'Payment processed successfully!',
    
    // Legacy messages
    'error.payment': 'Error processing payment. Please try again.',
    'error.required': 'This field is required',
    'error.email': 'Invalid email',
    'error.amount': 'Amount must be greater than zero',
    
    // Footer
    'footer.privacy': 'Privacy Policy',
    'footer.terms': 'Terms of Use',
    'footer.secure': 'Secure payments processed by Stripe',
  },
};

export function getLangFromUrl(url: URL) {
  // Extract language from URL path
  const [, lang] = url.pathname.split('/');
  if (lang === 'br') return 'br';
  if (lang === 'en') return 'en';
  
  // Fallback to default
  return defaultLang;
}

export function useTranslations(lang: keyof typeof translations) {
  return function t(key: keyof typeof translations[typeof defaultLang]) {
    return translations[lang][key] || translations[defaultLang][key];
  }
}

// Page mapping between languages
const pageMap = {
  // PT pages (br)
  '/br/': '/en/',
  '/br/pagamento': '/en/payment',
  '/br/privacidade': '/en/privacy',
  '/br/termos': '/en/terms',
  '/br/gerenciar': '/en/manage',
  '/br/sucesso': '/en/success',
  // EN pages
  '/en/': '/br/',
  '/en/payment': '/br/pagamento',
  '/en/privacy': '/br/privacidade',
  '/en/terms': '/br/termos',
  '/en/manage': '/br/gerenciar',
  '/en/success': '/br/sucesso'
};

export function getAlternateUrl(currentUrl: URL, currentLang: string): string {
  let currentPath = currentUrl.pathname;
  
  // Normalize path - remove trailing slash except for root
  if (currentPath.length > 1 && currentPath.endsWith('/')) {
    currentPath = currentPath.slice(0, -1);
  }
  
  // Add trailing slash for root paths
  if (currentPath === '/br' || currentPath === '/en') {
    currentPath += '/';
  }
  
  // Use direct mapping or fallback to home page
  return pageMap[currentPath] || (currentLang === 'br' ? '/en/' : '/br/');
}