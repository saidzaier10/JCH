import openpyxl
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from datetime import datetime

def export_registrations_to_excel(registrations):
    """
    Génère un fichier Excel contenant la liste des inscriptions.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inscriptions"

    # Headers
    headers = [
        "Nom", "Prénom", "Date de Naissance", "Catégorie", 
        "Payé", "Statut", "Email Parent", "Téléphone", "Saison"
    ]
    
    for col_num, header in enumerate(headers, 1):
        col_letter = get_column_letter(col_num)
        ws[f"{col_letter}1"] = header
        ws[f"{col_letter}1"].font = openpyxl.styles.Font(bold=True)

    # Data
    for row_num, reg in enumerate(registrations, 2):
        member = reg.member
        parent = member.parent
        
        email = parent.email if parent else member.email
        phone = member.phone
        
        ws[f"A{row_num}"] = member.last_name
        ws[f"B{row_num}"] = member.first_name
        ws[f"C{row_num}"] = member.birth_date.strftime("%d/%m/%Y") if member.birth_date else ""
        ws[f"D{row_num}"] = reg.category.name
        ws[f"E{row_num}"] = "Oui" if reg.paid else "Non"
        ws[f"F{row_num}"] = reg.get_status_display()
        ws[f"G{row_num}"] = email
        ws[f"H{row_num}"] = phone
        ws[f"I{row_num}"] = reg.season.name

    # Auto-adjust column width
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename=inscriptions_{datetime.now().strftime("%Y%m%d")}.xlsx'
    
    wb.save(response)
    return response
