# Development Guide - Civilisations of the Middle Seas

## Technical Architecture

### Technology Stack
- **Frontend**: Pure HTML5, CSS3, vanilla JavaScript (ES6+)
- **No Framework**: Self-contained single-page application
- **No Build Process**: Direct browser execution
- **No Dependencies**: Zero external libraries

### File Structure
```
sixkingdoms/
├── CIV 5.html              # Main game file (~3600 lines)
├── civilisations_game_icons.html  # Icon reference
├── *.svg                   # Card type icons
├── *.jpg                   # Resource/civilization icons
├── README.md               # User documentation
├── GAME_RULES.md           # Complete rules
├── DEVELOPMENT.md          # This file
└── CLAUDE.md               # AI assistant instructions
```

---

## Core Classes

### GameEngine (`line ~1536`)

**Responsibilities**:
- Central game state management
- Phase progression and turn management
- Player creation and coordination
- Victory condition checking

**Key Methods**:
```javascript
createPlayer(name, type, civilizationKey)  // Create new player
startGame()                                 // Initialize game
nextPhase()                                 // Advance to next phase
nextTurn()                                  // Advance to next turn
nextAge()                                   // Advance to next age
placeCard(playerIndex, cardIndex)          // Player places card
manualPass(playerIndex)                     // Player passes turn
updatePlayerStats(player)                   // Recalculate totals
```

**State Structure**:
```javascript
this.state = {
    players: [],              // Array of player objects
    currentAge: 1,            // 1, 2, or 3
    currentTurn: 1,           // 1-6
    currentPhase: 'place',    // place, reveal, activate, conquest, war
    activePlayerIndex: 0,     // Currently acting player
    gameStarted: false,       // Game initialization flag
    settings: {...}           // Timer and AI settings
}
```

### CardDatabase (`line ~2506`)

**Responsibilities**:
- Store all card definitions
- Shuffle and deal cards
- Manage age decks

**Card Structure**:
```javascript
{
    name: "Card Name",
    cost: 3,                  // Gold cost
    type: "e",                // Card type (see types below)
    culture: 1,               // Culture points
    military: 2,              // Military strength
    resources: ["f", "w"],    // Resource types provided
    ability: "Description",   // Human-readable text
    effect: "effect:string"   // Machine-readable effects
}
```

**Card Types**:
- `a` = Concept
- `c` = Civic
- `e` = Economic
- `f` = Fortified
- `h` = Holy
- `i` = Infantry
- `m` = Mounted
- `n` = Naval
- `N` = Place
- `p` = Person
- `r` = Ranged
- `t` = Trade
- `u` = Underworld
- `w` = Wonder

### EffectEngine (`line ~2688`)

**Responsibilities**:
- Parse and execute card effects
- Handle triggers and conditions
- Process manual activations

**Effect String Format**:
```
"type:value,type:value,trigger:triggerType,condition:condType:value,effect:effectType:value"
```

**Examples**:
```javascript
"goldOnPlay:3,resource:f"  // Gain 3 gold, provide Food
"military:2,trigger:manual,effect:addMilitary:2,tap"  // Manual: +2 military, then tap
"culture:1,trigger:endOfAge,effect:ruinSelf"  // Ruin self at age end
```

**Supported Effects**:
- `goldOnPlay:X` - Immediate gold
- `goldPerAge:X` - Gold each age start
- `resource:X` - Add resource type
- `military:X` / `culture:X` - Add stats
- `tap` - Tap this card
- `gainGold:X` - Gain gold (manual)
- `addMilitary:X` - Bonus military to card
- `addMilitaryPerType:type:X` - Bonus per card type count
- `addCulturePerType:type:X` - Bonus culture per type
- `ruinSelf` - Destroy this card
- `ruinRandomOpponentCard` - Destroy opponent card
- `doubleConquestCulture` - Double conquest rewards
- `nextCardFree` - Next card costs 0

**Triggers**:
- *(none)* - Immediate on play
- `manual` - Player-activated
- `endOfAge` - During conquest phase
- `playCardType:X` - When type X played (not implemented)
- `warDeclared` - During war phase (not implemented)

**Conditions**:
- `hasType:X` - Must have type X card
- `countType:X:N` - Must have N+ type X cards
- `opponentLacksType:X` - All opponents lack type X

### UIManager (`line ~2725`)

**Responsibilities**:
- Render all visual elements
- Update displays
- Handle notifications and modals

