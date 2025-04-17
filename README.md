# KlarData Rapportgenerator

Et automatiseret system til at generere PDF-salgsrapporter for små og mellemstore virksomheder, baseret på deres egne data.

---

## 🧠 Funktioner

- Automatisk PDF-rapportering
- Kundeafhængigt indhold (konfiguration pr. kunde)
- Visuelle kapitelsider og nøgletal
- Dynamiske kommentarer baseret på data
- Automatisk afsendelse via e-mail (SMTP)

---

## 🗂 Projektstruktur

- `report_service/`: Håndtering af PDF-oprettelse og e-mail
- `scripts/`: Indlæsning, klargøring og analyse af data
- `app/`, `api/`: (Klar til fremtidigt UI eller API)
- `generated_reports/`: Output af færdige PDF-rapporter
- `data/`: CSV-filer og eksempeldata
- `docs/`: Dokumentation og teknisk beskrivelse
- `.env`: Miljøvariabler (bl.a. SMTP-login – pushes **ikke** til GitHub)

---

## 🚀 Kom i gang

1. **Clone repoet:**
```bash
git clone https://github.com/GustavDegn123/data-consultant-dashboard.git
cd data-consultant-dashboard

2. **Opret virtuelt miljø og installer pakker:**
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. **Tilføj .env-fil med e-mail credentials:**
EMAIL_SENDER=din_email@gmail.com
EMAIL_PASSWORD=din_app_adgangskode

4. **Generér rapport (eksempel):**
python test_report_generator.py

🛠️ Teknologier
Python 3.10+
Plotly (visualiseringer)
FPDF og PyPDF2 (PDF-oprettelse)
SMTP (e-mail-afsendelse)
Git + GitHub

🧪 Git Workflow
main: Stabil og deploy-klar version
dev: Hovedudviklings
feat/xyz: Nye features og eksperimenter

git checkout dev
git pull
git checkout -b feat/navn-på-feature
# Lav ændringer...
git add .
git commit -m "Tilføj ny funktion"
git push -u origin feat/navn-på-feature