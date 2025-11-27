from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)  # Isso libera o acesso para o React (que roda em outra porta)

# --- 1. Carregar o Cérebro da IA ---
print("Carregando modelo e encoders...")
modelo = joblib.load('modelo_carros.pkl')
encoders = joblib.load('encoders.pkl')
print("Sistema pronto!")


# --- 2. Rota de Previsão (O Endpoint) ---
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Recebe os dados enviados pelo Front-end (JSON)
        dados = request.get_json()

        # Exemplo de como os dados chegam:
        # {"Brand": "Honda", "Model": "Civic", "Year": 2020, ...}

        # Transformar o JSON em um DataFrame (tabela)
        df_input = pd.DataFrame([dados])

        # --- Pré-processamento igual ao do Treinamento ---
        # Temos que converter texto para número usando os mesmos encoders
        colunas_categoricas = ['Brand', 'Model', 'Fuel_Type', 'Transmission']

        for col in colunas_categoricas:
            # Pegamos o valor que veio do site
            valor_texto = df_input[col].iloc[0]

            # Precisamos do encoder específico dessa coluna
            le = encoders[col]

            # Tentamos converter. Se for uma marca que a IA nunca viu,
            # isso daria erro. Aqui vamos assumir que o Front só manda opções válidas.
            if valor_texto in le.classes_:
                df_input[col] = le.transform(df_input[col])
            else:
                # Fallback: se não conhece a marca, usa a primeira da lista (ou trate como erro)
                # Para o trabalho acadêmico, isso evita crashar na demo.
                df_input[col] = 0

                # --- Fazer a Previsão ---
        preco_estimado = modelo.predict(df_input)

        # O resultado é um array (ex: [25000.50]). Pegamos o primeiro valor.
        resultado = float(preco_estimado[0])

        return jsonify({
            'sucesso': True,
            'preco_previsto': f"{resultado:.2f}",
            'mensagem': 'Cálculo realizado com sucesso!'
        })

    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500


# --- 3. Rodar o Servidor ---
if __name__ == '__main__':
    # debug=True faz o servidor reiniciar se você mudar o código
    app.run(port=5000, debug=True)