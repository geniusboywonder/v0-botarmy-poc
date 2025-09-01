# BotArmy Style Guide

This document provides a comprehensive overview of the BotArmy POC application's design system, including the color palette, typography, and usage guidelines.

## Technology Stack

### Frontend Framework
- **Next.js**: 15.5.2 with App Router
- **React**: 19.x (latest stable)
- **TypeScript**: 5.x (strict mode enabled)

### Styling & UI
- **Tailwind CSS**: 3.4.17 (stable version for better CSS variable compatibility)
- **PostCSS**: 8.5.6 with Autoprefixer 10.4.21
- **shadcn/ui**: Radix UI components with Tailwind styling
- **CSS Variables**: HSL color format for theme system

### Configuration Files
- `tailwind.config.js`: Tailwind v3 configuration with extended color palette
- `postcss.config.mjs`: PostCSS configuration for Tailwind and Autoprefixer
- `app/globals.css`: Global styles with CSS custom properties

## Color System

The application uses a comprehensive theming system with CSS variables defined in `app/globals.css`. All colors are defined as HSL values in CSS custom properties and exposed through Tailwind CSS utility classes configured in `tailwind.config.js`.

### Base Palette

#### Light Theme

| Color Swatch | Color Name | Hex (Approximated) |
| :--- | :--- | :--- |
| <div style="width:100%;height:20px;background-color:#ffffff;border:1px solid #000;"></div> | `background` | `#ffffff` |
| <div style="width:100%;height:20px;background-color:#202b38;"></div> | `foreground` | `#202b38` |
| <div style="width:100%;height:20px;background-color:#fafafa;border:1px solid #ccc;"></div> | `card` | `#fafafa` |
| <div style="width:100%;height:20px;background-color:#0891b2;"></div> | `primary` | `#0891b2` |
| <div style="width:100%;height:20px;background-color:#f3f4f6;border:1px solid #ccc;"></div> | `secondary` | `#f3f4f6` |
| <div style="width:100%;height:20px;background-color:#6b7280;"></div> | `muted-foreground` | `#6b7280` |
| <div style="width:100%;height:20px;background-color:#ef4444;"></div> | `destructive` | `#ef4444` |
| <div style="width:100%;height:20px;background-color:#e5e7eb;border:1px solid #ccc;"></div> | `border` | `#e5e7eb` |

#### Dark Theme

| Color Swatch | Color Name | Hex (Approximated) |
| :--- | :--- | :--- |
| <div style="width:100%;height:20px;background-color:#1f2937;"></div> | `background` | `#1f2937` |
| <div style="width:100%;height:20px;background-color:#ffffff;border:1px solid #000;"></div> | `foreground` | `#ffffff` |
| <div style="width:100%;height:20px;background-color:#164e63;"></div> | `card` | `#164e63` |
| <div style="width:100%;height:20px;background-color:#06b6d4;"></div> | `primary` | `#06b6d4` |
| <div style="width:100%;height:20px;background-color:#374151;"></div> | `secondary` | `#374151` |
| <div style="width:100%;height:20px;background-color:#9ca3af;"></div> | `muted-foreground` | `#9ca3af` |
| <div style="width:100%;height:20px;background-color:#dc2626;"></div> | `destructive` | `#dc2626` |
| <div style="width:100%;height:20px;background-color:#374151;"></div> | `border` | `#374151` |

### Semantic Colors

These colors are used to convey meaning and represent different roles and message types in the application.

| Color Swatch | Color Name | Tailwind Class |
| :--- | :--- | :--- |
| <div style="width:100%;height:20px;background-color:#0891b2;"></div> | User | `user` |
| <div style="width:100%;height:20px;background-color:#f3f4f6;border:1px solid #ccc;"></div> | System | `system` |
| <div style="width:100%;height:20px;background-color:#3b82f6;"></div> | Analyst | `analyst` |
| <div style="width:100%;height:20px;background-color:#8b5cf6;"></div> | Architect | `architect` |
| <div style="width:100%;height:20px;background-color:#f97316;"></div> | Developer | `developer` |
| <div style="width:100%;height:20px;background-color:#10b981;"></div> | Tester | `tester` |
| <div style="width:100%;height:20px;background-color:#ef4444;"></div> | Deployer | `deployer` |
| <div style="width:100%;height:20px;background-color:#14b8a6;"></div> | Teal | `teal` |
| <div style="width:100%;height:20px;background-color:#f59e0b;"></div> | Amber | `amber` |

## Technical Implementation

### CSS Custom Properties Format

Colors are defined in `app/globals.css` using HSL format without the `hsl()` wrapper:

