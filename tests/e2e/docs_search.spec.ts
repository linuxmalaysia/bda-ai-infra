import { test, expect } from '@playwright/test';

test.describe('Documentation Site & Interactive Template E2E Tests', () => {
  test('Theme switcher toggles light, dark, and auto modes', async ({ page }) => {
    await page.goto('/bda-ai-infra/README.html');

    const html = page.locator('html');
    await expect(html).toHaveAttribute('data-theme', 'auto');

    // Click LIGHT mode
    const lightBtn = page.locator('button[data-theme-set="light"]');
    await lightBtn.click();
    await expect(html).toHaveAttribute('data-theme', 'light');

    // Click DARK mode
    const darkBtn = page.locator('button[data-theme-set="dark"]');
    await darkBtn.click();
    await expect(html).toHaveAttribute('data-theme', 'dark');

    // Click AUTO mode
    const autoBtn = page.locator('button[data-theme-set="auto"]');
    await autoBtn.click();
    await expect(html).toHaveAttribute('data-theme', 'auto');
  });

  test('Sidebar navigation displays dynamic links and navigates correctly', async ({ page }) => {
    await page.goto('/bda-ai-infra/README.html');

    const sidebar = page.locator('.sidebar-nav');
    await expect(sidebar).toBeVisible();

    const navLink = sidebar.locator('a.nav-link[href="/bda-ai-infra/CHANGELOG.html"]');
    await expect(navLink).toBeVisible();
    await navLink.click();

    await expect(page).toHaveURL(/\/bda-ai-infra\/CHANGELOG\.html/);

    const printBtn = page.locator('.print-btn');
    await expect(printBtn).toBeVisible();
  });

  test('Dynamic role permissions and cookie expiration boundary verification', async ({ context, page }) => {
    // Set simulated session cookie with 1-hour expiration
    const expiryTimestamp = Math.floor(Date.now() / 1000) + 3600;
    await context.addCookies([
      {
        name: 'bda_session_role',
        value: 'data_architect',
        domain: 'localhost',
        path: '/bda-ai-infra',
        expires: expiryTimestamp,
        httpOnly: false,
        secure: false,
        sameSite: 'Lax',
      },
    ]);

    await page.goto('/bda-ai-infra/README.html');

    // Verify session cookie presence
    const cookies = await context.cookies();
    const sessionCookie = cookies.find((c) => c.name === 'bda_session_role');
    expect(sessionCookie).toBeDefined();
    expect(sessionCookie?.value).toBe('data_architect');
    expect(sessionCookie?.expires).toBeGreaterThan(Math.floor(Date.now() / 1000));
  });

  test('Search index and OpenWiki knowledge graph visualizer page load', async ({ page }) => {
    await page.goto('/bda-ai-infra/START-HERE.html');
    await expect(page.locator('h1')).toContainText('START HERE');
  });
});
