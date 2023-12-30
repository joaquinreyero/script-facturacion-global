from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Image
from oauth2client.service_account import ServiceAccountCredentials
import gspread


def get_clients_to_print():
    credenciales_json = "client_secret_660460554817-rctv1rs9dhdup8nbs3mvks0du5qr289c.apps.googleusercontent.com.json"
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credenciales = ServiceAccountCredentials.from_json_keyfile_name(credenciales_json, scope)
    gc = gspread.authorize(credenciales)

    wks = gc.open("global-chequera").sheet1
    values = wks.get_all_values()

    client = []

    for row in values:
        if row[4].lower() == 'x':
            client.append((row[0], row[1], row[2], row[3]))
    return client


def print_invoice(clients: list, months: list):
    c = canvas.Canvas("output.pdf", pagesize=A4)

    table_height = A4[1]
    table_width = A4[0]
    num_rows = 3
    num_cols = 2
    row_height = table_height / num_rows
    col_width = table_width / num_cols

    img = Image("http://www.globaltechsrl.com.ar/images/logo.png", width=150, height=40)

    c.setDash(1, 2)
    for x, client in enumerate(clients):
        client_name, client_address, client_price, client_observation = client

        if x > 0:
            c.showPage()

        for i in range(4):
            for j in range(2):
                x = col_width * j
                y = table_height - (row_height * i)
                c.rect(x, y, col_width, row_height, fill=0)
                img.drawOn(c, x + 20, y + 230)
                c.setFont("Helvetica-Oblique", 10)
                c.drawString(x + 7, y + 200, "Solis 397 telefono 2657-332143/202556")
                c.setDash()
                c.line(x, y + 190, x + col_width, y + 190)
                c.setDash(1, 2)
                c.setFont("Helvetica", 12)
                c.drawString(x + 7, y + 160, f"Cliente: {client_name}")
                c.drawString(x + 7, y + 140, f"Domicilio:{client_address}")
                c.setFont("Helvetica-Bold", 20)
                c.setDash()
                c.drawString(x + 80, y + 100, f"Abono: {months[i - 1]}")
                c.line(x, y + 90, x + col_width, y + 90)
                c.line(x, y + 130, x + col_width, y + 130)
                c.setDash(1, 2)
                c.setFont("Helvetica", 13)
                c.drawString(x + 7, y + 70, f"Antes del 10: ${client_price}")
                c.setFont("Helvetica-Oblique", 10)
                if client_observation:
                    c.drawString(x + 7, y + 50, f"Observacion: {client_observation}")
                c.setFont("Helvetica-Oblique", 7)
                c.drawString(x + 6, y + 30,
                             "Estimado clientes comunicamos que los abonos deben ser pagados por transferencia")
                c.drawString(x + 6, y + 23,
                             "o mercado pago hasta el dia 10 inclusive al alias pago.internet.global o al numero")
                c.drawString(x + 6, y + 16,
                             "2657202556, enviando el comprobante a este mismo numero, si desea realizarlo en el")
                c.drawString(x + 6, y + 9, "cobradorantes del dia 9 de cada mes.")

    c.save()


if __name__ == "__main__":
    months = []
    for i in range(3):
        month = input(f"Ingrese el nombre del mes: ")
        months.append(month)

    print_invoice(get_clients_to_print(), months)
