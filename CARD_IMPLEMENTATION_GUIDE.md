# Card Implementation Guide for Composer 1.5

## Overview

The game "Civilisations of the Middle Seas" has all 114 base game cards plus 45 expansion cards fully implemented. **All effects and triggers are implemented** — base stats (cost, type, culture, military, resources) and special abilities have complete game logic in the EffectEngine.

**File to edit**: `CIV 5.html` (single-file game, ~6600 lines)

---

## Architecture Quick Reference

| Class | Purpose | Approx Line |
|-------|---------|-------------|
| `CardDatabase.initializeCards()` | Card definitions | ~3604 |
| `EffectEngine` | All effect logic | ~4390 |
| `EffectEngine.parseEffectString()` | Parses effect strings | ~4490 |
| `EffectEngine.executeEffect()` | Main effect switch | ~4670 |
| `EffectEngine.checkCondition()` | Condition checking | ~4750 |
| `EffectEngine.manuallyActivateCard()` | Manual ability flow | ~4425 |
| `EffectEngine.triggerAgeStart()` | Age-start triggers | ~5190 |
| `EffectEngine.triggerEndOfAge()` | End-of-age triggers | ~5230 |
| `EffectEngine.triggerReactiveEffects()` | Card-played triggers | ~5270 |
| `EffectEngine.triggerWarDeclaredEffects()` | War triggers | ~5340 |
| `GameEngine.calculateCardCost()` | Cost reduction | ~3565 |
| `GameEngine.updatePlayerStats()` | Stat recalculation | ~3540 |
| `GameEngine.endGame()` | Final scoring | ~3435 |
| `GameEngine.handleConquestPhase()` | Conquest logic | ~2990 |
| `GameEngine.handleWarPhase()` | War logic | ~3090 |

---

## Condition System (FIXED — Complete)

The condition system uses `effect.conditions` and `checkCondition()` correctly. Conditions `hasType`, `countType`, and `opponentLacksType` are enforced before manual abilities activate. Unknown conditions log only when `window.DEBUG_CIV_GAME` is set.

---

## Effect String Format

```
"immediate:value,immediate:value,trigger:type,condition:condType:value,effect:action:value,tap"
```

**Parser rules:**
- Commas inside `effect:` and `trigger:` values are treated as part of the value (not separators)
- Commas after other keys (like `condition:`, `culture:`) ARE separators
- `tap` at the end of an `effect:` value gets extracted automatically
- For non-trigger/non-effect keys that need multi-character type lists, concatenate single chars (e.g., `reduceCostType:nrim` NOT `reduceCostType:n,r,i,m`)

---

## Fully Implemented Effect Types

These work correctly in `executeEffect()`:

