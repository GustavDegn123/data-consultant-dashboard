# KlarData Rapportgenerator

Et automatiseret system til at generere salgsrapporter (PDF) for små og mellemstore virksomheder, baseret på deres egne data.

## 🧠 Funktioner

- Automatisk PDF-rapportering
- Kundeafhængigt indhold (konfiguration pr. kunde)
- Visuelle kapitelsider og nøgletal
- Dynamiske kommentarer
- E-mail afsendelse af rapport

## 🗂 Projektstruktur

- `report_generator.py`: Central funktion til at bygge og sende rapporten
- `customer_manager.py`: Info og konfiguration for hver kunde
- `scripts/`: Dataindlæsning, preprocessing og analyse
- `plots/`: Plotfunktioner med Plotly
- `metrics/`: Beregning af nøgletal
- `docs/`: Dokumentation og systembeskrivelse
- `generated_reports/`: Output af færdige rapporter
- `.env`: Miljøvariabler (skal ikke pushes til GitHub)

## 🚀 Kom i gang

1. Clone repoet:
   ```bash
   git clone https://github.com/<dit-brugernavn>/klardata-reports.git
   cd klardata-reports

   ## 🛠️ Teknologier

- Python 3.10+
- Plotly, FPDF, PyPDF2
- Git + GitHub
- Miljøstyring med `.env`
- Automatisk e-mail (SMTP)

## 📦 Installation

1. Opret virtuel miljø:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## 🧪 Git workflow

- `main`: stabil version
- `dev`: aktiv udviklingsbranch
- `feat/xyz`: nye funktioner og eksperimenter

### Sådan laver du ny feature-branch:
```bash
git checkout dev
git pull
git checkout -b feat/pdf-insights
# Lav ændringer...
git add .
git commit -m "Tilføj dynamiske indsigter"
git push -u origin feat/pdf-insights
