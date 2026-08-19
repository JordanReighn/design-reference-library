# Synthesis and website transformation

Read this reference when blending multiple design languages, translating a reference onto an existing product, or producing a project-specific `DESIGN.md`.

## Choose references by role

Give each reference a job instead of averaging complete systems together. Useful roles include:

- **Structure:** layout density, grids, section rhythm, navigation, and information hierarchy.
- **Expression:** color atmosphere, imagery, decorative treatments, and motion character.
- **Interface:** controls, forms, cards, data display, focus states, and compact interaction patterns.
- **Typography:** display/body relationship, scale, weight, tracking, and editorial voice.

Use one reference as the dominant source. Add a second or third only when it supplies a clearly missing role. If two sources disagree, resolve the conflict in favor of the user's product needs, accessibility, and the dominant source.

## Translate rather than clone

For each selected reference, separate transferable principles from brand-owned expression.

Transferable:

- Semantic color relationships and contrast strategy
- Type scale, rhythm, weight, and hierarchy
- Spacing cadence, grid logic, and content density
- Shape language, borders, elevation, and surface hierarchy
- Interaction feel, responsive behavior, and image treatment

Do not copy by default:

- Logos, wordmarks, slogans, product names, or corporate copy
- Proprietary photography, illustrations, icons, or font files
- Layouts whose distinctiveness depends on a specific campaign or product image
- Exact brand combinations that would make the result appear officially affiliated

Keep the user's identity as the content layer and apply the reference as the visual grammar.

## Transform an existing website

1. Record a baseline of representative pages and widths before editing.
2. Locate the existing token and component seams: CSS variables, theme objects, Tailwind configuration, component variants, layout primitives, and typography setup.
3. Map the target language to semantic roles before changing components. Typical roles include:
   - `canvas`, `surface`, `surface-raised`, `surface-inverse`
   - `text`, `text-muted`, `text-inverse`, `border`
   - `accent`, `accent-hover`, `accent-active`, `focus`
   - display, heading, body, label, caption, and mono typography
   - radius, spacing, elevation, container, and breakpoint scales
4. Apply foundational tokens first, shared primitives second, composed sections third, and page-specific exceptions last.
5. Preserve routes, content, forms, data flow, and interaction behavior unless the requested redesign includes structural work.
6. Inspect before/after states and correct local exceptions that undermine the new hierarchy.

If only a URL is available, inspection can establish the baseline and inform a specification. Actual changes require an editable project, CMS/design surface, or an explicitly requested local reconstruction.

## Project DESIGN.md shape

Use only sections that materially guide the project. A useful project document often contains:

1. Product context and design intent
2. Visual principles and atmosphere
3. Semantic color tokens with roles and states
4. Typography families, scale, and substitutes
5. Spacing, grid, containers, and breakpoints
6. Shape, borders, elevation, and imagery
7. Core component rules and interaction states
8. Responsive behavior and accessibility constraints
9. Project-specific do's and don'ts
10. Provenance: references used and what was adapted from each

Do not paste the source analyses together. Write one consistent specification using the project's names and implementation vocabulary.

## Visual verification

Check at least one content-rich page and one interaction-heavy surface when they exist. Verify:

- Desktop and mobile hierarchy
- Text wrapping, clipping, overflow, and density
- Navigation and form states
- Contrast and focus visibility
- Image cropping and empty/loading/error states
- Reduced motion and keyboard navigation where relevant

A successful transformation should feel intentionally art-directed, remain recognizably the user's product, and preserve its behavior.
