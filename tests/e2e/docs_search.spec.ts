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

    // Check sidebar navigation links
    const sidebar = page.locator('.sidebar-nav');
    await expect(sidebar).toBeVisible();

    const navLink = sidebar.locator('a.nav-link[href="/bda-ai-infra/SUMMARY.html"]');
    await expect(navLink).toBeVisible();
    await navLink.click();

    await expect(page).toHaveURL(/\/bda-ai-infra\/SUMMARY\.html/);

    // Verify print button presence
    const printBtn = page.locator('.print-btn');
    await expect(printBtn).toBeVisible();
  });
});
