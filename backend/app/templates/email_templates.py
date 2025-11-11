"""Email templates for different languages with professional design"""

# Base template with logo and professional styling
BASE_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ subject }}</title>
    <style>
        body { margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px 20px; text-align: center; }
        .logo { max-width: 80px; height: auto; margin-bottom: 10px; border-radius: 50%; }
        .header-text { color: #ffffff; font-size: 24px; font-weight: bold; margin: 0; }
        .content { padding: 40px 30px; }
        .status-badge { display: inline-block; padding: 8px 16px; border-radius: 20px; font-weight: bold; margin-bottom: 20px; }
        .success { background-color: #d4edda; color: #155724; }
        .error { background-color: #f8d7da; color: #721c24; }
        .details-box { background-color: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .footer { background-color: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; font-size: 14px; }
        .button { display: inline-block; padding: 12px 24px; background-color: #1e40af; color: #ffffff !important; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 10px 0; }
        @media (max-width: 600px) { .container { width: 100% !important; } .content { padding: 20px !important; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://evertramos.com.br/images/logo.png" alt="{{ company_name }}" class="logo">
            <h1 class="header-text">{{ header_title }}</h1>
        </div>
        <div class="content">
            {{ content }}
        </div>
        <div class="footer">
            <p>{{ company_name }} | {{ support_email }}</p>
            <p>Este é um email automático, não responda a esta mensagem.</p>
        </div>
    </div>
</body>
</html>
"""

EMAIL_TEMPLATES = {
    "pt": {
        "customer_success": {
            "subject": "✅ Pagamento Confirmado - {company_name}",
            "content": """
                <div class="status-badge success">✅ Pagamento Confirmado</div>
                
                <h2 style="color: #333; margin-bottom: 20px;">Olá {{ name }}!</h2>
                
                <p style="font-size: 16px; line-height: 1.6; color: #555;">Ótimas notícias! Seu pagamento foi processado com <strong>sucesso</strong> e já está confirmado em nosso sistema.</p>
                
                <div class="details-box">
                    <h3 style="margin-top: 0; color: #333;">📋 Detalhes do Pagamento</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 8px 0; font-weight: bold;">💰 Valor:</td><td style="padding: 8px 0;">{{ amount_display }}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">📅 Tipo:</td><td style="padding: 8px 0;">{{ payment_type_display }}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">🔢 ID:</td><td style="padding: 8px 0; font-family: monospace;">{{ payment_id }}</td></tr>
                    </table>
                </div>
                
                <p style="font-size: 16px; line-height: 1.6; color: #555;">Guarde este email como comprovante. Se precisar de ajuda, estamos aqui para você!</p>
                
                <a href="mailto:{{ support_email }}" class="button">💬 Falar com Suporte</a>
                
                <p style="margin-top: 30px; color: #666;">Atenciosamente,<br><strong>{{ company_name }}</strong></p>
            """
        },
        "customer_failed": {
            "subject": "❌ Problema no Pagamento - {company_name}",
            "content": """
                <div class="status-badge error">❌ Pagamento Não Processado</div>
                
                <h2 style="color: #333; margin-bottom: 20px;">Olá {{ name }},</h2>
                
                <p style="font-size: 16px; line-height: 1.6; color: #555;">Infelizmente, não conseguimos processar seu pagamento. Isso pode acontecer por diversos motivos, mas não se preocupe - é fácil resolver!</p>
                
                <div class="details-box">
                    <h3 style="margin-top: 0; color: #333;">📋 Detalhes da Tentativa</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 8px 0; font-weight: bold;">💰 Valor:</td><td style="padding: 8px 0;">{{ amount_display }}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">📅 Tipo:</td><td style="padding: 8px 0;">{{ payment_type_display }}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">🔢 ID:</td><td style="padding: 8px 0; font-family: monospace;">{{ payment_id }}</td></tr>
                    </table>
                </div>
                
                <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h4 style="margin-top: 0; color: #856404;">💡 O que fazer agora?</h4>
                    <ul style="margin-bottom: 0; color: #856404;">
                        <li>Verifique os dados do cartão</li>
                        <li>Confirme se há limite disponível</li>
                        <li>Tente novamente em alguns minutos</li>
                    </ul>
                </div>
                
                <a href="mailto:{{ support_email }}" class="button" style="background-color: #dc3545;">🆘 Preciso de Ajuda</a>
                
                <p style="margin-top: 30px; color: #666;">Estamos aqui para ajudar!<br><strong>{{ company_name }}</strong></p>
            """
        },
        "payment_types": {
            "one_time": "Pagamento único",
            "monthly": "Assinatura mensal",
            "yearly": "Assinatura anual"
        }
    },
    "en": {
        "customer_success": {
            "subject": "✅ Payment Confirmed - {company_name}",
            "content": """
                <div class="status-badge success">✅ Payment Confirmed</div>
                
                <h2 style="color: #333; margin-bottom: 20px;">Hi {{ name }}!</h2>
                
                <p style="font-size: 16px; line-height: 1.6; color: #555;">Great news! Your payment has been <strong>successfully processed</strong> and confirmed in our system.</p>
                
                <div class="details-box">
                    <h3 style="margin-top: 0; color: #333;">📋 Payment Details</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 8px 0; font-weight: bold;">💰 Amount:</td><td style="padding: 8px 0;">{{ amount_display }}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">📅 Type:</td><td style="padding: 8px 0;">{{ payment_type_display }}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">🔢 ID:</td><td style="padding: 8px 0; font-family: monospace;">{{ payment_id }}</td></tr>
                    </table>
                </div>
                
                <p style="font-size: 16px; line-height: 1.6; color: #555;">Keep this email as your receipt. If you need any assistance, we're here to help!</p>
                
                <a href="mailto:{{ support_email }}" class="button" style="background-color: #1e40af; color: #ffffff; text-decoration: none;">💬 Contact Support</a>
                
                <p style="margin-top: 30px; color: #666;">Best regards,<br><strong>{{ company_name }}</strong></p>
            """
        },
        "customer_failed": {
            "subject": "❌ Payment Issue - {company_name}",
            "content": """
                <div class="status-badge error">❌ Payment Not Processed</div>
                
                <h2 style="color: #333; margin-bottom: 20px;">Hi {{ name }},</h2>
                
                <p style="font-size: 16px; line-height: 1.6; color: #555;">Unfortunately, we couldn't process your payment. This can happen for various reasons, but don't worry - it's easy to resolve!</p>
                
                <div class="details-box">
                    <h3 style="margin-top: 0; color: #333;">📋 Attempt Details</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 8px 0; font-weight: bold;">💰 Amount:</td><td style="padding: 8px 0;">{{ amount_display }}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">📅 Type:</td><td style="padding: 8px 0;">{{ payment_type_display }}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">🔢 ID:</td><td style="padding: 8px 0; font-family: monospace;">{{ payment_id }}</td></tr>
                    </table>
                </div>
                
                <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h4 style="margin-top: 0; color: #856404;">💡 What to do now?</h4>
                    <ul style="margin-bottom: 0; color: #856404;">
                        <li>Check your card details</li>
                        <li>Verify available credit limit</li>
                        <li>Try again in a few minutes</li>
                    </ul>
                </div>
                
                <a href="mailto:{{ support_email }}" class="button" style="background-color: #dc3545;">🆘 Need Help</a>
                
                <p style="margin-top: 30px; color: #666;">We're here to help!<br><strong>{{ company_name }}</strong></p>
            """
        },
        "payment_types": {
            "one_time": "One-time payment",
            "monthly": "Monthly subscription",
            "yearly": "Yearly subscription"
        }
    }
}