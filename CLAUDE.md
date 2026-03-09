# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Civilisations of the Middle Seas** - A turn-based civilization building card game where players compete to build the most cultured civilization across three ages.

- **Type**: Browser-based card game
- **Technology**: Single-page HTML application with vanilla JavaScript
- **No Build Process**: Game runs directly in browser
- **No Dependencies**: Pure HTML/CSS/JavaScript implementation

## File Structure

The project consists of two HTML files:
- `CIV 5.html` - Main game implementation (~3600 lines)
- `civilisations_game_icons.html` - Icon asset reference page

Image assets for civilizations, resources, and card types are in the root directory (JPG/SVG/PNG formats).

## Architecture

### Core Game Engine Classes

The game is built using an object-oriented architecture with the following main classes:

1. **GameEngine** (`CIV 5.html:~1536`)
   - Central game state management
   - Phase progression and turn management
   - Player creation and game initialization
   - Coordinates between all other systems

2. **CardDatabase** (`CIV 5.html:~2506`)
   - Stores all card definitions for Ages I, II, and III
   - Card structure: `{ name, cost, type, culture, military, resources[], ability, effect }`
   - Handles deck generation and shuffling

3. **EffectEngine** (`CIV 5.html:~2688`)
   - **Comprehensive card effect processing system** (fully implemented)
   - Handles immediate effects, triggered effects, manual activations, and conditions
   - Effect format: comma-separated string (e.g., `"goldOnPlay:1,resource:f"`)
   - Supports all effect types: goldOnPlay, goldPerAge, resource, tap, ruin, bonuses, etc.
   - Condition checking: hasType, countType, opponentLacksType
   - Trigger types: immediate, manual, endOfAge, playCardType (partial)
   - Manual activation via `manuallyActivateCard()` method
   - Age start triggers via `triggerAgeStart()` method
   - End of age triggers via `triggerEndOfAge()` method

4. **UIManager** (`CIV 5.html:~2725`)
   - Updates all visual elements
   - Manages player boards, hands, and tableau display
   - Handles notifications and modals
   - Creates card HTML with resource/type icons

5. **IconMapping** (`CIV 5.html:~1125`)
   - Maps resource types (a,f,k,m,s,v,w) to image assets
   - Maps card types (e,c,i,m,n,r,f,h,w,etc.) to icons
   - Maps civilizations to sigil images
   - Provides inline icon replacement in card ability text

6. **AIManager** (`CIV 5.html:~1204`)
   - Handles AI opponent decision-making
   - Three difficulty levels: easy, medium, hard
   - AI card selection, placement, and activation logic

7. **TimerManager** (`CIV 5.html:~1455`)
   - Manages turn timers and time limits
   - Handles auto-advance when time expires

### Game Flow

**Game Structure:**
- 3 Ages, each with 6 turns
- Each turn has 5 phases: place → reveal → activate → (conquest) → (war)
- Conquest and war phases only occur at the end of each age (turn 6)

**Phase Cycle:**
1. **Place Phase**: Players select a card from hand to play (or pass for +3 gold)
2. **Reveal Phase**: Cards are revealed and paid for (gold cost minus resource discounts)
3. **Activate Phase**: Card abilities trigger and take effect
4. **Conquest Phase**: (End of age only) Player with highest military gains culture (2/4/6)
5. **War Phase**: (End of age only) **Fully functional war system**
   - Players with 2x opponent's military can attack weakest opponent
   - Fortified cards block attacks
   - Successful attacks ruin random card and cause 2 culture loss
   - War results displayed with detailed breakdown

**Turn Progression:**
- After activate phase → next turn (turns 1-5)
- After activate phase on turn 6 → conquest phase
- After conquest → war phase
- After war → next age (or end game if Age III)

**Key Mechanics:**
- Hand passing: Hands rotate clockwise after each turn
- Card costs reduced by matching resources on cards in play
- Tableau: 18 slots (3 ages × 6 turns) where played cards are placed
- **Manual Card Activation**: Cards with `trigger:manual` show ⚡ button for player activation
- **Tapping System**: Cards tap when abilities used, untap at start of next age
- **Card States**: Normal, Tapped (rotated 45°), Ruined (grayed out, non-functional)
- **Passing**: Players can pass turn to gain 3 gold if unable to afford cards

### Resource System

