import pyodbc


def obtener_conexion():
    conexion = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER='';'    # Cambiar SERVER según la instancia local de SQL Server
        'DATABASE=ReservaNatural;'
        'Trusted_Connection=yes;'
    )

    return conexion