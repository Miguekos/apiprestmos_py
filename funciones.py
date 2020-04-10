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

def noSunday(fechaCredito, cuotasTotales, cuotasPagadas):
    print(fechaCredito.strftime('%d/%m/%y'))
    print(cuotasTotales)
    print(cuotasPagadas)
    from datetime import datetime, timedelta
    import pytz
    # asd = fechaCredito + timedelta(days=1)
    # print("week", asd.strftime('%d/%m/%y'))
    cuotasTotalesT = cuotasTotales
    daterange = []
    diasvencidos = []
    # print(datetime.now(fechaCredito))
    for i in range(1, cuotasTotalesT):
        # print(cuotasTotalesT)
        yesterday = fechaCredito + timedelta(days=i)
        if yesterday.weekday() != 6:
            daterange.append(yesterday.strftime('%d/%m/%y'))
            diasvencidos.append(yesterday)
            # print("DIAS", yesterday.strftime('%d/%m/%y'))
    print(daterange[-cuotasPagadas:])
    formato1 = "%a %b %d %H:%M:%S %Y"
    formato2 = "%d/%m/%y"
    fechaDePago = diasvencidos[-cuotasPagadas:][0]
    hoyAhora = datetime.now()
    diasDeMora = hoyAhora - fechaDePago
    diasDeMora = diasDeMora.days
    print(diasDeMora)
    print(type(fechaDePago))
    print(type(hoyAhora))
    print("fechasPorPagar", len(daterange))
    jsonResposne = {
        "fechasCuotas" : daterange[-cuotasPagadas:],
        "DiasVencidos" : diasDeMora
    }
    return jsonResposne
    # print(*daterange[-cuotasPagadas:], sep='\n')

# noSunday("2020-04-09 16:31:58.612919", 24, 8)