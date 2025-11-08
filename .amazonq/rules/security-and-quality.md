# Regras de Desenvolvimento - Ezyba Project

## Stack: Astro (Frontend) + FastAPI (Backend) + Stripe

### 🔒 SEGURANÇA OBRIGATÓRIA

#### Backend (Python/FastAPI)
- **SEMPRE** validar entrada com Pydantic models
- **SEMPRE** usar type hints em todas as funções
- **SEMPRE** sanitizar dados antes de queries SQL
- **SEMPRE** implementar rate limiting
- **SEMPRE** usar HTTPS em produção
- **SEMPRE** validar webhooks Stripe com assinatura
- **NUNCA** expor chaves secretas no código
- **NUNCA** fazer queries SQL diretas sem ORM/validação
- **SEMPRE** usar variáveis de ambiente para secrets

#### Frontend (Astro)
- **SEMPRE** usar Content Security Policy (CSP)
- **SEMPRE** sanitizar dados do usuário
- **NUNCA** incluir dados sensíveis no cliente
- **SEMPRE** usar HTTPS
- **SEMPRE** validar formulários no servidor também
- **NUNCA** confiar apenas em validação client-side

### 🛡️ VERIFICAÇÃO CVE
- **SEMPRE** verificar dependências por vulnerabilidades conhecidas
- **SEMPRE** usar versões LTS/estáveis
- **SEMPRE** atualizar dependências críticas de segurança
- **SEMPRE** revisar changelogs antes de updates

### 📱 RESPONSIVIDADE OBRIGATÓRIA
- **SEMPRE** testar em mobile-first
- **SEMPRE** usar breakpoints: 320px, 768px, 1024px, 1440px
- **SEMPRE** verificar touch targets (min 44px)
- **SEMPRE** testar orientação portrait/landscape
- **SEMPRE** otimizar imagens para diferentes densidades

### 🌍 MULTILÍNGUE (PT/EN)
- **SEMPRE** implementar i18n desde o início
- **SEMPRE** usar chaves de tradução consistentes
- **SEMPRE** validar traduções em ambos idiomas
- **SEMPRE** testar URLs localizadas (/pt/, /en/)
- **SEMPRE** configurar hreflang para SEO

### 🧪 TESTES OBRIGATÓRIOS
- **SEMPRE** criar testes unitários para novas funções
- **SEMPRE** criar testes de integração para APIs
- **SEMPRE** testar cenários de erro
- **SEMPRE** testar validação de entrada
- **SEMPRE** mockar chamadas externas (Stripe)
- **SEMPRE** manter cobertura > 80%

### 📋 CHECKLIST PRE-COMMIT
- [ ] Código passa em todos os testes
- [ ] Sem vulnerabilidades de segurança
- [ ] Responsivo em todos breakpoints
- [ ] Traduções PT/EN funcionando
- [ ] Type hints completos (Python)
- [ ] CSP configurado (Frontend)
- [ ] Rate limiting implementado (APIs)
- [ ] Logs estruturados adicionados

### 🚫 NUNCA FAZER
- Hardcode de credentials
- SQL injection vulnerável
- XSS vulnerável
- Dados sensíveis no frontend
- Deploy sem HTTPS
- APIs sem rate limiting
- Código sem testes
- UI não responsiva