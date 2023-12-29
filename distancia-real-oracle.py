import requests
import cx_Oracle

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

def calcular_distancia_bing_maps(api_key, origem, destino):
    base_url = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix"

    params = {
        "origins": origem,
        "destinations": destino,
        "travelMode": "driving",
        "key": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'resourceSets' in data and len(data['resourceSets']) > 0:
            results = data['resourceSets'][0]['resources'][0]['results']
            if len(results) > 0:
                distance = results[0]['travelDistance']
                print(origem)
                print(destino)
                print(f"Distância: {distance} Km")
                return distance
                #print(f"Distância entre os pontos: {distance} km")
            else:
                print("Não foi possível calcular a distância.")
        else:
            print("Não foi possível obter os resultados.")
    else:
        print(f"Erro ao calcular a distância: {response.status_code}")
    return 0.0  # Retorna None se a distância não pôde ser calculada


# Substitua 'SUA_CHAVE_DE_API' pela sua chave de API da Bing Maps
api_key = 'x'
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
    distancia_entre_pontos = calcular_distancia_bing_maps(api_key, coordenada_atual, coordenada_proxima)   
    distancia_total += distancia_entre_pontos
    
print(f"O vendedor percorreu aproximadamente {distancia_total:.3f} km nessa data.")