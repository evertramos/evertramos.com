# Regras Específicas - Integração Stripe

## 🔐 SEGURANÇA STRIPE

### Webhooks
- **SEMPRE** verificar assinatura do webhook
- **SEMPRE** usar endpoint_secret do Stripe
- **SEMPRE** implementar idempotência
- **SEMPRE** logar eventos para auditoria
- **NUNCA** confiar em dados sem verificação

### Chaves API
- **SEMPRE** usar chaves diferentes para test/prod
- **SEMPRE** armazenar em variáveis de ambiente
- **NUNCA** commitar chaves no código
- **SEMPRE** rotacionar chaves periodicamente

### Pagamentos
- **SEMPRE** validar valores no servidor
- **SEMPRE** usar centavos (integers) para valores
- **SEMPRE** implementar retry logic
- **SEMPRE** salvar transaction_id
- **NUNCA** processar pagamentos apenas no frontend

### Dados Sensíveis
- **NUNCA** armazenar dados de cartão
- **SEMPRE** usar Stripe Elements no frontend
- **SEMPRE** tokenizar dados sensíveis
- **SEMPRE** cumprir PCI DSS requirements

## 📊 MONITORAMENTO
- **SEMPRE** logar tentativas de pagamento
- **SEMPRE** monitorar falhas de webhook
- **SEMPRE** alertar sobre transações suspeitas
- **SEMPRE** backup de dados críticos