**Resource Types:**
- `a` - Animals
- `f` - Food
- `k` - Knowledge
- `m` - Metal
- `s` - Stone
- `v` - Valuables
- `w` - Wood

Resources on cards in play reduce the cost of future cards with matching resource requirements.

### Card Types

- `a` - Concept
- `c` - Civic
- `e` - Economic
- `f` - Fortified
- `h` - Holy
- `i` - Infantry
- `m` - Mounted
- `n` - Naval
- `N` - Place
- `p` - Person
- `r` - Ranged
- `t` - Trade
- `u` - Underworld
- `w` - Wonder

### Reactive Trigger Cards (All Fully Implemented!)

**Age I Cards with Reactive Abilities**:
1. **Spearmen** (Infantry) - Gains +1 ⚔️ whenever an opponent plays a mounted unit
2. **Chariots** (Mounted) - Gains +1 ⚔️ whenever an opponent plays an infantry unit
3. **Fire Catapults** (Ranged) - Gains +1 ⚔️ whenever an opponent plays a civic card
4. **Watchtower** (Fortified) - When attacked, adds +1 ⚔️ to all your infantry, mounted, and ranged, then taps
5. **Agoge** (Civic) - Adds +1 ⚔️ to each infantry card when YOU play it
6. **Arabian Horses** (Trade) - Adds +1 ⚔️ to each mounted/trade card when YOU play it

**How They Work**:
- Reactive cards automatically trigger during the activate phase
- No player input required - effects happen automatically
- Triggers are logged in game history (🔗 icon)
- Notifications show when reactive abilities activate
- Can create powerful card combos and counter-strategies

### Civilizations

Each civilization has unique starting bonuses:
- **Rome**: 7 gold, 0 culture, 0 military
- **Greece**: 7 gold, 1 culture, 2 military
- **Egypt**: 8 gold, 2 culture, 0 military
- **Persia**: 8 gold, 1 culture, 1 military
- **The Celts**: 7 gold, 2 culture, 1 military
- **Carthage**: 9 gold, 1 culture, 0 military

Gold bonuses repeat at the start of each new age.

## Testing

- **Manual testing only** - Open HTML file in browser
- Test each phase transition carefully
- Verify AI behavior at different difficulty levels
- Check card cost calculations with various resource combinations
- Ensure modal displays work correctly
- Test with 2-12 players (both human and AI)

## Common Development Tasks

### Adding New Cards

1. Locate the `CardDatabase.initializeCards()` method
2. Add card definition to appropriate age array (1, 2, or 3)
3. Define card properties: name, cost, type, culture, military, resources, ability, effect
4. Use effect string format: `"effectType:value,effectType:value"`

### Modifying Game Phases

1. Phase handlers are in `GameEngine.phaseHandlers` object
2. Phase progression logic is in `GameEngine.nextPhase()`
3. Update `UIManager.updateGameInfo()` for phase display text

### Working with Effects

**Effect String Format**:
```
"type:value,type:value,trigger:triggerType,condition:condType:value,effect:effectType:value"
```

**Implemented Effect Types**:
- `goldOnPlay:X` - Gain X gold when card is played
- `goldPerAge:X` - Gain X gold at start of each age (after first)
- `goldOnPass:X` - Gain X gold when passing
- `resource:X` - Provide resource type (a,f,k,m,s,v,w)
- `military:X` / `culture:X` - Base stats (always active)
- `tap` - Tap the card (rotate 45°)
- `gainGold:X` - Gain gold (typically in manual effects)
- `nextCardFree` - Next card played costs 0 gold
- `addMilitary:X` - Add bonus military to this card
- `addMilitaryPerType:type:X` - Add X military per card of type
- `addMilitaryToTypes:types:X` - Add X military to each card of types
- `addCulturePerType:type:X` - Add X culture per card of type
- `ruinSelf` - Destroy this card
- `ruinRandomOpponentCard` - Destroy random opponent card
- `doubleConquestCulture` - Double all conquest culture earned
- `enablesFree:CardName` - Make specified card cost 0

**Trigger Types**:
- *(none)* - Immediate effect on play
- `manual` - Player-activated (shows ⚡ button)
- `endOfAge` - Triggers during conquest phase
- `playCardType:X` - **FULLY IMPLEMENTED** - Triggers when YOU play card of type X
- `otherPlayerPlaysType:X` - **FULLY IMPLEMENTED** - Triggers when OPPONENTS play card of type X
- `warDeclared` - **FULLY IMPLEMENTED** - Triggers when you're attacked in war phase

