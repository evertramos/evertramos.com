import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import vue from '@astrojs/vue';

export default defineConfig({
  vite: {
    define: {
      'import.meta.env.STRIPE_CUSTOMER_PORTAL_URL': JSON.stringify(process.env.STRIPE_CUSTOMER_PORTAL_URL || 'http://localhost:8000/api/v1/payments/customer-portal')
    }
  },
  integrations: [tailwind(), vue()],
  i18n: {
    defaultLocale: "pt",
    locales: ["pt", "en"],
    routing: {
      prefixDefaultLocale: false
    }
  },
  server: {
    host: '0.0.0.0',
    port: 3000
  },
  security: {
    checkOrigin: true
  }
});