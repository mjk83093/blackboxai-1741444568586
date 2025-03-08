# UI/UX Design Guide (Nexelion Branding)

## Table of Contents
- [Design Principles](#design-principles)
- [Color Palette](#color-palette)
- [Typography](#typography)
- [Components](#components)
- [Layout Guidelines](#layout-guidelines)
- [Responsive Design](#responsive-design)
- [Accessibility](#accessibility)

## Design Principles

### 1. Clarity
- Clear and concise information presentation
- Intuitive navigation and user flow
- Consistent visual hierarchy
- Meaningful feedback for user actions

### 2. Efficiency
- Minimize clicks/steps to complete tasks
- Quick loading times
- Smart defaults
- Keyboard shortcuts for power users

### 3. Consistency
- Uniform design patterns
- Predictable behavior
- Standardized components
- Coherent terminology

## Color Palette (Nexelion Theme)

### Brand Colors
```css
/* Primary Colors */
--primary: #0074E4;      /* Electric Blue - Main Brand Color */
--primary-dark: #0056A3; /* Darker Electric Blue - Hover States */
--primary-light: #DCEFFF;/* Light Electric Blue - Backgrounds */

/* Secondary Colors */
--secondary: #FFB400;    /* Electric Gold - Innovation, Energy */
--secondary-dark: #E6A200;/* Darker Gold - Hover States */
--secondary-light: #FFF3D6;/* Light Gold - Backgrounds */
```

### System Colors
```css
/* Feedback Colors */
--success: #28A745;      /* Success states and positive actions */
--danger: #DC3545;       /* Error states and destructive actions */
--warning: #FFC107;      /* Warning states and cautionary actions */
--info: #17A2B8;         /* Information states and help actions */

/* Neutral Colors */
--black: #000000;        /* Text and high-contrast elements */
--gray-900: #212529;     /* Primary text */
--gray-700: #495057;     /* Secondary text */
--gray-500: #ADB5BD;     /* Disabled states */
--gray-300: #DEE2E6;     /* Borders */
--gray-100: #F8F9FA;     /* Backgrounds */
--white: #FFFFFF;        /* Base background */
```

### Usage Guidelines
- Use `--primary` for main call-to-action buttons and key interactive elements
- Use `--secondary` for complementary actions and highlights
- Use system colors for feedback and status indicators
- Use neutral colors for text, backgrounds, and subtle elements
- Maintain WCAG 2.1 AA contrast ratios in all color combinations

## Typography

### Font Stack
```css
/* Primary Font - For all body text and general UI */
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* Display Font - For headlines and large text */
--font-display: 'Montserrat', var(--font-primary);

/* Monospace - For code and technical content */
--font-mono: 'SF Mono', 'JetBrains Mono', monospace;
```

### Type Scale
```css
--text-xs: 0.75rem;   /* 12px - Small labels */
--text-sm: 0.875rem;  /* 14px - Secondary text */
--text-base: 1rem;    /* 16px - Body text */
--text-lg: 1.125rem;  /* 18px - Large body text */
--text-xl: 1.25rem;   /* 20px - Small headlines */
--text-2xl: 1.5rem;   /* 24px - Section headlines */
--text-3xl: 1.875rem; /* 30px - Page headlines */
--text-4xl: 2.25rem;  /* 36px - Hero headlines */
```

### Font Weights
```css
--font-normal: 400;   /* Regular text */
--font-medium: 500;   /* Emphasized text */
--font-semibold: 600; /* Headlines */
--font-bold: 700;     /* Strong emphasis */
```

## Components

### Buttons
```css
.btn-primary {
    background-color: var(--primary);
    color: var(--white);
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    font-weight: var(--font-medium);
    transition: background-color 0.2s ease;
}

.btn-primary:hover {
    background-color: var(--primary-dark);
}

.btn-secondary {
    background-color: var(--secondary);
    color: var(--black);
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    font-weight: var(--font-medium);
    transition: background-color 0.2s ease;
}

.btn-secondary:hover {
    background-color: var(--secondary-dark);
}
```

### Cards
```css
.card {
    background-color: var(--white);
    border: 1px solid var(--gray-300);
    border-radius: 0.5rem;
    padding: 1.5rem;
    transition: box-shadow 0.2s ease;
}

.card:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
```

### Forms
```css
.input {
    border: 1px solid var(--gray-300);
    border-radius: 0.375rem;
    padding: 0.5rem 0.75rem;
    font-size: var(--text-base);
    transition: border-color 0.2s ease;
}

.input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 2px var(--primary-light);
}
```

## Layout Guidelines

### Spacing Scale
```css
--space-1: 0.25rem;  /*  4px */
--space-2: 0.5rem;   /*  8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-12: 3rem;    /* 48px */
--space-16: 4rem;    /* 64px */
```

### Breakpoints
```css
--screen-sm: 640px;   /* Mobile landscape */
--screen-md: 768px;   /* Tablets */
--screen-lg: 1024px;  /* Desktops */
--screen-xl: 1280px;  /* Large desktops */
--screen-2xl: 1536px; /* Extra large displays */
```

### Container
```css
.container {
    width: 100%;
    margin-left: auto;
    margin-right: auto;
    padding-left: var(--space-4);
    padding-right: var(--space-4);
    max-width: var(--screen-xl);
}
```

## Accessibility

### Focus Styles
```css
:focus-visible {
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}
```

### Interactive Elements
- Minimum touch target size: 44x44px
- Clear hover and focus states
- Keyboard navigation support
- ARIA labels where needed

## Animation

### Transitions
```css
--transition-fast: 150ms ease;
--transition-base: 200ms ease;
--transition-slow: 300ms ease;
```

### Motion
- Use subtle animations
- Respect reduced-motion preferences
- Keep animations under 300ms
- Use appropriate easing curves
