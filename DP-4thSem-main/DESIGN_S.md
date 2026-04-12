# Design System Strategy: The Obsidian Protocol

> **Note:** The webpaths detailed in this document are incomplete. The correct webpath should be like @[DP-4thSem-main/complaint-management-system/stitch_webpath.txt].

## 1. Overview & Creative North Star
**The Creative North Star: "Kinetic Intelligence"**

This design system is built to move away from the static, rigid "dashboard" aesthetic of common SaaS platforms and toward an experience that feels alive, responsive, and deeply sophisticated. We are moving beyond "Standard Dark Mode" into a realm of **Obsidian Depth**. 

The goal is to communicate high-level problem solving through "Kinetic Intelligence"—a visual language where information doesn't just sit on a page, it floats within a multi-dimensional space. By utilizing intentional asymmetry, overlapping glass layers, and high-contrast geometric typography, we create an editorial feel that positions the product as an elite, futuristic solution rather than a utility tool.

---

## 2. Color & Surface Philosophy

### The Palette
We utilize a sophisticated range of deep obsidian tones contrasted with neon-gas accents. 
- **Primary Accent (`#bbc3ff`):** Electric Blue. Use for high-intent actions and primary focus.
- **Secondary Accent (`#d1bcff`):** Soft Violet. Use for secondary flow paths and depth-layer highlights.
- **Tertiary Accent (`#00dce5`):** Cyan Neon. Reserved for "intelligence" indicators—AI status, data pips, and glowing interactive states.

### Named Color Tokens (from Stitch)

| Token | Hex | Usage |
|-------|-----|-------|
| `background` | `#121318` | The infinite void — base layer |
| `surface` | `#121318` | Primary surface |
| `surface-dim` | `#121318` | Dimmed surface |
| `surface-bright` | `#38393e` | Elevated bright surfaces |
| `surface-container-lowest` | `#0d0e13` | Deepest nesting |
| `surface-container-low` | `#1a1b20` | Section grounding |
| `surface-container` | `#1e1f25` | Active interactive plane |
| `surface-container-high` | `#292a2f` | Elevated containers |
| `surface-container-highest` | `#34343a` | Top-level containers |
| `surface-variant` | `#34343a` | Variant surfaces |
| `surface-tint` | `#bbc3ff` | Surface tint accent |
| `on-background` | `#e3e1e9` | Text on background |
| `on-surface` | `#e3e1e9` | Primary text |
| `on-surface-variant` | `#c6c5d0` | Secondary text |
| `primary` | `#dfe1ff` | Primary color |
| `primary-container` | `#bbc3ff` | Primary container |
| `on-primary` | `#242c5e` | Text on primary |
| `on-primary-container` | `#474f83` | Text on primary container |
| `secondary` | `#d1bcff` | Secondary color |
| `secondary-container` | `#503f79` | Secondary container |
| `on-secondary` | `#37265e` | Text on secondary |
| `on-secondary-container` | `#c2aef0` | Text on secondary container |
| `tertiary` | `#66f7ff` | Tertiary color |
| `tertiary-container` | `#00dce5` | Tertiary container |
| `on-tertiary` | `#003739` | Text on tertiary |
| `on-tertiary-container` | `#005c60` | Text on tertiary container |
| `error` | `#ffb4ab` | Error state |
| `error-container` | `#93000a` | Error container |
| `on-error` | `#690005` | Text on error |
| `on-error-container` | `#ffdad6` | Text on error container |
| `outline` | `#90909a` | Outline borders |
| `outline-variant` | `#46464f` | Subtle outlines |
| `inverse-surface` | `#e3e1e9` | Inverse surfaces |
| `inverse-on-surface` | `#2f3036` | Text on inverse |
| `inverse-primary` | `#525b90` | Inverse primary |

