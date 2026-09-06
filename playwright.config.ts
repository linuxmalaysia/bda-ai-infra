import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'list',
  use: {
    baseURL: 'http://localhost:8000/bda-ai-infra',
    trace: 'on-first-retry',
  },
  webServer: {
    command: 'sh -c "jekyll build -d _site && (ln -s . _site/bda-ai-infra 2>/dev/null || true) && python3 -m http.server 8000 --directory _site"',
    url: 'http://localhost:8000/bda-ai-infra/README.html',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
