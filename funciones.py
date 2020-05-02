from datetime import datetime, timedelta

# timestamp = 1545730073
def convertTimestampToData(date):
    print("funciona timestam", date)
    dt_object = datetime.fromtimestamp(date)
    # print("dt_object =", dt_object)
    # print("type(dt_object) =", type(dt_object))
    return dt_object

def calcularMora():
    return "ads"

def CalcuarlCuotas(deudaCredito, sumaAbonos, importeCuotas):
    return (deudaCredito - sumaAbonos) / importeCuotas

def noSunday(fechaCredito, cuotasTotales, cuotasPagadas):
    print("FechaInicoDeCredto",fechaCredito.strftime('%d/%m/%y'))
    print("cuotasTotales:" , cuotasTotales)
    print("cuotasPagadas:", cuotasPagadas)
    from datetime import datetime, timedelta
    import pytz
    # asd = fechaCredito + timedelta(days=1)
    # print("week", asd.strftime('%d/%m/%y'))
    cuotasTotalesT = cuotasTotales
    daterange = []
    diasvencidos = []
    todosLosDIas = []
    # print(datetime.now(fechaCredito))

    i = 0
    diasPorRecorrer = 24
    # for i in range(1, cuotasTotalesT):
    while i < diasPorRecorrer:
        yesterday = fechaCredito + timedelta(days=i)
        if yesterday.weekday() == 6:
            i = i + 1
            diasPorRecorrer = diasPorRecorrer + 1
        else:
            daterange.append(yesterday.strftime('%d/%m/%y'))
            diasvencidos.append(yesterday)
            i = i + 1
            # print("DIAS", yesterday.strftime('%d/%m/%y'))

    # print("todosLosDIas", len(todosLosDIas))
    # print("todosLosDIas", todosLosDIas)
    print(daterange[-cuotasPagadas:])
    formato1 = "%a %b %d %H:%M:%S %Y"
    formato2 = "%d/%m/%y"
    fechaDePago = diasvencidos[-cuotasPagadas:][0]
    hoyAhora = datetime.now()
    diasDeMora = hoyAhora - fechaDePago
    diasDeMora = diasDeMora.days
    print("Dias de Mora:", diasDeMora)
    # print(type(fechaDePago))
    # print(type(hoyAhora))
    print("fechasPorPagar", len(daterange))
    jsonResposne = {
        "fechasCuotas" : daterange[-cuotasPagadas:],
        "DiasVencidos" : diasDeMora
    }
    return jsonResposne
    # print(*daterange[-cuotasPagadas:], sep='\n')

# noSunday("2020-04-09 16:31:58.612919", 24, 8)