### The "No-Line" Rule
Traditional 1px borders are strictly prohibited for sectioning. They create visual friction and "box in" the intelligence. Boundaries must be defined through:
1. **Background Shifts:** Moving from `surface` (#121318) to `surface-container-low` (#1a1b20).
2. **Tonal Transitions:** Using subtle `surface-variant` gradients to imply containment without a hard stroke.

### Surface Hierarchy & Nesting
Think of the UI as a series of physical layers stacked in a dark room.
- **Base Layer:** `surface` (#121318) - The infinite void.
- **Section Layer:** `surface-container-low` (#1a1b20) - Subtle grounding for content blocks.
- **Interactive Layer:** `surface-container` (#1e1f25) - The active plane for cards.
- **Floating Layer:** `surface-bright` (#38393e) at 60% opacity with 24px backdrop blur for high-level modals or navigation.

### The "Glass & Gradient" Rule
To achieve a signature "soul," all primary CTAs and hero elements must utilize a dual-tone gradient (Primary to Primary-Container). Use `glassmorphism` for any floating UI element to allow the "ambient light" of the background glow to bleed through, ensuring the layout feels integrated, not pasted.

---

## 3. Typography: The Editorial Edge

The typography system is designed to create a "Technical Editorial" look, balancing the aggressive geometry of Space Grotesk with the human-centric clarity of Inter and Manrope.

| Role | Font | Style Notes |
|------|------|-------------|
| **Display** | Space Grotesk | -0.04em letter spacing. Massive, high-contrast hero claims. |
| **Headline** | Space Grotesk | Bold and geometric. Guides user through the "story" of data. |
| **Body** | Inter | Clean, high-legibility sans-serif. Used for descriptions and data. |
| **Labels** | Manrope | All-caps, +0.05em tracking. Technical "scanned" aesthetic. |

---

## 4. Shape & Spacing

- **Corner Roundness:** 8px (`ROUND_EIGHT`) for all UI elements
- **Spacing Scale:** 3 (Stitch spacing scale multiplier)

---

## 5. Elevation, Depth & Light

### The Layering Principle
Depth is achieved by "stacking" tones. Place a `surface-container-lowest` card on a `surface-container-low` section. The contrast should be so subtle that the user "feels" the lift rather than "sees" a border.

### Ambient Shadows & Neon Glow
*   **Shadows:** Shadows must be extra-diffused. Use a 40px blur at 6% opacity. Never use pure black; use a tinted version of `surface-container-highest`.
*   **The Intelligence Glow:** For key "Smart" features, apply a `tertiary` (#00dce5) outer glow at 15% opacity with a 24px spread. This simulates a "screen emission" effect.

### The "Ghost Border" Fallback
If a border is required for accessibility, use a **Ghost Border**: `outline-variant` (#46464f) at 15% opacity. Full-opacity borders are considered a design failure in this system.

---

## 6. Component Logic

### Buttons (The "Pulse" Interaction)
- **Primary:** Gradient fill (`primary` to `primary-container`). On hover, scale 1.02x and increase the gradient border intensity from 20% to 100%.
- **Tertiary (Ghost):** No background. Label in `primary-fixed-dim`. On hover, a `surface-variant` glass background fades in.

### Cards & Intelligence Modules
**Strict Rule: No Divider Lines.** Separate content using the Spacing Scale (typically `spacing-6` or `spacing-8`). Use a `surface-container` background with a 1.02x hover scale to signal interactivity.

### Smart Chips
- **Selection:** `secondary-container` background with `on-secondary-container` text.
- **Logic:** Use a 2px `tertiary` dot on the left to indicate an "active" AI process or status.

### Input Fields
- **Default:** `surface-container-low` with a 1px ghost border (15% opacity).
- **Focus:** Border transitions to 60% `primary-container` with a subtle 10px glow of the same color. Label (Manrope) stays pinned to the top-left in `muted-gray`.

### Signature Component: The "Timeline Pulse"
For complaint management, use a vertical "Pulse" line. Instead of a solid line, use a gradient stroke that fades into the background, with `tertiary` (#00dce5) glowing nodes representing complaint milestones.

---

## 7. Do's and Don'ts

### Do:
- **Do** use intentional white space. Let the obsidian background breathe.
- **Do** overlap elements. A card slightly hanging off a section edge creates a sense of depth.
- **Do** use Manrope for small technical data—it adds a "pro" layer to the UI.
- **Do** use the 1.02x scale on hover for all interactive cards to provide tactile feedback.

### Don't:
- **Don't** use 1px solid white or light-gray borders.
- **Don't** use standard "Drop Shadows" (0, 4, 10, black). Use our ambient shadow values.
- **Don't** use pure black (#000). Always use the Obsidian base (#121318).
- **Don't** cram content. If it feels tight, increase the spacing by two increments in the scale.

---

## 8. Stitch Project Reference

- **Project ID:** `4322261519944648783`
- **Color Mode:** DARK
- **Device Type:** DESKTOP
- **Primary Color:** `#bbc3ff`
- **Secondary Color:** `#d1bcff`
- **Tertiary Color:** `#00dce5`
- **Neutral Color:** `#121318`
- **Color Variant:** FIDELITY
