import math

def calcular_distancia_haversine(origem, destino):
    # Função para converter graus para radianos
    def graus_para_radianos(graus):
        return graus * math.pi / 180.0

    # Coordenadas de latitude e longitude dos pontos de origem e destino
    lat1, lon1 = map(float, origem.split(','))
    lat2, lon2 = map(float, destino.split(','))

    # Raio médio da Terra em quilômetros
    raio_terra_km = 6371.0

    # Diferença das latitudes e longitudes em radianos
    diferenca_lat = graus_para_radianos(lat2 - lat1)
    diferenca_lon = graus_para_radianos(lon2 - lon1)

    # Fórmula de Haversine para calcular a distância em linha reta
    a = math.sin(diferenca_lat / 2) ** 2 + math.cos(graus_para_radianos(lat1)) * math.cos(graus_para_radianos(lat2)) * math.sin(diferenca_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = raio_terra_km * c

    return distancia

# Substitua 'latitude,longitude' pelos valores reais das coordenadas
coordenadas_origem = '-3.8068818497080703, -38.583741917489846'  # Exemplo: Latitude e Longitude de Nova York
coordenadas_destino = '-3.8448340666419027, -38.502476647934635'  # Exemplo: Latitude e Longitude de Los Angeles

# Calcula a distância em linha reta
distancia_linha_reta = calcular_distancia_haversine(coordenadas_origem, coordenadas_destino)
print(f"Distância em linha reta entre os pontos: {distancia_linha_reta:.2f} km")
