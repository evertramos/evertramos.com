import { defineMiddleware } from 'astro:middleware';

export const onRequest = defineMiddleware(async (context, next) => {
  const { url, redirect } = context;
  
  // Skip middleware for static assets
  if (url.pathname.startsWith('/_astro/') || 
      url.pathname.startsWith('/images/') || 
      url.pathname.includes('.')) {
    return next();
  }
  
  const hostname = url.hostname;
  const pathname = url.pathname;
  
  // Skip middleware for localhost/development
  if (hostname.includes('localhost') || hostname.includes('127.0.0.1')) {
    return next();
  }
  
  // Domain-based language routing (production only)
  if (hostname === 'evertramos.com') {
    // English domain - redirect Portuguese paths to English paths
    const pathMap: Record<string, string> = {
      '/pagamento': '/payment',
      '/privacidade': '/privacy', 
      '/termos': '/terms',
      '/gerenciar': '/manage',
      '/sucesso': '/success'
    };
    
    const englishPath = pathMap[pathname];
    if (englishPath) {
      return redirect(englishPath, 301);
    }
  }
  
  if (hostname === 'evertramos.com.br') {
    // Portuguese domain - redirect English paths to Portuguese paths
    const pathMap: Record<string, string> = {
      '/payment': '/pagamento',
      '/privacy': '/privacidade',
      '/terms': '/termos', 
      '/manage': '/gerenciar',
      '/success': '/sucesso'
    };
    
    const portuguesePath = pathMap[pathname];
    if (portuguesePath) {
      return redirect(portuguesePath, 301);
    }
  }
  
  return next();
});