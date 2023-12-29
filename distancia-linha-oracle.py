import cx_Oracle
import math

host = 'x'
servico = 'x'
usuario = 'x'
senha = 'x'

# Encontra o arquivo que aponta para o banco de dados
cx_Oracle.init_oracle_client(lib_dir="./instantclient_21_10")

# Faz a conexão ao banco de dados
conecta_banco = cx_Oracle.connect(usuario, senha, f'{host}/{servico}')

# Cria um cursor no banco para que seja possível fazer consultas e alterações no banco de dados
cursor = conecta_banco.cursor()

def calcular_distancia_haversine(origem, destino):
    # Função para converter graus para radianos
    def graus_para_radianos(graus):
        return graus * math.pi / 180.0

    lat1, lon1 = map(float, origem.split(','))
    lat2, lon2 = map(float, destino.split(','))

    raio_terra_km = 6371.0

    diferenca_lat = graus_para_radianos(lat2 - lat1)
    diferenca_lon = graus_para_radianos(lon2 - lon1)

    a = math.sin(diferenca_lat / 2) ** 2 + math.cos(graus_para_radianos(lat1)) * math.cos(graus_para_radianos(lat2)) * math.sin(diferenca_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = raio_terra_km * c
    print(origem)
    print(destino)
    print(f"Distância: {distancia:.3f} Km")
    return distancia
    
    
codvendedor = int(input('Informe o código do vendedor: '))
check_date = input('Informe a data: ')

consulta_sql = """SELECT LATITUDE, LONGITUDE FROM (
                    SELECT J.LATITUDE, J.LONGITUDE, J.JOURNEY_DATE AS DATE_ORDER
                    FROM IONV_SYNC.IONVR_ROUTE_JOURNEY J
                    WHERE J.CODVENDEDOR = {0}
                    AND J.JOURNEY_DATE BETWEEN TO_DATE ('{1}','DD-MON-YYYY') AND TO_DATE ('27-DEC-2023','DD-MON-YYYY')
                    AND J.JOURNEY_TYPE = 0
                    AND ROWNUM = 1
                UNION ALL
                    SELECT A.LATITUDE, A.LONGITUDE, A.CHECK_DATE AS DATE_ORDER
                    FROM IONV_SYNC.IONVR_ROUTE_ATTENDANCES A
                    WHERE A.CODVENDEDOR = {0}
                    AND A.CHECK_DATE BETWEEN TO_DATE ('{1}','DD-MON-YYYY') AND TO_DATE ('27-DEC-2023','DD-MON-YYYY')
                    AND A.CHECK_TYPE = 'IN'
                UNION ALL
                    SELECT J.LATITUDE, J.LONGITUDE, J.JOURNEY_DATE AS DATE_ORDER
                    FROM IONV_SYNC.IONVR_ROUTE_JOURNEY J
                    WHERE J.CODVENDEDOR = {0}
                    AND J.JOURNEY_DATE BETWEEN TO_DATE ('{1}','DD-MON-YYYY') AND TO_DATE ('27-DEC-2023','DD-MON-YYYY')
                    AND J.JOURNEY_TYPE = 1
                    AND ROWNUM = 1
                    )
                ORDER BY DATE_ORDER""".format(codvendedor, check_date)
cursor.execute(consulta_sql)

rows = cursor.fetchall()

distancia_total = 0

# Calcular a distância percorrida
for i in range(len(rows) - 1):
    coordenada_atual = f"{rows[i][0]},{rows[i][1]}"  # Coordenadas atuais
    coordenada_proxima = f"{rows[i+1][0]},{rows[i+1][1]}"  # Próximas coordenadas
    distancia_entre_pontos = calcular_distancia_haversine(coordenada_atual, coordenada_proxima)
    distancia_total += distancia_entre_pontos
    
print(f"O vendedor percorreu aproximadamente {distancia_total:.3f} km nessa data.")
