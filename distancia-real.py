import requests

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
                print(f"Distância entre os pontos: {distance} km")
            else:
                print("Não foi possível calcular a distância.")
        else:
            print("Não foi possível obter os resultados.")
    else:
        print(f"Erro ao calcular a distância: {response.status_code}")

# Substitua 'SUA_CHAVE_DE_API' pela sua chave de API da Bing Maps
api_key = 'AqXXq_dKNGPf2OCsp3_32GH1zhRpddNKKJ4msNWPdwyk9wJfrRyC14ihDUIbhi4D'

# Substitua 'latitude,longitude' pelos valores reais das coordenadas
coordenadas_origem = '-3.807215564734376, -38.5838596181973'  # Exemplo: Casa Mondubim
coordenadas_destino = '-3.845694312265432, -38.502434012827734'  # Exemplo: Super Supply

calcular_distancia_bing_maps(api_key, coordenadas_origem, coordenadas_destino)

