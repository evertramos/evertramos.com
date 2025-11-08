export const languages = {
  pt: 'Português',
  en: 'English',
};

export const defaultLang = 'pt';

export const translations = {
  pt: {
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
    'payment.submit': 'Processar Pagamento',
    'payment.processing': 'Processando...',
    
    // Messages
    'success.payment': 'Pagamento processado com sucesso!',
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
    'payment.submit': 'Process Payment',
    'payment.processing': 'Processing...',
    
    // Messages
    'success.payment': 'Payment processed successfully!',
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
  const [, lang] = url.pathname.split('/');
  if (lang in languages) return lang as keyof typeof languages;
  return defaultLang;
}

export function useTranslations(lang: keyof typeof translations) {
  return function t(key: keyof typeof translations[typeof defaultLang]) {
    return translations[lang][key] || translations[defaultLang][key];
  }
}