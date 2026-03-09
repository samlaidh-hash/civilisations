# Complete Game Rules - Civilisations of the Middle Seas

## Table of Contents
1. [Game Setup](#game-setup)
2. [Game Structure](#game-structure)
3. [Turn Phases](#turn-phases)
4. [Card Mechanics](#card-mechanics)
5. [Resources](#resources)
6. [Military & Combat](#military--combat)
7. [Scoring & Victory](#scoring--victory)
8. [Card Abilities](#card-abilities)
9. [Advanced Rules](#advanced-rules)

---

## Game Setup

### Player Configuration
- **Players**: 2-12 (human and/or AI)
- **AI Levels**: Easy (random affordable cards), Medium (basic strategy), Hard (optimized play)

### Choose Your Civilization

Each civilization provides unique starting bonuses:

| Civilization | Gold | Culture | Military | Special |
|-------------|------|---------|----------|---------|
| Rome | 7 | 0 | 0 | Reliable and balanced |
| Greece | 7 | 1 | 2 | Early military dominance |
| Egypt | 8 | 2 | 0 | Cultural head start |
| Persia | 8 | 1 | 1 | Wealthy and balanced |
| The Celts | 7 | 2 | 1 | Culture with defense |
| Carthage | 9 | 1 | 0 | Economic juggernaut |

**Important**: Civilization bonuses repeat at the start of each age!

---

## Game Structure

### Three Ages
- **Age I**: Foundations (basic cards, cost 2-3)
- **Age II**: Development (advanced cards, cost 2-4)
- **Age III**: Pinnacle (powerful cards, wonders, cost 2-9)

### Six Turns Per Age
- Each age consists of exactly 6 turns
- After turn 6: Conquest → War → Next Age (or game end)

### Total Game Length
- 18 turns total (6 per age × 3 ages)
- Plus 3 conquest/war phases (end of each age)
- Approximately 30-60 minutes depending on player count

---

## Turn Phases

### Phase 1: PLACE
**What Happens**:
- Each player secretly selects one card from their hand
- Click a card to place it (if affordable)
- Click "Pass" if you can't afford anything or want to save gold

**Passing**:
- Immediately gain 3 gold
- Don't play a card this turn
- Sometimes strategically optimal!

**Key Rules**:
- All players choose simultaneously
- Cannot see what others chose until Reveal phase
- Card costs displayed in gold circle (top-right)
- Resources reduce costs (see [Resources](#resources))

### Phase 2: REVEAL
**What Happens**:
- All placed cards are simultaneously revealed
- Gold is deducted from each player
- Cards are added to tableaus at the current turn position
- Passed players receive their 3 gold

**Tableau Layout**:
```
Age I:   [Turn 1] [Turn 2] [Turn 3] [Turn 4] [Turn 5] [Turn 6]
Age II:  [Turn 1] [Turn 2] [Turn 3] [Turn 4] [Turn 5] [Turn 6]
Age III: [Turn 1] [Turn 2] [Turn 3] [Turn 4] [Turn 5] [Turn 6]
```

### Phase 3: ACTIVATE
**What Happens**:
- All newly-played cards activate their immediate effects
- Effects include: gaining gold, adding resources, military/culture bonuses
- Automatic - no player input required

**Common Immediate Effects**:
- `goldOnPlay:X` - Gain X gold
- `resource:X` - Add resource type X to your pool
- `military:X` / `culture:X` - Add to totals (always active)

### Phases 4 & 5: CONQUEST & WAR (End of Age Only)

**After turn 6 of each age, two special phases occur:**

#### CONQUEST PHASE
- Player with highest military wins
- Ties: All tied players win
- Rewards:
  - Age I: 2 culture
  - Age II: 4 culture
  - Age III: 6 culture
- Tracked for "double conquest culture" abilities

#### WAR PHASE
- Aggressive players (2x opponent's military) may attack
- Target: Weakest opponent
- **If Defender Has Fortifications**: Attack fails
- **If No Fortifications**: Random card ruined, 2 culture lost
- Results displayed in war modal

---

## Card Mechanics

### Card Anatomy

```
┌─────────────┐
│ [Res][Cost] │  Top: Resources (left), Cost (right)
│             │
│    NAME     │  Card name
│             │
│   Ability   │  Card text/ability
│             │
│ [Cul][Mil]  │  Bottom: Culture/Military (left), Type (right)
│        [T]  │
└─────────────┘
```

### Card Properties

**Cost** (Gold circle, top-right):
- Gold required to play
- Reduced by matching resources (1 gold per match)
- Can be affected by card abilities

**Resources** (Icons, top-left):
- Reduce costs of future cards with matching resources
- Permanent once card is in play
- Not consumed - reusable every turn

**Culture** (Blue circle, bottom-left):
- Victory points
- Always active (unless card is ruined)
- Final score = total culture

**Military** (Red circle, bottom-left):
- Combat strength
- Used for Conquest and War
- Can be boosted by effects

**Type** (Icon, bottom-right):
- Card category (Economic, Military, Civic, etc.)
- Affects synergies and bonuses
- See [Card Types](#card-types)

### Card States

**Normal**: Face-up, can be used, counts for stats

**Tapped** (Rotated 45°):
- Used its manual ability this age
- Still counts for stats
- Cannot activate again until untapped
- Untaps at start of next age

**Ruined** (Grayed out):
- Destroyed by war or card effects
- Does NOT count for stats
- Permanent - cannot be repaired
- Remains visible but inactive

---

## Resources

### Resource Types

| Code | Name | Common Sources |
|------|------|----------------|
| **a** | Animals | Herding, domestication cards |
| **f** | Food | Irrigation, agriculture |
| **k** | Knowledge | Schools, libraries |
| **m** | Metal | Mining, smithing |
| **s** | Stone | Quarries, pit mines |
| **v** | Valuables | Gold mines, jewelers |
| **w** | Wood | Logging camps, forestry |

### How Resources Work

**Cost Reduction**:
1. Card shows required resources (top-left)
2. Each matching resource in your tableau reduces cost by 1
3. Example: Card costs 5, needs 2 Wood, you have 2 Wood → pay only 3 gold

**Accumulation**:
- Resources are permanent
- Don't run out or get consumed
- More resources = more savings

**Strategy**:
- Age I: Build resource engine
- Ages II-III: Benefit from reduced costs
- Trade cards provide multiple resource types

---

## Military & Combat

### Military Strength

**Sources**:
- Card military values (red circle)
- Bonus military from effects (added to card)
- Civilization starting bonuses

**Total Military** = Base + All Card Values + All Bonuses

### Conquest (End of Age)

**Winner Determination**:
1. Compare all players' total military
2. Highest wins (ties share victory)
3. Must have at least 1 military to win
4. Zero military = no conquest possible

**Rewards**:
- Age I: +2 culture
- Age II: +4 culture
- Age III: +6 culture

### War Phase (End of Age)

**War Declaration**:
- Automatically occurs for players with 2x an opponent's military
- Targets weakest opponent only
- Minimum 3 military required to attack

**War Resolution**:
```
IF attacker military ≥ 2 × defender military:
    IF defender has Fortified cards:
        → Attack fails (fortifications protect)
    ELSE:
        → Ruin random defender card
        → Defender loses 2 culture
        → Success message displayed
ELSE:
    → No war declared
```

**Fortifications**:
- Any card with type "f" (Fortified)
- Must be non-ruined
- Protects entire tableau
- Multiple fortifications don't stack

**Culture Loss**:
- 2 culture per successful attack
- Can reduce culture below starting amount
- Cannot go below 0

---

## Scoring & Victory

### Culture Sources

1. **Card Culture Values**: Blue circles on cards
2. **Conquest Rewards**: 2/4/6 per age
3. **Card Abilities**: Some cards grant culture bonuses
4. **Gold Conversion**: 3 gold = 1 culture (at game end)

### Final Scoring

**At end of Age III:**
1. Convert remaining gold (3:1 ratio)
2. Sum all culture from all sources
3. Highest culture wins!

**Tiebreaker**:
- Most military
- Then most gold
- Then most cards in play

### Victory Strategies

**Military Dominance**:
- Win all 3 conquests: 12 culture
- Prevent opponents from building

**Economic Engine**:
- Max gold generation
- Convert to culture at end
- Enables expensive wonder cards

**Balanced Approach**:
- Some military for conquests
- Strong tableau for culture
- Protect with fortifications

---

## Card Abilities

### Immediate Effects

**Activate on Play** (during Activate phase):
- `goldOnPlay:X` - Gain X gold immediately
- `resource:X` - Add resource type permanently
- Effects happen once when card enters play

### Triggered Effects

**Continuous** (always active):
- `military:X` - Adds X to military total
- `culture:X` - Adds X to culture total

**Age Start**:
- `goldPerAge:X` - Gain X gold at start of each age
- Triggers during Age II and Age III setup

**End of Age**:
- `trigger:endOfAge` - Happens during Conquest phase
- Example: "The 300" ruins itself

### Manual Abilities

**Identified By**: ⚡ button appears on card

**How to Use**:
1. Click ⚡ button on card in tableau
2. Check conditions are met (if any)
3. Effect resolves immediately
4. Card taps (rotates 45°)
5. Cannot use again until next age

**Common Manual Effects**:
- `nextCardFree` - Next card costs 0 gold
- `addMilitaryPerType` - Bonus based on card count
- `doubleConquestCulture` - Double all conquest rewards

**Conditions**:
- `hasType:X` - Must have at least one type X card
- `countType:X:N` - Must have at least N type X cards
- `opponentLacksType:X` - All opponents must lack type X

---

## Advanced Rules

### Hand Passing

After each turn (except turn 6):
- All hands rotate clockwise
- Your hand becomes your left neighbor's hand
- Creates draft-like dynamics
- Consider what you pass!

**Strategic Implications**:
- Hate-drafting (taking cards to deny opponents)
- Signaling (passing cards you want returned)
- Counting (tracking what's been played)

### Card Combos

**Resource Engines**:
```
Irrigation (Food) → Cheaper food-based cards
Multiple trade cards → Access to all resources
```

**Military Synergies**:
```
Agoge (Infantry boost) + Many infantry → Massive military
Chariots (anti-infantry) + Opponent heavy infantry → Counters
```

**Wonder Strategies**:
```
Colossus of Rhodes → Double conquest culture (use late)
The Pantheon → 9 instant culture (expensive but huge)
```

### Optimal Play Patterns

**Early Game (Age I)**:
- Prioritize resource-generating cards
- Don't overspend - passing is fine
- Build foundation for future

**Mid Game (Age II)**:
- Leverage resources for big plays
- Start military investment
- Look for synergies

**Late Game (Age III)**:
- High-value plays
- Manual ability timing crucial
- Calculate final scores

### Time Management

**Human Players**:
- 60 second timer per decision (Place phase)
- Resets each turn
- Auto-pass if time expires

**AI Players**:
- Faster (5-10 seconds)
- Auto-advance when all AI game
- Can spectate or step away

### Edge Cases

**Negative Gold**: Cannot occur (minimum 0)
**Negative Culture**: Can occur from war losses (minimum 0 at end)
**Ruined Resources**: Don't count (lose cost reduction)
**Tapped Ruined Cards**: Still ruined, tap state irrelevant
**Multiple Wars**: Can only be attacked once per war phase

---

## Quick Reference

### Turn Order
1. PLACE → 2. REVEAL → 3. ACTIVATE → (4. CONQUEST)* → (5. WAR)* → Next Turn
\* Only on turn 6 of each age

### Costs
- Base: Card cost (gold circle)
- Reduction: -1 per matching resource
- Minimum: 0 (can be free!)

### Victory
- Highest culture wins
- Culture from: cards + conquests + abilities + gold÷3

### Hotkeys
- Click card in hand: Place it
- Pass button: Skip & get 3 gold
- ⚡ on card: Activate manual ability
- Next Phase: Advance game

---

**Good luck, and may your civilization stand the test of time!**
