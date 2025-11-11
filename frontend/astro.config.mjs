import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import vue from '@astrojs/vue';

export default defineConfig({
  output: 'static',
  build: {
    inlineStylesheets: 'auto',
    assets: '_astro'
  },
  vite: {
    define: {
      'import.meta.env.PUBLIC_STRIPE_CUSTOMER_PORTAL_URL': JSON.stringify(process.env.PUBLIC_STRIPE_CUSTOMER_PORTAL_URL)
    },
    build: {
      minify: 'esbuild',
      cssMinify: 'esbuild',
      sourcemap: false,
      rollupOptions: {
        output: {
          manualChunks: undefined
        }
      }
    }
  },
  integrations: [tailwind(), vue()],
  i18n: {
    defaultLocale: "br",
    locales: ["br", "en"],
    routing: {
      prefixDefaultLocale: true,
      redirectToDefaultLocale: false
    },
    fallback: {
      en: "br"
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