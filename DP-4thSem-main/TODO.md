# 📋 SCMS Project - Pending Tasks & Roadmap

> **Note:** The webpaths detailed in this document are incomplete. The correct webpath should be like @[DP-4thSem-main/complaint-management-system/stitch_webpath.txt].

This file contains the current progress and the "to-do" list for completion. Refer to this when starting work on the repository.

---

## 🚀 1. Setup & Environment
- [ ] **Clone**: `git clone https://github.com/24cu0310111-ship-it/DP-4thSem.git`
- [ ] **Install**: `npm install`
- [ ] **Run**: `npm run dev`
- [ ] **Ref Reference**: Link to the Stitch Project `4322261519944648783`.

---

## 🚧 2. Immediate Fixes & Logic
- [ ] **Navigation Expansion**: In `src/data/mockData.ts`, update `navigationData` to include links for sections:
  - Protocol (`#protocol`)
  - Lifecycle (`#lifecycle`)
  - Capabilities (`#capabilities`)
  - Dashboard (`#dashboard`)
  - Performance (`#performance`)
- [ ] **Section ID Audit**: Check all component files in `src/components/sections/` and ensure each `<section>` tag has its corresponding `id`.
- [ ] **Mobile Navbar**: Add a mobile-friendly menu/drawer toggle in `src/components/layout/Navbar.tsx`.

---

## 🧹 3. Refactoring & Code Quality
- [ ] **Split `RemainingSections.tsx`**: Move the components below into their own files under `src/components/sections/` (and `src/components/layout/` for the Footer):
  - [ ] `Performance.tsx`
  - [ ] `Testimonials.tsx`
  - [ ] `Feedback.tsx`
  - [ ] `Footer.tsx` (Move to layout folder)
- [ ] **Fix Imports in `App.tsx`**: Update paths after splitting the components.

---

## ✨ 4. Visual & UI Optimization
- [ ] **1:1 Parity Check**: Compare the current layout with the Stitch 디자인 to match:
  - Corner roundness (`ROUND_EIGHT` tokens).
  - Background contrast (Surface vs Surface-light).
  - Subtle hover states and shadows for consistency.
- [ ] **Form Validation**: Add simple validation/feedback to the `Feedback.tsx` form.

---

## 🔮 5. Future Development
- [ ] **Backend Integration**: Replace the static records in `src/data/mockData.ts` with hooks or Redux/Zustand to handle real complaints.
- [ ] **Feedback Form**: The 'Submit Feedback' form at the bottom of the page currently sets a local React state to simulate success. This needs to be wired to a real endpoint.

---

## 📅 Status Update (2026-04-04)
The current build has all major sections imported in `App.tsx`, but the logic for section navigation and mobile responsiveness is only partially complete. The core design system (`index.css`) and data structures (`mockData.ts`) are already set up.
