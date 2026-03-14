// @ts-check
const { test, expect } = require('@playwright/test');
const path = require('path');

const HTML_PATH = path.join(__dirname, '..', 'CIV 5.html');

test.describe('Civilisations of the Middle Seas', () => {
  test.beforeEach(async ({ page }) => {
    // Listen for uncaught JS errors
    page.on('pageerror', (err) => {
      console.error('Uncaught page error:', err.message);
      throw err;
    });
  });

  test('full AI game completes without errors', async ({ page }) => {
    test.setTimeout(360000); // 6 min for full AI game
    await page.goto(`file:///${HTML_PATH.replace(/\\/g, '/')}`);
    
    // Wait for setup to load
    await page.waitForSelector('#playerSetup', { timeout: 5000 });
    
    // Set both players to AI (Hard) for faster gameplay
    const playerTypes = await page.locator('.player-type');
    await expect(playerTypes).toHaveCount(2);
    await playerTypes.nth(0).selectOption('ai-hard');
    await playerTypes.nth(1).selectOption('ai-hard');
    
    // Set short AI thinking time (Fast = 3s) for quicker test
    const aiThinkingSelect = page.locator('select#aiThinkingTime');
    if (await aiThinkingSelect.count() > 0) {
      await aiThinkingSelect.selectOption('3');
    }
    
    // Start game
    await page.click('button:has-text("Start Game")');
    
    // Wait for game board to appear
    await page.waitForSelector('.game-board.active', { timeout: 5000 });
    
    // Dismiss conquest/war modals as they appear (AI-only game needs manual advancement)
    // Poll and click Continue buttons until final scoring appears
    const startTime = Date.now();
    const timeout = 300000; // 5 min max
    let gameComplete = false;
    
    while (Date.now() - startTime < timeout) {
      const modal = page.locator('#gameModal:not(.hidden) .modal-content');
      if (await modal.count() > 0) {
        const text = await modal.textContent();
        // Final scoring - we're done
        if (/FINAL|RANKINGS|WINNER/i.test(text || '')) {
          gameComplete = true;
          break;
        }
        // Conquest or war modal - click Continue
        const continueBtn = page.locator('button:has-text("Continue to War"), button:has-text("Continue to Age"), button:has-text("Proceed to Final Scoring")');
        if (await continueBtn.count() > 0) {
          await continueBtn.first().click();
          await page.waitForTimeout(500);
        }
      }
      await page.waitForTimeout(1000);
    }
    
    expect(gameComplete).toBe(true);
    const modalText = await page.locator('.modal-content').textContent();
    expect(modalText).toMatch(/FINAL|RANKINGS|WINNER|Culture|civilization/i);
  });

  test('human + AI: place card and activate manual ability', async ({ page }) => {
    await page.goto(`file:///${HTML_PATH.replace(/\\/g, '/')}`);
    
    await page.waitForSelector('#playerSetup', { timeout: 5000 });
    
    // Player 1 = Human, Player 2 = AI
    const playerTypes = await page.locator('.player-type');
    await playerTypes.nth(0).selectOption('human');
    await playerTypes.nth(1).selectOption('ai-hard');
    
    const aiThinkingSelect = page.locator('select#aiThinkingTime');
    if (await aiThinkingSelect.count() > 0) {
      await aiThinkingSelect.selectOption('3');
    }
    
    await page.click('button:has-text("Start Game")');
    await page.waitForSelector('.game-board.active', { timeout: 5000 });
    
    // Wait for place phase - human player's turn
    await page.waitForTimeout(2000);
    
    // Click a random card in hand (human player)
    const handCards = page.locator('.hand .card:not(.passed-card)');
    const handCount = await handCards.count();
    if (handCount > 0) {
      const randomIdx = Math.floor(Math.random() * handCount);
      await handCards.nth(randomIdx).click();
      await page.waitForTimeout(500);
    }
    
    // Advance phase - click Next Phase if visible
    const nextPhaseBtn = page.locator('button:has-text("Next Phase"), button:has-text("Reveal")');
    if (await nextPhaseBtn.count() > 0) {
      await nextPhaseBtn.first().click();
      await page.waitForTimeout(2000);
    }
    
    // Activate phase - try to click a random manual ability button (⚡)
    const activateBtns = page.locator('button.card-activate-btn, button:has-text("⚡")');
    const activateCount = await activateBtns.count();
    if (activateCount > 0) {
      const randomActivateIdx = Math.floor(Math.random() * activateCount);
      await activateBtns.nth(randomActivateIdx).click();
      await page.waitForTimeout(1000);
    }
    
    // Game should still be responsive (no crash)
    await expect(page.locator('.game-board.active').first()).toBeVisible();
  });
});