**Key Methods**:
```javascript
updateGameDisplay()                         // Refresh entire UI
updateGameInfo()                            // Update age/turn/phase display
updatePlayerBoards()                        // Update all player boards
updatePlayerTableau(player, index)          // Render player's tableau
getCardHTML(card)                           // Generate card HTML
showNotification(message)                   // Display notification
showModal(title, content)                   // Display modal
```

### IconMapping (`line ~1164`)

**Responsibilities**:
- Map resource/type/civ codes to images
- Provide fallback text if images fail
- Replace text with inline icons

**Icon Sources**:
```javascript
this.resourceIcons = {
    'a': { name: 'Animals', image: 'Animals.svg', fallback: 'A' },
    // ... more resources
}

this.typeIcons = {
    'e': { name: 'Economic', image: 'Economic.svg', fallback: 'e' },
    // ... more types
}

this.civilizationIcons = {
    'rome': { name: 'Rome', image: 'Rome-sigil.svg', fallback: 'R' },
    // ... more civilizations
}
```

### AIManager (`line ~1262`)

**Responsibilities**:
- AI decision making
- Card evaluation
- Difficulty levels

**Difficulty Implementations**:
- **Easy**: Random affordable card
- **Medium**: Prioritize value (culture + military ÷ cost)
- **Hard**: Advanced evaluation with resource consideration

### TimerManager (`line ~1455`)

**Responsibilities**:
- Turn timers
- Auto-advance for AI games
- Timeout handling

---

## Adding New Cards

### Step 1: Define Card Object

```javascript
{
    name: "My New Card",
    cost: 4,
    type: "c",  // Civic
    culture: 2,
    military: 1,
    resources: ["s", "k"],  // Stone, Knowledge
    ability: "When played, gain 2 gold for each civic card you have.",
    effect: "culture:2,military:1,goldOnPlay:0,trigger:manual,condition:hasType:c,effect:gainGold:2,tap"
}
```

### Step 2: Add to Appropriate Age

In `CardDatabase.initializeCards()`:

```javascript
this.cards[2] = [  // Age II
    // ... existing cards
    {
        name: "My New Card",
        // ... card definition
    }
];
```

### Step 3: Test

1. Start game, reach appropriate age
2. Play the card
3. Verify effects trigger correctly
4. Test edge cases (conditions, tapping, etc.)

---

## Effect String Reference

### Format
```
"immediate_effect,immediate_effect,trigger:type,condition:check,effect:action,tap"
```

### Building Complex Effects

**Example 1: Simple Economic Card**
```javascript
effect: "goldOnPlay:2,resource:f"
// Immediate: +2 gold, provide Food resource
```

**Example 2: Manual Ability with Condition**
```javascript
effect: "military:3,trigger:manual,condition:countType:i:2,effect:addMilitary:2,tap"
// Always: +3 military
// Manual (if 2+ infantry): +2 more military, then tap
```

**Example 3: End-of-Age Effect**
```javascript
effect: "military:6,trigger:endOfAge,effect:ruinSelf"
// Always: +6 military
// At age end: Ruin this card
```

### Effect Processing Order

1. Parse effect string into effect objects
2. Filter by trigger type (immediate, manual, etc.)
3. Check conditions (if any)
4. Execute effects in order
5. Apply state changes (tap, ruin, etc.)

---

## Modifying Game Phases

### Phase Flow

```
Place → Reveal → Activate → (Conquest*) → (War*) → Next Turn/Age
* Only at turn 6 of each age
```

### Adding a New Phase

1. Add phase name to `this.phases` array
2. Create handler method: `handleMyPhase()`
3. Register handler: `this.phaseHandlers.myPhase = () => this.handleMyPhase()`
4. Update `nextPhase()` logic for progression
5. Add UI description in `UIManager.updateGameInfo()`

### Phase Handler Template

```javascript
handleMyPhase() {
    console.log('=== MY PHASE ===');

    // Do phase logic
    this.state.players.forEach(player => {
        // Process each player
    });

    // Update UI
    this.showNotification('My phase complete!');
    this.updateDisplay();
}
```

---

## Testing Guidelines

### Manual Testing Checklist

**Game Flow**:
- [ ] Can start game with 2-12 players
- [ ] All 3 ages complete successfully
- [ ] Victory screen displays correctly
- [ ] Can start new game after completion

**Card Mechanics**:
- [ ] Cards can be placed if affordable
- [ ] Resource cost reduction works
- [ ] Manual abilities activate with ⚡ button
- [ ] Tapped cards cannot be reactivated
- [ ] Ruined cards are grayed and don't count

