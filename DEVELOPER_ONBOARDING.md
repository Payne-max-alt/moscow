# Developer Onboarding  
**Projekt: Platforma narzędzi wspierających zarządzanie projektami**

---

## 1. Wizja i cel projektu

Projekt ma na celu stworzenie modularnej platformy narzędziowej wspierającej zarządzanie projektami w metodykach Agile i hybrydowych.  
W centrum platformy znajduje się zestaw narzędzi usprawniających planowanie, retrospekcje, priorytetyzację oraz raportowanie postępów projektowych.  
**Misja:** _Dostarczać proste, wizualne i praktyczne rozwiązania tam, gdzie inne narzędzia są zbyt ciężkie lub mało elastyczne._

---

## 2. Zakres MVP i aktualny etap rozwoju

**MVP obejmuje:**
- MoSCoW Visualizer (priorytetyzacja backlogu)
- System wersjonowania zadań
- Eksport danych (CSV + Excel)
- Drag & Drop inline
- Dokumentacja zgodna z cyklem życia DSDM

**Status:** Zakończona faza podstaw, trwa rozwój ewolucyjny.

---

## 3. Architektura i technologia

- **Frontend:** Streamlit (tymczasowo), docelowo React + Tailwind + Next.js
- **Backend:** Python, planowane FastAPI
- **Baza danych:** obecnie `session_state`, plan: PostgreSQL / Supabase
- **Eksport:** CSV / XLSX (z wykresami)
- **Eksperymenty:** Drag & Drop wewnątrz osi backlogu

---

## 4. Struktura kodu i organizacja

- Plik główny: `app.py`
- Sekcje: sidebar, wykres, formularz dodawania, lista zadań
- Stany: `st.session_state.tasks`
- Refaktoryzacja: planowane wydzielenie komponentów `draw_chart()`, `render_task_row()` itd.

---

## 5. Proces pracy

- **Framework:** DSDM Agile Project Framework
- Fazy: Przed projektem → Wykonalność → Podstawy → Rozwój
- Gałęzie: `main`, `gold`, `drag&drop`
- Wersje: `v1.5` (aktualna), `v1.4` - GOLD

---

## 6. Standardy techniczne

- Styl: **PEP8**
- Komentarze: tylko tam, gdzie naprawdę trzeba
- Funkcje: zasada pojedynczej odpowiedzialności
- Narzędzia: `black`, `flake8`
- Testy: manualne, plan: **PyTest**, **Playwright**

---

## 7. Dokumentacja i narzędzia

- Dokumentacja projektowa (DSDM `.docx`)
- Backlog: MoSCoW + GitHub Projects
- Repozytorium: GitHub (3 główne branche)
- Eksport danych
- Strategia testów: draft

---

## 8. Komunikacja i onboarding

- Styl komunikacji: bezpośredni, z kulturą
- Feedback: aktywnie zachęcany
- Onboarding obejmuje:
  - ten dokument
  - dostęp do repozytorium
  - dostęp do dokumentacji projektowej
  - kontakt z zespołem core

---

**Witamy na pokładzie! 🚀**
