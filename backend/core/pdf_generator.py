from django.template.loader import render_to_string
from weasyprint import HTML

def generate_invoice_pdf(invoice):
    """
    Génère le PDF d'une facture avec WeasyPrint.
    """
    context = {
        'invoice': invoice,
        'member': invoice.member,
        'registration': invoice.registration,
        'season': invoice.registration.season,
        'club_name': "Judo Club Hem",
        'club_address': "Rue des Écoles, 59510 Hem",
        'club_siret': "123 456 789 00012",
    }
    
    html_string = render_to_string('invoices/invoice_template.html', context)
    pdf = HTML(string=html_string).write_pdf()
    return pdf
