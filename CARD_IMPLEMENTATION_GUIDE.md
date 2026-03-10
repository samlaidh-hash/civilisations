# Card Implementation Guide for Composer 1.5

## Overview

The game "Civilisations of the Middle Seas" now has all 114 cards from the PDF (`20210608_CIVILISATIONS_FINAl_X-1a - Copy.pdf`) added to the card database (38 per age). However, many cards have **placeholder effects** — their base stats (cost, type, culture, military, resources) are correct, but their special abilities need actual game logic implemented in the EffectEngine.

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

## BUG: Condition Checking is Broken (Fix First!)

The condition system parses correctly but is **never actually checked** due to a property name mismatch:

**In `manuallyActivateCard()` (~line 4447):**
```javascript
// BUG: checks effect.condition (singular) but conditions are stored as effect.conditions (plural)
if (effect.condition && !this.checkCondition(player, effect.condition, gameState)) {
```

**Fix:** Change `effect.condition` to `effect.conditions`:
```javascript
if (effect.conditions && !this.checkCondition(player, effect.conditions, gameState)) {
```

Additionally, `checkCondition()` re-parses `cond.value` to extract the condition type, but the type is already in `cond.type`. The function at ~line 4750 does:
```javascript
const [condType, ...params] = cond.value.split(':');
```

But since `cond` is `{type: "hasType", value: "i"}`, `condType` becomes `"i"` instead of `"hasType"`. 

**Fix:** Change to use `cond.type`:
```javascript
checkCondition(player, conditions, gameState) {
    if (!conditions) return true;
    for (let cond of conditions) {
        switch (cond.type) {
            case 'hasType':
                if (!this.hasCardType(player, cond.value)) return false;
                break;
            case 'countType': {
                const [cardType, required] = cond.value.split(':');
                if (this.countCardType(player, cardType) < parseInt(required)) return false;
                break;
            }
            case 'opponentLacksType':
                if (this.anyOpponentHasType(player, cond.value, gameState)) return false;
                break;
            default:
                console.warn(`Unknown condition: ${cond.type}`);
                return false;
        }
    }
    return true;
}
```

**WARNING**: Fixing this will mean conditions are actually enforced. Test to make sure abilities still activate when conditions are met.

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

---

## PLACEHOLDER Effects (Need Real Implementation)

These effects currently just show a notification but do nothing:

### 1. `controlRandom` — The Graeae (Age II)
**Card**: "When a random choice is called for by a card you may instead choose the result, then TAP"
**Implementation**: Set a flag `player.controlRandom = true`. When any random effect runs (like `ruinRandomOpponentCard`), if this flag is set, let the player choose the target instead of randomizing. Clear the flag after use.

### 2. `wildType` — The Oracle at Delphi (Age II)
**Card**: "This card can be counted as a card of any type once, then TAP"
**Implementation**: When activated, prompt for or auto-select the most beneficial type. Temporarily add that type to the player's type counts for condition checks. Works with `hasType` and `countType` conditions.

### 3. `swapWithOpponent` — Bad Deal (Age II), Spy (Age II)
**Card (Bad Deal)**: "Swap this card with another player's random Trade or Economic card, then TAP"
**Card (Spy)**: "Swap this card with a random card of another player, then TAP"
**Implementation**: Find a valid opponent card, remove it from their tableau, place it in yours, move this card to their tableau. Update both players' stats. Bad Deal targets specific types (t,e); Spy targets any card.

### 4. `replaceFromDiscard` — Crassus (Age II), Spurinna the Haruspex (Age III)
**Card**: "Look at the discarded hand for this Age and replace this card with a card of your choice"
**Implementation**: Access the discarded hand (cards not drafted this age). Show a selection UI or auto-pick the best card. Replace this card in the tableau. Treat the new card as just played (activate its effects).

### 5. `stealOpponentCard` — Mithridates (Age I)
**Card**: "If you win a War you may choose a card from any opponent's Ages, then TAP"
**Implementation**: After winning a war, let the player (or AI) pick an opponent card. Move it to their tableau. This requires integration with the war phase results.

