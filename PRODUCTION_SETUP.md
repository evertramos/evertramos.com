# 🚀 Setup de Produção - Mailtrap API

## ⚙️ **Variáveis Atualizadas no Docker Compose**

### **Removidas (SMTP):**
```bash
SMTP_HOST
SMTP_PORT  
SMTP_USER
SMTP_PASSWORD
```

### **Adicionadas (Mailtrap API):**
```bash
MAILTRAP_API_TOKEN
SENDER_EMAIL
SENDER_NAME
COMPANY_NAME
SUPPORT_EMAIL
USD_SYMBOL
BRL_SYMBOL
```

## 📋 **Checklist para Deploy de Produção**

### 1. **Configurar .env de Produção**
```bash
# Copiar template
cp .env.production.example .env

# Editar com valores reais
nano .env
```

### 2. **Variáveis Críticas para Alterar:**
- ✅ `ENVIRONMENT=production`
- ✅ `MAILTRAP_API_TOKEN=` (token real do Mailtrap)
- ✅ `STRIPE_SECRET_KEY=sk_live_...` (chave live)
- ✅ `STRIPE_PUBLISHABLE_KEY=pk_live_...` (chave live)
- ✅ `TURNSTILE_SECRET_KEY=` (chave real do Cloudflare)
- ✅ `API_KEY=` (gerar nova chave segura)

### 3. **Mailtrap Setup**
1. **Login no Mailtrap**
2. **Criar projeto de produção**
3. **Copiar API Token**
4. **Configurar domínio de envio**

### 4. **Deploy**
```bash
# Parar ambiente atual
docker compose down

# Deploy produção
docker compose up -d --build

# Verificar logs
docker compose logs -f evertramos-backend
```

## 🔍 **Verificação Pós-Deploy**

### **Logs para Monitorar:**
```bash
# Email service sendo usado
grep "Using.*Service" logs

# Emails sendo enviados
grep "\[MAILTRAP\]" logs

# Erros de configuração
grep "ERROR" logs
```

### **Teste de Email:**
1. **Fazer pagamento teste**
2. **Verificar dashboard Mailtrap**
3. **Confirmar recebimento dos emails**

## ⚠️ **Importante**

- **Development**: Usa Mailpit (SMTP local)
- **Production**: Usa Mailtrap API
- **Troca automática** baseada em `ENVIRONMENT`

## 🎯 **Resultado Esperado**

```bash
[MAILTRAP] Using MailtrapService (API) for environment: production
[MAILTRAP] Customer email sent successfully
[MAILTRAP] Admin email sent successfully
```

Sistema pronto para produção com Mailtrap API! 🚀