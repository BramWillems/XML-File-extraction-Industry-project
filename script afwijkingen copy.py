import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet


# ---------- 1. Dummy data (kan later vervangen door echte afwijkingen JSON) ----------
dummy_afwijkingen = [
    {"element": "Titel dia 1", "type": "kleur", "verwacht": "#000000", "gevonden": "#111111", "pagina": 1, "ernst": "hoog"},
    {"element": "Tekstvak 1", "type": "lettertype", "verwacht": "Calibri", "gevonden": "Arial", "pagina": 2, "ernst": "laag"},
    {"element": "Paragraaf 3", "type": "marges", "verwacht": "2 cm", "gevonden": "1.5 cm", "pagina": 3, "ernst": "gemiddeld"},
    {"element": "Logo", "type": "logo", "verwacht": "rechtsboven", "gevonden": "linksonder", "pagina": 1, "ernst": "hoog"},
    {"element": "Lijst dia 4", "type": "opsomming", "verwacht": "bullets", "gevonden": "nummering", "pagina": 4, "ernst": "laag"}
]

# ---------- 2. Console rapport met kleurcodering ----------
def generate_console_report(data):
    print("Rapport van afwijkingen:")
    kleurcodes = {"laag": "\033[92m", "gemiddeld": "\033[93m", "hoog": "\033[91m"}
    reset = "\033[0m"
    print(f"{'Element':<15}{'Type':<12}{'Verwacht':<12}{'Gevonden':<12}{'Pagina':<6}{'Ernst'}")
    for item in data:
        kleur = kleurcodes[item['ernst']]
        print(f"{kleur}{item['element']:<15}{item['type']:<12}{item['verwacht']:<12}{item['gevonden']:<12}{item['pagina']:<6}{item['ernst']}{reset}")

# ---------- 3. PDF rapport ----------
def generate_pdf_report(data, pdf_file="rapport_dummy.pdf", logo_path="laméco_logo.png"):
    doc = SimpleDocTemplate(pdf_file, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Logo toevoegen bovenaan rechts
    if logo_path:
        try:
            img = Image(logo_path, width=100, height=50)
            img.hAlign = 'RIGHT'
            elements.append(img)
            elements.append(Spacer(1, 12))
        except Exception as e:
            print(f"Kon logo niet laden: {e}")

    # Titel
    title = Paragraph("Laméco Documentstijl Controle Rapport", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Tabeldata
    table_data = [["Element", "Type", "Verwacht", "Gevonden", "Pagina", "Ernst"]]
    for item in data:
        table_data.append([item['element'], item['type'], item['verwacht'], item['gevonden'], str(item['pagina']), item['ernst']])

    table = Table(table_data, repeatRows=1)

    # Table styling + kleurcodering op basis van ernst
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN', (4,1), (4,-1), 'CENTER')
    ])
    for i, item in enumerate(data, start=1):
        if item['ernst'] == 'hoog':
            style.add('BACKGROUND', (0,i), (-1,i), colors.salmon)
        elif item['ernst'] == 'gemiddeld':
            style.add('BACKGROUND', (0,i), (-1,i), colors.yellow)
        else:
            style.add('BACKGROUND', (0,i), (-1,i), colors.lightgreen)

    table.setStyle(style)
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Legenda
    legend_text = "Legenda: Hoog = rood, Gemiddeld = geel, Laag = groen"
    legend = Paragraph(legend_text, styles['Normal'])
    elements.append(legend)

    doc.build(elements)
    print(f"\nPDF-rapport gegenereerd: {pdf_file}")

# ---------- 4. Main ----------
if __name__ == "__main__":
    # Console rapport
    generate_console_report(dummy_afwijkingen)

    # PDF rapport (nu met logo laméco_logo.png)
    generate_pdf_report(dummy_afwijkingen, pdf_file="rapport_dummy.pdf", logo_path="laméco_logo.png")