**Condition Types**:
- `hasType:X` - Must have at least one card of type X
- `countType:X:N` - Must have at least N cards of type X
- `opponentLacksType:X` - All opponents must lack type X cards

**Example Effects**:
```javascript
// Simple economic card
"goldOnPlay:2,resource:f"

// Manual ability with condition
"military:3,trigger:manual,condition:countType:i:2,effect:addMilitary:2,tap"

// End of age effect
"military:6,trigger:endOfAge,effect:ruinSelf"

// Complex combo
"culture:2,trigger:manual,condition:hasType:c,effect:addCulturePerType:c:1,tap"
```

### UI Modifications

1. All CSS is embedded in `<style>` tag at top of HTML
2. Card HTML generation is in `UIManager.getCardHTML()`
3. Player board creation is in `createPlayerBoards()` function
4. Modal system uses `showModal()` and `hideModal()` global functions

## Important Implementation Notes

- **State Management**: All game state is in `GameEngine.state` object
- **Global Instance**: Game engine is instantiated as global `game` variable
- **No Modules**: Everything is in global scope (pre-ES6 module style)
- **Inline Styles**: All CSS is embedded, no external stylesheets
- **Direct DOM**: Uses `getElementById` and `querySelector` - no framework
- **Event Handlers**: Inline onclick attributes and addEventListener
- **Card Hover**: Cards scale up 3x on hover with high z-index to break stacking contexts

## Completed Features (Version 1.0)

**Core Gameplay**:
- ✅ Full game loop (3 ages × 6 turns)
- ✅ All 5 phases implemented and working
- ✅ Conquest phase with culture rewards
- ✅ War phase with card destruction and fortification mechanics
- ✅ Passing system (+3 gold)
- ✅ Hand rotation (clockwise)
- ✅ Resource cost reduction system
- ✅ Victory conditions and final scoring

**Card Systems**:
- ✅ Comprehensive effect engine (20+ effect types)
- ✅ Manual card activation with ⚡ buttons
- ✅ Tapping/untapping system
- ✅ Card conditions (hasType, countType, etc.)
- ✅ Triggered effects (immediate, manual, endOfAge, playCardType, otherPlayerPlaysType, warDeclared)
- ✅ **Reactive trigger system** - Cards react to other cards being played!
- ✅ Bonus military/culture tracking
- ✅ Card ruining (from wars and effects)

**Visual & UX**:
- ✅ Image icons for resources, types, and civilizations
- ✅ Fallback text if images missing
- ✅ Card hover scaling (3x zoom)
- ✅ Notifications for game events
- ✅ Modal system for phases and menus
- ✅ Visual indicators (tapped, ruined, placed)
- ✅ Responsive layout

**AI & Automation**:
- ✅ Three AI difficulty levels
- ✅ AI card selection and placement
- ✅ Auto-advance for all-AI games
- ✅ Turn timers with auto-pass

**Documentation**:
- ✅ README.md - User quick start guide
- ✅ GAME_RULES.md - Complete rules reference
- ✅ DEVELOPMENT.md - Technical documentation
- ✅ CLAUDE.md - This file (AI assistant instructions)

## Known Limitations

- Maximum 12 players (UI layout constraint)
- Fixed 3 ages × 6 turns structure (hardcoded)
- Card database is hardcoded (not loaded from external file)
- Image paths are relative (images must be in same directory)
- No save/load functionality (no persistent state)
- No undo/redo system
- No game history/replay viewer
- Limited card variety (~15 Age I, ~9 Age II, ~6 Age III)
- Browser compatibility: Modern browsers only (uses CSS gradients, flexbox, grid)

## Future Enhancement Opportunities

**Gameplay**:
- Expand card database (30+ cards per age)
- Add more civilizations (Babylon, Vikings, etc.)
- Player-controlled war declarations (vs automated)
- More triggered effect types (playCardType, warDeclared)
- Card draft mode for civilization selection

**Technical**:
- Save/load game state (localStorage/JSON export)
- Undo/redo system
- Game history and replay
- Networked multiplayer
- Sound effects and music

**UI/UX**:
- Card animations
- Drag-and-drop placement
- Interactive tutorial
- Statistics and achievements
- Mobile-optimized layout
