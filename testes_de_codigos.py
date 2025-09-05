from datetime import date

ano = date.today().year
data = date.today()
dataFormatada = data.strftime("%d/%m/%Y")

print(dataFormatada)
print(data)
print(ano)