| Effect | Description | Example |
|--------|-------------|---------|
| `goldOnPlay:X` | Gain X gold when played | `goldOnPlay:3` |
| `goldPerAge:X` | Gain X gold at age start | `goldPerAge:1` |
| `goldOnThirdAge:X` | Gain X gold at Age III start only | `goldOnThirdAge:9` |
| `goldOnPass:X` | Gain X gold when passing | `goldOnPass:3` |
| `resource:X` | Add resource to player pool | `resource:f` |
| `military:X` | Base military stat | `military:3` |
| `culture:X` | Base culture stat | `culture:2` |
| `tap` | Tap the card | `tap` |
| `gainGold:X` | Gain gold (in manual effects) | `gainGold:2` |
| `nextCardFree` | Next card costs 0 | `nextCardFree` |
| `addMilitary:X` | Add bonus military to THIS card | `addMilitary:2` |
| `addMilitaryPerType:T:X` | Add X military per card of type T | `addMilitaryPerType:i:2` |
| `addMilitaryToTypes:T1,T2:X` | Add X military to ALL cards of types | `addMilitaryToTypes:i,m,r:1` |
| `addCulture:X` | Add bonus culture to THIS card | `addCulture:3` |
| `addCultureToTypes:T1,T2:X` | Add X culture to ALL cards of types | `addCultureToTypes:c,a:1` |
| `addCulturePerType:T:X` | Add X culture per card of type T (to this card) | `addCulturePerType:h:1` |
| `ruinSelf` | RUIN this card | `ruinSelf` |
| `ruinRandomOpponentCard` | RUIN random opponent card | `ruinRandomOpponentCard` |
| `ruinOpponentType:T` | RUIN random opponent card of type T | `ruinOpponentType:n` |
| `ruinHighCultureOpponentCard` | RUIN opponent card with most culture | `ruinHighCultureOpponentCard` |
| `doubleConquestCulture` | Double conquest culture earned | `doubleConquestCulture` |
| `enablesFree:Name` | Named card costs 0 to play | `enablesFree:Bowmen` |
| `reduceCostType:types` | Reduce cost of card types by 1 | `reduceCostType:nrim` |
| `gainGoldPerType:T:X` | Gain X gold per card of type T | `gainGoldPerType:e:2` |
| `gainGoldPerOpponentType:T:X` | Gain X gold per opponent's type T cards | `gainGoldPerOpponentType:e:3` |
| `gainGoldPerChosenResource:X` | Gain X gold per best resource count | `gainGoldPerChosenResource:3` |
| `stealCulture:X` | Steal X culture from random opponent | `stealCulture:4` |
| `convertMilitaryToCulture:X` | Convert X military to X culture on each card | `convertMilitaryToCulture:1` |
| `addCulturePerUniqueType` | +1 culture per unique card type in play | `addCulturePerUniqueType` |
| `spendForMilitary:cost:bonus` | Spend gold for military | `spendForMilitary:3:2` |
| `spendForCulture:cost:bonus` | Spend gold for culture | `spendForCulture:3:2` |
| `removeAllCulture:X` | Remove X culture from each of your cards | `removeAllCulture:1` |
| `unruinCard` | UNRUIN a random ruined card | `unruinCard` |
| `reuseRandomTapped` | Untap a random card, use its ability, re-tap | `reuseRandomTapped` |
| `shieldFromEffect` | Shield from next opponent effect | `shieldFromEffect` |
| `winTies` | Win conquest/war ties (immediate) | `winTies` |
| `gambling:W:L:C` | Age start: C/6 chance of W gold, else L | `gambling:6:2:4` |
| `endGameBonus:X` | Add X culture at end of game | `endGameBonus:10` |
| `endGameGambling:W:L:C` | End of game: C/6 chance of W gold, else L | `endGameGambling:8:0:4` |

## Fully Implemented Triggers

| Trigger | When it fires | Handler location |
|---------|--------------|-----------------|
| *(none)* | Immediately on play | `activateCard()` |
| `manual` | Player clicks ⚡ button | `manuallyActivateCard()` |
| `endOfAge` | End of each age (conquest phase) | `triggerEndOfAge()` |
| `playCardType:T` | When YOU play card of type T | `triggerReactiveEffects()` |
| `otherPlayerPlaysType:T` | When OPPONENT plays type T | `triggerReactiveEffects()` |
| `anyPlayerPlaysType:T` | When ANY player plays type T | `triggerReactiveEffects()` |
| `warDeclared` | When you are attacked in war | `triggerWarDeclaredEffects()` |
| `warResult` | After each war (won/lost) | `triggerWarResult()` |
| `anyResourceUsed` | When any player uses resources for cost | `triggerAnyResourceUsed()` |
| `ownCardRuined` | When your card is ruined | `triggerOwnCardRuined()` |
| `anyCardRuined` | When any card is ruined | `triggerAnyCardRuined()` |
| `winConquestOrWar` | When you win conquest or war | `triggerWinConquestOrWar()` |
| `warPhase` | End of war phase (peace bonus) | `triggerWarPhasePeaceBonus()` |

---

## All Effects and Triggers — Implementation Complete ✅

All previously listed placeholder effects and unimplemented triggers are now fully implemented:

**Effect types**: `controlRandom`, `wildType`, `swapWithOpponent`, `replaceFromDiscard`, `stealOpponentCard`, `swapCultureMilitary`, `swapMilitaryWithOpponent`, `sacrificeAndBoostType`, `sacrificeAndBoostTypeCulture`, `doubleAdjacentCard`, `addCultureFromAgeGold`, `peaceBonus`, `winAddCulture`, `loseAddCulture`