```css
:root {
  --background: 0 0% 100%;           /* White */
  --foreground: 222.2 84% 4.9%;      /* Dark slate */
  --primary: 188 100% 37%;           /* Cyan-600 */
  --border: 214.3 31.8% 91.4%;       /* Slate-200 */
  /* ... */
}

.dark {
  --background: 222.2 84% 4.9%;      /* Dark slate */
  --foreground: 210 40% 98%;         /* Light gray */
  --primary: 187 92% 44%;            /* Cyan-500 */
  /* ... */
}
```

### Tailwind Configuration

Colors are mapped in `tailwind.config.js` using the `hsl()` function:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        // ... extended palette
      }
    }
  }
}
```

## Usage Guidelines

### Color Application

All colors should be applied using the Tailwind CSS utility classes defined in `tailwind.config.js`. **Do not use hardcoded hex values or inline styles.**

#### Basic Usage

```html
<!-- Primary button -->
<button class="bg-primary text-primary-foreground hover:bg-primary/90">
  Click me
</button>

<!-- Card with border -->
<div class="bg-card border border-border rounded-lg p-4">
  Card content
</div>
```

#### Agent-Specific Colors

```html
<!-- Analyst agent message -->
<div class="bg-analyst/10 border border-analyst/20 text-analyst rounded-lg p-3">
  Analysis complete: Found 5 requirements
</div>

<!-- Developer agent status -->
<span class="bg-developer/10 text-developer px-2 py-1 rounded-full text-xs">
  Coding in progress
</span>
```

#### Opacity Modifiers

Use Tailwind's opacity modifiers for subtle backgrounds and effects:

```html
<!-- Light background -->
<div class="bg-primary/10">Light primary background</div>

<!-- Hover states -->
<button class="bg-secondary hover:bg-secondary/80">Hover effect</button>
```

### Best Practices

1. **Always use CSS variables**: Never hardcode color values
2. **Respect the theme system**: Colors automatically adapt to light/dark themes
3. **Use semantic names**: Prefer `bg-primary` over `bg-cyan-600`
4. **Leverage opacity**: Use `/10`, `/20`, etc. for subtle backgrounds
5. **Test in both themes**: Ensure components work in light and dark modes

## Tab Component Standards

### Tab Design Principles

The tab component follows traditional browser tab patterns for optimal user experience and accessibility.

### Visual Specifications

#### Tab List Structure
- **Container**: Transparent background with bottom border
- **Layout**: Horizontal flex layout with items aligned to bottom
- **Spacing**: No padding around the tab list container

#### Individual Tabs
- **Inactive State**:
  - Background: Transparent
  - Text: `text-muted-foreground` with hover to `text-foreground`
  - Border: Transparent top/left/right borders
  - Hover: `bg-muted/50` background overlay
  
- **Active State**:
  - Background: `bg-background` (matches content area)
  - Text: `text-foreground`
  - Border: `border-border` for top/left/right, `border-b-background` to connect seamlessly with content
  - Shadow: `shadow-sm` for subtle elevation

#### Tab Content Area
- **Background**: `bg-background` 
- **Border**: `border-border` on all sides except top
- **Border Radius**: `rounded-b-lg rounded-tr-lg` (rounded bottom corners and top-right)
- **Padding**: `p-4` default, customizable via className
- **Connection**: Border-top removed to create seamless connection with active tab

### Usage Guidelines

#### Basic Implementation
```tsx
<Tabs defaultValue="progress" className="w-full">
  <TabsList className="mb-0">
    <TabsTrigger value="progress">Progress</TabsTrigger>
    <TabsTrigger value="config">Configuration</TabsTrigger>
  </TabsList>

  <TabsContent value="progress" className="space-y-6 p-6">
    {/* Progress content */}
  </TabsContent>

  <TabsContent value="config" className="p-6">
    {/* Configuration content */}
  </TabsContent>
</Tabs>
```

#### Styling Customizations
- **TabsList**: Remove default margin with `mb-0` for seamless connection
- **TabsContent**: Add custom padding as needed (default `p-4` is applied)
- **Responsive**: Tabs automatically adapt to container width

#### Accessibility Features
- Full keyboard navigation support
- ARIA labels and roles provided by Radix UI
- Focus indicators with `focus-visible:ring-2 focus-visible:ring-primary/20`
- Proper color contrast ratios maintained

### Development Notes

- **Tailwind v3**: Using stable version for better CSS variable compatibility
- **HSL Format**: Provides better color manipulation and theme transitions  
- **No v4 Migration**: v4 had compatibility issues with the existing color system
- **Browser Support**: HSL custom properties work in all modern browsers
- **Tab Component**: Based on Radix UI Tabs primitive with custom styling for traditional browser tab appearance
