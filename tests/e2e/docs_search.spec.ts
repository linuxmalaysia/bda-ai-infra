import { test, expect } from '@playwright/test';

test.describe('Documentation Site & Search Indexing E2E Tests', () => {
  test('Search modal opens and indexes documentation pages', async ({ page }) => {
    // Navigate to local documentation server homepage
    await page.goto('/');

    // Verify main header title
    await expect(page).toHaveTitle(/Big Data Analytics|DSOM/i);

    // Open search modal (either clicking search input or pressing '/')
    const searchButton = page.locator('button[data-md-component="search"], input[type="search"]');
    if (await searchButton.isVisible()) {
      await searchButton.click();
    } else {
      await page.keyboard.press('/');
    }

    // Type query into search field
    const searchInput = page.locator('input[data-md-component="search-query"], input[placeholder*="Search"]');
    await searchInput.fill('Lakehouse');

    // Verify search results are generated
    const searchResults = page.locator('.md-search-result__item, .search-result');
    await expect(searchResults.first()).toBeVisible();

    // Click on the first search result and verify navigation
    await searchResults.first().click();
    await expect(page).toHaveURL(/lakehouse|architecture/i);
  });
});
