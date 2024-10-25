import requests as r

while True:
    print(f"""
        {"-"*30}
        Sistema de análise de dados
        {"-"*30}

        Qual query você deseja analisar?
        [1] Qual foi o total de receitas no ano de 1997
        [2] Valor total que cada cliente já pagou até agora
        [3] Identifica os 10 produtos mais vendidos
        [4] Quais clientes do Reino Unido pagaram mais de 1000 dólares
        [5] Separar os clientes em 5 grupos de acordo com o valor pago por cliente
        [6] SAIR
    """)
    response_input = int(input("Resposta: "))
    if response_input == 1:
            response = r.get("http://127.0.0.1:8000/total_receitas_ano")
            print(response.json().get("data"))
    elif response_input == 2:
            response = r.get("http://127.0.0.1:8000/valor_pago_por_cliente")
            print(response.json().get("data"))
    elif response_input == 3:
            response = r.get("http://127.0.0.1:8000/Produtos_mais_vendidos")
            print(response.json().get("data"))
    elif response_input == 4:
            response = r.get("http://127.0.0.1:8000/clientes_do_Reino_Unido_pagaram_mais_de_1000_dólares")
            print(response.json().get("data"))
    elif response_input == 5:
            response = r.get("http://127.0.0.1:8000/valor_pago_por_cliente_agrupado")
            print(response.json().get("data"))
    elif response_input == 6:
        break
    else:
        print("Resposta inválida, tente novamente")