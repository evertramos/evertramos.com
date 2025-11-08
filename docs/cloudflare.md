# Configuração Cloudflare - Bloqueio de Indexação

## 🛡️ **Configurações para Bloquear Mecanismos de Busca**

### **1. Transform Rules (PRIORIDADE ALTA)**
**Localização**: Rules → Transform Rules → HTTP Response Header Modification

**Configuração**:
- **Nome da Regra**: Block Search Engine Indexing
- **Campo**: All incoming requests
- **Operador**: matches
- **Valor**: `*` (todo o site)

**Headers a Adicionar**:
```
X-Robots-Tag: noindex, nofollow, noarchive, nosnippet, noimageindex, nocache
X-Robots-Tag: googlebot: noindex, nofollow, noarchive, nosnippet
X-Robots-Tag: bingbot: noindex, nofollow, noarchive, nosnippet
X-Robots-Tag: duckduckbot: noindex, nofollow, noarchive, nosnippet
```

### **2. WAF Custom Rules (PRIORIDADE ALTA)**
**Localização**: Security → WAF → Custom Rules

**Configuração**:
- **Nome da Regra**: Block Search Engine Bots
- **Campo**: User Agent
- **Operador**: contains
- **Valor**: `googlebot OR bingbot OR duckduckbot OR slurp OR facebookexternalhit OR twitterbot OR linkedinbot OR whatsapp OR applebot OR yandexbot OR baiduspider`
- **Ação**: Block
- **Resposta**: 403 Forbidden

### **3. Page Rules (PRIORIDADE MÉDIA)**
**Localização**: Rules → Page Rules

**Configuração**:
- **URL Pattern**: `*evertramos.com*` (ou seu domínio)
- **Configurações**:
  - Cache Level: Bypass
  - Browser Cache TTL: Respect Existing Headers
  - Security Level: High
  - Bot Fight Mode: On

### **4. Bot Fight Mode (PRIORIDADE MÉDIA)**
**Localização**: Security → Bots

**Configurações**:
- ✅ **Bot Fight Mode**: Ativado
- ✅ **Super Bot Fight Mode**: Ativado (se disponível no plano)
- **Configuração**: Definitely Automated → Block
- **Likely Automated**: Challenge (Managed Challenge)

### **5. Security Level (PRIORIDADE BAIXA)**
**Localização**: Security → Settings

**Configuração**:
- **Security Level**: High
- **Challenge Passage**: 30 minutes

### **6. Cache Settings (PRIORIDADE BAIXA)**
**Localização**: Caching → Configuration

**Configurações**:
- **Caching Level**: Standard
- **Browser Cache TTL**: 4 hours
- **Always Online**: Off (para evitar cache de bots)

### **7. Scrape Shield (PRIORIDADE BAIXA)**
**Localização**: Scrape Shield

**Configurações**:
- ✅ **Email Address Obfuscation**: Ativado
- ✅ **Server-side Excludes**: Ativado
- ✅ **Hotlink Protection**: Ativado

### **8. Network Settings (OPCIONAL)**
**Localização**: Network

**Configurações**:
- **HTTP/2**: Ativado
- **HTTP/3 (with QUIC)**: Ativado
- **0-RTT Connection Resumption**: Desativado (segurança)

## 🎯 **Ordem de Implementação**

1. **Transform Rules** (headers X-Robots-Tag) - IMPLEMENTAR PRIMEIRO
2. **WAF Custom Rules** (bloquear bots específicos) - IMPLEMENTAR SEGUNDO
3. **Bot Fight Mode** - IMPLEMENTAR TERCEIRO
4. **Page Rules** (configurações gerais) - IMPLEMENTAR QUARTO
5. Demais configurações conforme necessário

## ⚠️ **Notas Importantes**

- **Transform Rules** são processadas antes de qualquer outra regra
- **WAF Rules** bloqueiam bots antes mesmo deles acessarem o conteúdo
- **Bot Fight Mode** adiciona uma camada extra de proteção
- Teste as configurações em modo "Log" antes de ativar "Block"
- Monitore os logs para verificar efetividade

## 🔍 **Verificação**

Para verificar se está funcionando:
1. Acesse: `curl -H "User-Agent: Googlebot" https://seudominio.com`
2. Deve retornar erro 403 ou headers X-Robots-Tag
3. Verifique nos logs da Cloudflare se bots estão sendo bloqueados

## 📊 **Monitoramento**

- **Analytics → Security**: Verificar requests bloqueados
- **Security Events**: Monitorar tentativas de bots
- **Firewall Events**: Acompanhar regras WAF ativadas

---

**Última atualização**: Janeiro 2025  
**Testado em**: Cloudflare Free/Pro/Business Plans