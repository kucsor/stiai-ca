# Plan Îmbunătățiri Proiect Q&A Educational

> **Pentru Hermes:** Folosește subagent-driven-development și delegate_task pentru implementare.
> **Multi-agent:** Planner → Task-uri paralele → Review

**Obiectiv:** Transformă website-ul Q&A într-o platformă completă cu 100+ întrebări, generator automat, și export PDF.

**Arhitectură:** Site static HTML/JS + API DeepSeek pentru generare conținut + Cron job pentru actualizare zilnică.

**Tehnologii:** HTML/CSS/JS, Python, DeepSeek API, Cron

---

### Task 1: Generator Automat de Întrebări (Agent: EXECUTOR 1)
**Obiectiv:** Script Python care generează întrebări noi folosind DeepSeek API direct

**Fișiere:**
- Creează: `src/generate_questions.py`
- Modifică: `data/questions_latest.json`

**Context:** Scriptul trebuie să:
1. Trimita un prompt la DeepSeek API (model: deepseek-chat)
2. Primească o întrebare + răspuns nou
3. Salveze în JSON
4. Categorii: Corp Uman, Natura si Univers, Somn si Vis, Tehnologie

**Cod exemplu:**
```python
import requests, json, os

DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_qa_pair(category):
    prompt = f"""Generează o întrebare interesantă și un răspuns educațional în limba română.

Categoria: {category}

Format:
Întrebare: [întrebare interesantă]
Răspuns: [răspuns detaliat, cu explicație simplă, analogie, și secțiune pentru copii + adulți]"""
    
    response = requests.post(
        DEEPSEEK_URL,
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000
        }
    )
    return response.json()['choices'][0]['message']['content']
```

---

### Task 2: Export PDF (Agent: EXECUTOR 2)
**Obiectiv:** Buton "Exportă ca PDF" pe website care descarcă toate întrebările

**Fișiere:**
- Modifică: `public/index.html` (adaugă buton + JavaScript pentru export)
- Creează: `src/export_pdf.py`

**Context:**
- Folosește jsPDF prin CDN pentru export direct din browser
- Buton în bara de acțiuni
- PDF cu antet frumos și toate întrebările numerotate

---

### Task 3: Statistici și Grafică (Agent: EXECUTOR 3)
**Obiectiv:** Adaugă grafice și statistici vizuale pe website

**Fișiere:**
- Modifică: `public/index.html`

**Context:**
- Adaugă o secțiune "Statistici" cu:
  - Grafic de distribuție pe categorii (folosind Chart.js CDN)
  - Top 5 cuvinte cheie
  - Progres: câte întrebări din câte planificate
- Grafic tip "pie chart" cu culorile theme-ului

---

### Task 4: Dark/Light Theme Toggle (Agent: EXECUTOR 4)
**Obiectiv:** Comutare între dark mode (actual) și light mode

**Fișiere:**
- Modifică: `public/index.html`

**Context:**
- Adaugă un buton 🌙/☀️ în header
- Salvează preferința în localStorage
- CSS variables pentru ambele theme-uri
- Tranziție smooth la comutare

---

### Task 5: Întrebări Recomandate (Agent: EXECUTOR 5)
**Obiectiv:** Sistem de recomandare pe baza categoriei vizualizate

**Fișiere:**
- Modifică: `public/index.html`

**Context:**
- Când utilizatorul deschide un răspuns, arată 3 întrebări similare (aceeași categorie)
- Secțiune "Te-ar mai putea interesa:" după răspuns
- Linkuri rapide către acele întrebări

---

### Task 6: Review Final + Testare (Agent: REVIEWER)
**Obiectiv:** Verifică toate modificările și rulează teste

**Fișiere:**
- Toate fișierele modificate

**Context:**
- Verifică:
  - [ ] Toate funcționalitățile noi funcționează
  - [ ] Site-ul se încarcă fără erori
  - [ ] JSON cu 50+ întrebări există
  - [ ] Generatorul de întrebări funcționează
  - [ ] PDF export funcționează
  - [ ] Dark/Light toggle funcționează
  - [ ] Recomandările apar corect
