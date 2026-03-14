# Civilisations of the Middle Seas – Implementation Plan

**Status review date:** March 2026  
**Main file:** `CIV 5.html` (~7000 lines)

---

## Executive Summary

| Category | Status | Notes |
|----------|--------|------|
| Base game cards (114) | ✅ Implemented | All effects and triggers wired |
| Expansions (4) | ✅ Implemented | 45 cards + 8 civs (thematic, not from PDF) |
| Condition system | ✅ Fixed | `effect.conditions` in use |
| Triggers | ✅ Implemented | All 6 documented triggers exist |
| Known bugs | ⚠️ To verify | See testing section |
| Automated tests | ❌ None | Manual testing only |
| Future features | 📋 Documented | Save/load, undo, etc. |

---

## 1. Current Implementation Status

### 1.1 Core Features (Complete)
- [x] 114 base game cards with full effect logic
- [x] 6 civilizations with age-start bonuses
- [x] All triggers: `ownCardRuined`, `anyCardRuined`, `winConquestOrWar`, `warResult`, `anyResourceUsed`, `warPhase`
- [x] All placeholder effects: swapCultureMilitary, swapMilitaryWithOpponent, sacrificeAndBoostType, sacrificeAndBoostTypeCulture, doubleAdjacentCard, addCultureFromAgeGold, peaceBonus, swapWithOpponent, replaceFromDiscard, stealOpponentCard, controlRandom, wildType
- [x] Masada immune-while-tapped
- [x] Condition checking (hasType, countType, opponentLacksType)
- [x] 4 expansions with thematic cards and civilizations

### 1.2 Potential Issues to Verify
1. **addCultureToTypes parsing** – Effect `addCultureToTypes:a,c:2` (Great Owl): Parser must split `a,c` and `2` correctly. Base game uses `addCultureToTypes:c,a:1` – verify comma handling.
2. **Eagle Legion** – `trigger:winConquestOrWar,effect:addMilitary:2` adds military to the triggering card; ensure cardIndex is passed correctly for reactive triggers.
3. **Human choice for controlRandom/wildType** – AI picks; human players get no modal for choosing. Low priority.

### 1.3 Expansion Cards from PDF
- Expansion PDFs (`EXPANSIONS/*.pdf`) are image-only; OCR was not run successfully.
- Current expansion cards are thematic placeholders. To align with PDF content:
  - Install Tesseract OCR
  - Run `ocr_expansions.py` (or equivalent)
  - Parse output and update expansion card definitions

---

## 2. Bug Verification Checklist

### 2.1 High Priority
| Bug | Location | Verification |
|-----|----------|--------------|
| Conditions not enforced | `manuallyActivateCard` | ✅ Fixed: uses `effect.conditions` |
| checkCondition wrong parsing | `checkCondition()` | ✅ Fixed: uses `cond.type` |
| UIManager timerManager ref | `showModal` | Check: `this.game?.timerManager` |
| Masada ruin immunity | All ruin paths | Verify tapped Masada is excluded |

### 2.2 Medium Priority
| Bug | Description |
|-----|-------------|
| Double conquest culture | Verify conquest culture is doubled at correct phase |
| stealOpponentCard timing | Must only be activatable when `player.wonWarThisPhase` |
| replaceFromDiscard | Discard pile populated at dealAge; verify correct age is used |
| winAddCulture/loseAddCulture | Great Lament – cardIndex must be passed to addCulture |

### 2.3 Edge Cases
- 12 players: UI and performance
- All players pass: Game flow
- Zero military conquest: No winner, no culture
- Tied conquest/war: winTies handling

---

## 3. Testing Plan

### 3.1 Manual Test Matrix
| Test | Steps | Expected |
|------|-------|----------|
| Full game flow | 2 AI, all 3 ages | No console errors, victory screen |
| Condition gate | Play card with condition (e.g. countType:h:2), fail condition | "Conditions not met" |
| Condition pass | Meet condition, activate | Effect runs, card taps |
| Reactive triggers | Play Spearmen, opponent plays Chariots | Both gain military |
| War declared | Have Watchtower, get attacked | Military boost, Watchtower taps |
| Conquest winner | Win conquest with Spoils of War | +4 gold |
| War winner | Win war with Spoils of War | +4 gold |
| Peace bonus | No war with Pax Romana | +2 culture to card |
| Masada | Tap Masada, get attacked | Masada not ruined |
| Mithridates | Win war, activate | Steal card or "must win war" message |
| replaceFromDiscard | Activate Crassus | Replace with discard card |
| Expansion load | Check expansion, start game | Expansion cards in deck |

### 3.2 Automated Testing (Future)
- No unit tests exist. Options:
  - **Option A:** Playwright/Puppeteer for full-game automation
  - **Option B:** Extract core logic into testable modules + Jest
  - **Option C:** Add `window.runTestScenario(name)` hooks for critical flows

### 3.3 Console Monitoring
During play, watch for:
- `Unknown effect type:`
- `Unknown condition:`
- `Error in`
- Uncaught exceptions

---

## 4. Remaining Features (from FUTURE_FEATURES / DEVELOPMENT)

### 4.1 High Value
| Feature | Effort | Notes |
|---------|--------|------|
| Save/Load game | Medium | localStorage or export JSON |
| Undo last action | High | Requires state snapshots |
| Human choice for controlRandom | Low | Modal when ruining with Graeae |
| Human choice for wildType | Low | Modal for type selection |

### 4.2 Medium Value
| Feature | Effort |
|---------|--------|
| Sound effects | Low |
| Animated card effects | Medium |
| Statistics tracking | Low |
| Customizable themes | Low |

### 4.3 Lower Priority
- Network multiplayer (WebRTC)
- Campaign mode
- Achievements
- Draft civilization mode

---

## 5. Implementation Priority Order

### Phase 1: Verification & Bug Fixes (1–2 days)
1. Run manual test matrix; log all failures.
2. Fix any condition or effect parsing bugs found.
3. Verify Masada, Mithridates, replaceFromDiscard, winConquestOrWar.
4. Update `CARD_IMPLEMENTATION_GUIDE.md` to match current state.

### Phase 2: Polish & Edge Cases (1 day)
1. Add human choice modals for controlRandom and wildType.
2. Harden edge cases (all pass, 12 players, ties).
3. Improve AI evaluation for new effects in `evaluateManualAbility()`.

### Phase 3: Future Features (as needed)
1. Save/Load to localStorage.
2. Undo (optional, complex).
3. Automated regression tests.

---

## 6. File Reference

| File | Purpose |
|------|---------|
| `CIV 5.html` | Main game – all logic, UI, cards |
| `CARD_IMPLEMENTATION_GUIDE.md` | Effect/trigger reference (outdated in places) |
| `GAME_RULES.md` | Player-facing rules |
| `DEVELOPMENT.md` | Architecture overview |
| `EXPANSIONS/README.md` | OCR instructions for expansion PDFs |

---

## 7. Quick Start for Test Run

1. Open `CIV 5.html` in browser.
2. Add 2 players, both Hard AI.
3. Start game, let it run to completion.
4. Open DevTools console (F12) and review for errors.
5. Repeat with 1 human + 1 AI to test manual abilities.