### 6. `swapCultureMilitary` — Seneca the Younger (Age III)
**Card**: "Switch the culture and military tokens on your card with the most culture, then TAP"
**Implementation**: Find the player's card with the highest `bonusCulture`. Swap its `bonusCulture` and `bonusMilitary` values. Call `updatePlayerStats()`.

### 7. `swapMilitaryWithOpponent` — Menippean Satire (Age III)
**Card**: "Swap this card's military with military from a random other player's card with military, then TAP"
**Implementation**: Find a random opponent card that has military (base + bonus > 0). Swap the `bonusMilitary` values between this card and the opponent's card. Update both players.

### 8. `sacrificeAndBoostType` — Temple of Ares (Age III)
**Card**: "RUIN one of your cards of your choice to add 2 military to each other of your cards of the same Type, then TAP"
**Implementation**: Auto-select (or prompt) a card to sacrifice. RUIN it. Find all other cards of the same type. Add 2 `bonusMilitary` to each. For AI: sacrifice the card with lowest value.

### 9. `sacrificeAndBoostTypeCulture` — Theatre of Dionysus (Age III)
**Card**: Same as above but adds culture instead of military.
**Implementation**: Same as `sacrificeAndBoostType` but add to `bonusCulture`.

### 10. `doubleAdjacentCard` — Divine Blessing (Age II)
**Card**: "Double the culture and military tokens on the card to the right of this card, then TAP"
**Implementation**: Find this card's index in the tableau. Get the card at index+1 (or wrap to next round). Double its `bonusCulture` and `bonusMilitary`.

### 11. `addCultureFromAgeGold` — Temple of Mercury (Age III)
**Card**: "Add 1 culture per gold gained at start of current Age (not from starting value), then TAP"
**Implementation**: Track gold gained from card effects during age start (`goldPerAge`, `goldOnThirdAge`, `gambling`). Store this as `player.ageStartGoldFromCards`. Add that count as `bonusCulture` to this card.

### 12. `peaceBonus` — Pax Romana (Age I)
**Card**: "If you do not engage in a War during a War phase, add 2 culture to this card"
**Implementation**: After the war phase, check if this player was NOT involved in any war (neither attacking nor defending). If peaceful, add 2 to this card's `bonusCulture`. This needs a hook in `handleWarPhase()`.

---

## UNIMPLEMENTED Triggers (Need New Trigger Handlers)

These trigger types appear in card effect strings but have no handler code:

### 1. `trigger:warResult` — Great Lament (Age I)
**Effect string**: `"trigger:warResult,effect:winAddCulture:1,loseAddCulture:2"`
**Needs**: A new trigger handler in `handleWarPhase()` that fires after each war. If the player won, add culture; if they lost, add more culture.
**New effect types needed**: `winAddCulture:X`, `loseAddCulture:X`

### 2. `trigger:anyResourceUsed` — Customs House (Age I)
**Effect string**: `"culture:1,trigger:anyResourceUsed,effect:gainGold:1"`
**Needs**: A hook in `calculateCardCost()` or during the reveal/payment phase. When ANY player uses resources to reduce a card's cost, trigger this effect for the Customs House owner.

### 3. `trigger:ownCardRuined` — The Black Legion (Age I)
**Effect string**: `"military:3,culture:1,trigger:ownCardRuined,effect:addMilitary:2"`
**Needs**: A hook wherever cards are ruined (war phase, opponent effects). When one of this player's cards is ruined, add 2 military to The Black Legion.

### 4. `trigger:anyCardRuined` — Mausoleum of Halicarnassus (Age I)
**Effect string**: `"culture:2,trigger:anyCardRuined,effect:addCulture:2"`
**Needs**: Same hook location as above, but triggers when ANY card (any player's) is ruined.

### 5. `trigger:winConquestOrWar` — Spoils of War (Age I)
**Effect string**: `"trigger:winConquestOrWar,effect:gainGold:4"`
**Needs**: Hooks in both `handleConquestPhase()` and `handleWarPhase()`. When this player wins a conquest or war, gain 4 gold.

### 6. `trigger:warPhase` — Pax Romana (Age I)
**Effect string**: `"culture:2,trigger:warPhase,effect:peaceBonus:2"`
**Needs**: A hook at the end of `handleWarPhase()`. If this player did NOT participate in war, add 2 culture to this card.

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
