import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

# ---------- 1. Load JSON mismatches ----------
def load_mismatches_from_json(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        mismatches = json.load(f)

    converted = []
    for m in mismatches:
        # Parse reason to extract found font and expected font (if available)
        reason = m["reason"]
        if "instead of" in reason:
            parts = reason.replace("Font is '", "").replace("'", "").split(" instead of ")
            gevonden = parts[0].strip()
            verwacht = parts[1].strip() if len(parts) > 1 else "Montserrat"
        else:
            gevonden = "Onbekend"
            verwacht = "Montserrat"

        converted.append({
            "element": f"Regel {m['line']}",
            "type": "lettertype",
            "verwacht": verwacht,
            "gevonden": gevonden,
            "pagina": 1,  # If line ≠ page, you can later extend to map this properly
            "ernst": "laag",  # Default severity; could be set dynamically if needed
            "text": m["text"]
        })

    return converted


# ---------- 2. Console rapport ----------
def generate_console_report(data):
    print("Rapport van afwijkingen:")
    kleurcodes = {"laag": "\033[92m", "gemiddeld": "\033[93m", "hoog": "\033[91m"}
    reset = "\033[0m"
    print(f"{'Element':<15}{'Type':<12}{'Verwacht':<12}{'Gevonden':<12}{'Pagina':<6}{'Ernst'}")
    for item in data:
        kleur = kleurcodes[item['ernst']]
        print(f"{kleur}{item['element']:<15}{item['type']:<12}{item['verwacht']:<12}{item['gevonden']:<12}{item['pagina']:<6}{item['ernst']}{reset}")

# ---------- 3. PDF rapport ----------
def generate_pdf_report(data, pdf_file="rapport_fontcheck.pdf", logo_path=None):
    doc = SimpleDocTemplate(pdf_file, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Logo toevoegen (optioneel)
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
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN', (4,1), (4,-1), 'CENTER')
    ])

    # Kleurcodering per ernst
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
    elements.append(Paragraph(legend_text, styles['Normal']))

    doc.build(elements)
    print(f"\nPDF-rapport gegenereerd: {pdf_file}")

# ---------- 4. Main ----------
if __name__ == "__main__":
    json_file = "font_mismatches.json"  # Output from your font check script
    data = load_mismatches_from_json(json_file)

    generate_console_report(data)
    generate_pdf_report(data, pdf_file="rapport_fontcheck.pdf", logo_path="laméco_logo.png")
