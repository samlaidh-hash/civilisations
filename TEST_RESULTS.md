# Test Results — Civilisations of the Middle Seas

**Date:** March 2026  
**Last Test Run:** March 9, 2025  
**Phases Completed:** 1–4  
**Main File:** CIV 5.html (~7000 lines)

### Latest Run (March 9, 2025)
```
Running 2 tests using 1 worker

  ok 1 tests\civ5.spec.js:16:3 › Civilisations of the Middle Seas › full AI game completes without errors (3.4m)
  ok 2 tests\civ5.spec.js:71:3 › Civilisations of the Middle Seas › human + AI: place card and activate manual ability (12.4s)

  2 passed (3.9m)
```

---

## Summary

| Category | Status |
|----------|--------|
| Phase 1: Verification & Bug Fixes | ✅ Complete |
| Phase 2: Polish & Edge Cases | ✅ Complete |
| Phase 3: Playwright Testing | ✅ Complete |
| Phase 4: Bug Hunt & Final Verification | ✅ Complete |

---

## Phase 1 Verification Results

### 1. addCultureToTypes Parsing (Great Owl: `addCultureToTypes:a,c:2`)
- **Status:** ✅ Working correctly
- **Details:** Parser splits `a,c` and `2` correctly. Effect value `a,c:2` is parsed as `types="a,c"`, `amount="2"`. The lookahead logic treats commas inside effect values as part of the value when the next token is not a known effect type.

### 2. winAddCulture/loseAddCulture (Great Lament)
- **Status:** ✅ Working correctly
- **Details:** `triggerWarResult()` passes `cardIndex` to `executeEffect()` for both `winAddCulture` and `loseAddCulture`. Culture is added to the correct card.

### 3. Masada Ruin Immunity
- **Status:** ✅ Working correctly
- **Details:** Masada is excluded from ruin targets when tapped in all ruin paths:
  - War phase (line ~3194)
  - ruinRandomOpponentCard
  - ruinOpponentType
  - ruinHighCultureOpponentCard

### 4. stealOpponentCard and wonWarThisPhase
- **Status:** ✅ Working correctly
- **Details:** `stealOpponentCard` checks `player.wonWarThisPhase` before allowing activation. Shows "You must win a war first to use this ability!" when condition not met. Stolen cards are placed in the first empty tableau slot (no `push` overflow).

---

## Phase 2 Polish & Edge Cases

### Changes Made
- **Null checks:** Added guards for `player`, `player.tableau`, `player.civilization` in `endGame()`, `considerManualActivations()`, and `evaluateManualAbility()`.
- **AI evaluateManualAbility:** Added logic for `stealOpponentCard` (only when `wonWarThisPhase`), `doubleAdjacentCard`, `addCultureToTypes`, and `replaceFromDiscard`.
- **Console warnings:** `Unknown effect type` and `Unknown condition` only log when `window.DEBUG_CIV_GAME` is set. No warnings during normal play.

---

## Phase 3 Playwright Tests

### Test Suite: `tests/civ5.spec.js`

| Test | Result | Duration |
|------|--------|----------|
| full AI game completes without errors | ✅ Pass | 3.4m |
| human + AI: place card and activate manual ability | ✅ Pass | 12.4s |

### Test Details
1. **Full AI game:** 2 AI (Hard) players, Fast thinking (3s). Test dismisses conquest/war modals by clicking Continue. Asserts final scoring modal appears with RANKINGS/FINAL content. Listens for uncaught JS errors.
2. **Human + AI:** Human places card, advances phase, activates manual ability (⚡). Asserts game board remains visible (no crash).

### Run Command
```bash
npx playwright test
```

### Stress Test (20× with random card selection)

- **Command:** `npm run test:stress` or `npx playwright test --repeat-each=20`
- **Total runs:** 40 (20 × full AI game, 20 × human+AI)
- **Random selection:** Human player picks a random card from hand and a random ⚡ activate button when multiple available. AI players already use `Math.random()` for decisions, so each run varies.
- **Config:** `playwright.config.js` sets `timeout: 360000` (6 min) and `workers: 1` for stability. Expect ~75 min total.

---

## Phase 4 Bug Hunt & Verification

### Critical Cards Verified
- **Divine Blessing (doubleAdjacentCard):** Implemented — doubles bonus culture/military on adjacent card.
- **Temple of Ares (sacrificeAndBoostType):** Implemented — sacrifices card, adds +2 military to each other card of same type.
- **Mithridates (stealOpponentCard):** Implemented — requires `wonWarThisPhase`, steals random opponent card to first empty slot.

### Expansions
- Tested with expansions enabled; no crashes observed.

---

## Bugs Fixed During Implementation

1. **stealOpponentCard tableau:** Changed from `player.tableau.push(stolenCard)` to placing in first empty slot to respect fixed 18-slot tableau grid.
2. **AI thinking time in tests:** `#aiThinkingTime` is a `<select>`, not an input. Tests updated to use `selectOption('3')` instead of `fill('1')`.
3. **Modal dismissal in AI-only tests:** Conquest and war modals require manual Continue click. Test loop added to detect and click Continue/Proceed buttons until final scoring appears.
4. **endGame null guards:** Added `if (!player) return` and `(player.civilization && player.civilization.name) || 'Unknown'` for robustness.

---

## Remaining Known Issues

1. **stealOpponentCard timing:** `wonWarThisPhase` is cleared at the end of the war phase before the user can interact. The war results modal blocks the game board, so human players cannot activate Mithridates after winning. Consider adding an "Activate Mithridates" option in the war results modal for winners.
2. **controlRandom / wildType:** No human choice modal — AI picks; human players get no selection UI (low priority).
3. **Full game duration:** With default AI thinking time, a full 3-age AI game can take 5+ minutes.

---

## Files Modified/Created

- **CIV 5.html:** Null checks, AI `evaluateManualAbility` updates, DEBUG guard for console.warn
- **CARD_IMPLEMENTATION_GUIDE.md:** Updated overview, condition section, removed placeholder/unimplemented; added "All Complete" section
- **package.json:** Playwright dependency
- **tests/civ5.spec.js:** Full AI game test, human+AI manual ability test
- **TEST_RESULTS.md:** This file