**Triggers**: `trigger:warResult` (Great Lament), `trigger:anyResourceUsed` (Customs House), `trigger:ownCardRuined`, `trigger:anyCardRuined`, `trigger:winConquestOrWar`, `trigger:warPhase` (Pax Romana peace bonus)

**Masada**: Immune to ruin while tapped — excluded from ruin targets in war phase, ruinRandomOpponentCard, ruinOpponentType, ruinHighCultureOpponentCard.

---

## How to Add a New Trigger Handler

Here's the pattern for adding trigger support. Example: implementing `trigger:ownCardRuined`:

### Step 1: Create the trigger method in EffectEngine

```javascript
triggerOwnCardRuined(player, ruinedCardIndex, gameState) {
    player.tableau.forEach((card, cardIndex) => {
        if (!card || player.ruinedCards.has(cardIndex)) return;
        if (!card.effect || !card.effect.includes('trigger:ownCardRuined')) return;
        
        const effects = this.parseEffectString(card.effect);
        const matchingEffects = effects.filter(e => e.trigger === 'ownCardRuined');
        
        matchingEffects.forEach(effect => {
            if (effect.effects) {
                effect.effects.forEach(triggerEffect => {
                    this.executeEffect(player, triggerEffect, cardIndex, gameState);
                });
            }
        });
        
        this.game.showNotification(`${player.name}'s ${card.name} triggers!`);
        this.game.updatePlayerStats(player);
    });
}
```

### Step 2: Call it wherever cards are ruined

In `ruinRandomOpponentCard()`, `ruinOpponentType()`, `ruinHighCultureOpponentCard()`, and the war phase:

```javascript
target.ruinedCards.add(targetIndex);
// Add this line after ruining:
this.triggerOwnCardRuined(target, targetIndex, gameState);
// For anyCardRuined, also check all other players:
gameState.players.forEach(p => this.triggerAnyCardRuined(p, target, targetIndex, gameState));
```

---

## How to Implement a Placeholder Effect

Example: implementing `swapCultureMilitary` for Seneca the Younger:

### Step 1: Find the placeholder in executeEffect()

Search for `case 'swapCultureMilitary':` (around line ~5012).

### Step 2: Replace the placeholder with real logic

```javascript
case 'swapCultureMilitary': {
    let bestIdx = -1, bestCulture = -1;
    player.tableau.forEach((c, idx) => {
        if (c && !player.ruinedCards.has(idx)) {
            const cul = (c.bonusCulture || 0);
            if (cul > bestCulture) { bestCulture = cul; bestIdx = idx; }
        }
    });
    if (bestIdx >= 0) {
        const card = player.tableau[bestIdx];
        const tempCulture = card.bonusCulture || 0;
        card.bonusCulture = card.bonusMilitary || 0;
        card.bonusMilitary = tempCulture;
        this.game.updatePlayerStats(player);
        this.game.showNotification(`${player.name} swaps culture/military on ${card.name}!`);
    }
    return true;
}
```

### Step 3: Test

Start a game with AI players. If the card appears and gets activated, check the console for proper logging.

---

## Card Data Reference

Each card object has this structure:
```javascript
{
    name: "Card Name",       // Display name
    cost: 3,                 // Gold cost to play
    type: "c",               // Single-char card type (see table above)
    culture: 2,              // Base culture value
    military: 0,             // Base military value
    resources: ["s", "k"],   // Resource icons (reduce cost of future cards with matching resources)
    ability: "Description",  // Human-readable ability text shown on card
    effect: "effect:string"  // Machine-readable effect string (parsed by EffectEngine)
}
```

**Important notes about resources:**
- The `resources` array determines which resource icons show on the card
- When playing a card, each resource the player already has in their pool reduces cost by 1
- Economic cards typically add resources to the player's pool via `resource:X` in the effect string
- Non-economic cards have resources for cost reduction only (they don't add to the pool)

**Important notes about bonusCulture/bonusMilitary:**
- `card.culture` and `card.military` are the BASE stats (from the card definition)
- `card.bonusCulture` and `card.bonusMilitary` are BONUS tokens added by effects
- `updatePlayerStats()` sums both: `(card.culture || 0) + (card.bonusCulture || 0)`
- Always modify `bonusCulture`/`bonusMilitary` for runtime changes, never the base stats

---

## Effect String Parsing Details

The parser handles comma-separated values inside `effect:` and `trigger:` keys by looking ahead. For other keys, commas are always separators. 

**Safe patterns:**
```
"culture:2,trigger:manual,effect:addCulture:3,tap"           ✅
"military:3,trigger:manual,effect:addMilitaryToTypes:i,m:2,tap"  ✅ (commas inside effect value)
"culture:1,reduceCostType:nrim"                               ✅ (no commas in value)
```

**Broken patterns (don't use):**
```
"culture:1,reduceCostType:n,r,i,m"    ❌ (commas parsed as separators, "r","i","m" become unknown effects)
```

**Workaround**: For multi-type values outside of `effect:`/`trigger:`, concatenate single-char codes without commas: `reduceCostType:nrim`.

---

## Testing Checklist

After implementing any effect:

1. Start an AI-only game (2 Hard AI players, Fast thinking time)
2. Let it run through all 3 ages
3. Check browser console for:
   - `Unknown effect type:` errors
   - `Error in` messages
   - JavaScript exceptions
4. Verify the new effect appears in game log when triggered
5. Test with a human player to verify the ⚡ activation button works for manual abilities
6. Test that conditions properly gate the ability (after fixing the condition bug)

---

## Priority Order for Implementation

### High Priority (affects many games)
1. **Fix condition checking bug** (affects ALL conditional manual abilities)
2. **`trigger:ownCardRuined`** — The Black Legion is a strong Age I card
3. **`trigger:anyCardRuined`** — Mausoleum of Halicarnassus
4. **`trigger:winConquestOrWar`** — Spoils of War affects economy
5. **`peaceBonus`** — Pax Romana is a key strategy card

### Medium Priority (complex but important)
6. **`swapCultureMilitary`** — Seneca the Younger
7. **`sacrificeAndBoostType`** — Temple of Ares
8. **`sacrificeAndBoostTypeCulture`** — Theatre of Dionysus  
9. **`doubleAdjacentCard`** — Divine Blessing
10. **`addCultureFromAgeGold`** — Temple of Mercury

### Lower Priority (complex interactions)
11. **`swapWithOpponent`** — Bad Deal, Spy (card movement between players)
12. **`replaceFromDiscard`** — Crassus, Spurinna (discard pile interaction)
13. **`stealOpponentCard`** — Mithridates (post-war card theft)
14. **`swapMilitaryWithOpponent`** — Menippean Satire
15. **`controlRandom`** — The Graeae (override randomness)
16. **`wildType`** — The Oracle at Delphi (type wildcarding)
17. **`trigger:anyResourceUsed`** — Customs House
18. **`trigger:warResult`** — Great Lament
19. **`trigger:warPhase`** — Pax Romana (overlaps with peaceBonus)

---

## Masada Special Rule

The card "Masada" (Age II, Holy) has a special rule: "Whilst TAPPED this card cannot be RUINED." This is not currently implemented. To implement:

- In every place where a card is ruined (war phase, `ruinRandomOpponentCard`, `ruinOpponentType`, etc.), check:
```javascript
// Skip cards that are immune while tapped (Masada)
if (player.tappedCards.has(cardIndex) && card.name === 'Masada') continue;
```

Or better, add an `immuneWhileTapped` flag:
```javascript
if (player.tappedCards.has(cardIndex) && card.immuneWhileTapped) continue;
```

---

## AI Considerations

When implementing new effects, also update the AI evaluation in `AIManager.evaluateManualAbility()` (around line 1847) so the AI knows when to activate new ability types. Currently it uses simple heuristics:
- Gold-generating abilities: always activate
- Military bonuses: activate if competing for conquest
- Any other manual ability: activate if not tapped

For complex new effects (swapping cards, sacrificing), add specific AI logic to evaluate whether activation is beneficial.