**Combat**:
- [ ] Conquest awards culture to military leader
- [ ] Wars occur when military imbalance exists
- [ ] Fortifications block wars
- [ ] Successful wars ruin cards and reduce culture

**AI**:
- [ ] AI makes legal moves
- [ ] AI doesn't crash or timeout
- [ ] Different difficulties behave differently

### Common Issues

**Issue**: Cards not showing icons
**Solution**: Check image file paths, verify SVG files exist

**Issue**: Effects not triggering
**Solution**: Check effect string format, verify EffectEngine handles effect type

**Issue**: Phase not advancing
**Solution**: Check `nextPhase()` logic, verify phase handlers don't throw errors

**Issue**: AI not acting
**Solution**: Check AIManager card evaluation, verify affordable cards exist

---

## Performance Considerations

### Bottlenecks

1. **DOM Updates**: Full tableau redraws can be slow
   - Minimize: Only update changed players
   - Consider: Virtual DOM or incremental updates

2. **Effect Parsing**: String parsing on every activation
   - Optimization: Cache parsed effects

3. **AI Calculations**: Card evaluation in loops
   - Optimization: Memoize evaluations

### Scalability

**Current Limits**:
- 12 players max (UI constraint)
- 18 cards per player (3 ages × 6 turns)
- ~50 cards per age deck

**Potential Extensions**:
- More ages (requires new cards)
- More turns per age (longer games)
- Larger player counts (UI redesign needed)

---

## Known Limitations

1. **No Undo**: Can't take back card plays
2. **No Save/Load**: Game state not persistent
3. **Limited AI**: Basic strategy only
4. **No Networking**: Local play only
5. **No Animations**: Instant state changes
6. **Manual Ability Timing**: Can only activate during any phase (not phase-restricted)

---

## Future Enhancement Ideas

### Gameplay
- [ ] More cards (expand to 30+ per age)
- [ ] More civilizations (add Babylon, Vikings, etc.)
- [ ] Draft mode (pick civilization from pool)
- [ ] Campaign mode (linked games with progression)
- [ ] Achievements system

### Technical
- [ ] Save/load game state (localStorage)
- [ ] Undo/redo system
- [ ] Game replay/history viewer
- [ ] Animated card effects
- [ ] Sound effects
- [ ] Network multiplayer (WebRTC/WebSockets)

### UI/UX
- [ ] Improved card hover previews
- [ ] Drag-and-drop card placement
- [ ] Interactive tutorial
- [ ] Statistics tracking
- [ ] Customizable themes

---

## Debugging Tips

### Console Logging

Key logs to watch:
```javascript
console.log('=== PHASE NAME ===')  // Phase transitions
console.log(`${player.name} ...`)  // Player actions
console.log(`Activating ${card.name}`)  // Effect triggers
```

### Browser Dev Tools

**Useful Commands**:
```javascript
game.state  // View current state
game.state.players[0]  // Inspect specific player
game.effectEngine.manuallyActivateCard(player, cardIndex, game.state)  // Test activation
```

### Common Debug Scenarios

**Card not activating**:
1. Check `card.effect` string
2. Verify effect type is implemented
3. Check conditions are met
4. Look for console errors

**Phase stuck**:
1. Check `game.state.currentPhase`
2. Verify button states
3. Check player.placedCard values
4. Look for nextPhase() calls

**Wrong stats**:
1. Check `updatePlayerStats()` logic
2. Verify card values (culture, military)
3. Check for ruined/tapped cards
4. Inspect bonusMilitary properties

---

## Code Style

### Conventions
- **Classes**: PascalCase (`GameEngine`, `CardDatabase`)
- **Methods**: camelCase (`nextPhase`, `updateDisplay`)
- **Constants**: UPPER_SNAKE_CASE (if any)
- **Variables**: camelCase (`playerIndex`, `cardData`)

### Comments
- Use JSDoc for class/method documentation
- Inline comments for complex logic
- Section headers for major code blocks

### Best Practices
- Keep methods focused and small
- Avoid deep nesting (max 3 levels)
- Use early returns for clarity
- Prefer const over let
- Use template literals for strings with variables

---

## Contributing

### Before Making Changes
1. Read existing code in relevant section
2. Understand the architecture
3. Test manually in browser
4. Check console for errors

### Making Changes
1. Update relevant class/method
2. Test the specific feature
3. Test full game flow
4. Update documentation if needed

### Submitting Changes
1. Ensure game runs without errors
2. Test with 2, 4, and 8 players
3. Verify AI still works
4. Update CLAUDE.md if architecture changed

---

**Happy developing! Build something awesome!**
