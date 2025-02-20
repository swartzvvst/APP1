# APP1

Descrição do repositório.

## Estrutura do Projeto

```plaintext
meu_site/
├── app.py
├── templates/
│   ├── home.html
│   ├── materia.html
│   ├── afc.html
│   ├── respostas.html
├── static/
│   └── styles.css
└── README.md
```

## Arquivos do Projeto

### app.py
```python
from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
import os

app = Flask(__name__)

ARQUIVO_RESPOSTAS = "respostas.json"
MATERIAS = ["biologia", "matematica", "historia", "geografia", "portugues", "ingles", "quimica", "fisica"]
AFC_NUMEROS = [f"AFC{i}" for i in range(1, 11)]

# Função para carregar respostas
def carregar_respostas():
    if os.path.exists(ARQUIVO_RESPOSTAS):
        with open(ARQUIVO_RESPOSTAS, "r") as file:
            return json.load(file)
    return {}

# Função para salvar respostas
def salvar_respostas(respostas):
    with open(ARQUIVO_RESPOSTAS, "w") as file:
        json.dump(respostas, file, indent=4)

# Página inicial
@app.route("/")
def home():
    return render_template('home.html', materias=MATERIAS)

# Página de cada matéria com AFCs
@app.route("/<materia>")
def materia_page(materia):
    if materia not in MATERIAS:
        return "Matéria não encontrada.", 404
    return render_template('materia.html', materia=materia, afcs=AFC_NUMEROS)

# Página de respostas de cada AFC
@app.route("/<materia>/<afc>", methods=["GET", "POST"])
def afc_page(materia, afc):
    if materia not in MATERIAS or afc not in AFC_NUMEROS:
        return "Página não encontrada.", 404
    
    respostas = carregar_respostas().get(materia, {}).get(afc, {})
    if request.method == "POST":
        dados = request.form.to_dict()
        respostas.update(dados)
        data = carregar_respostas()
        if materia not in data:
            data[materia] = {}
        data[materia][afc] = respostas
        salvar_respostas(data)
        return redirect(url_for('respostas_page'))
    
    return render_template('afc.html', materia=materia, afc=afc, respostas=respostas)

# Página de respostas (nova rota)
@app.route("/respostas")
def respostas_page():
    respostas = carregar_respostas()
    return render_template('respostas.html', respostas=respostas)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
```

### templates/home.html
```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Plataforma de Respostas</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <h1>Escolha uma Matéria</h1>
    <div class="container">
        {% for materia in materias %}
            <a href="/{{ materia }}"><button class="btn">{{ materia.capitalize() }}</button></a>
        {% endfor %}
    </div>
</body>
</html>
```

### templates/materia.html
```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>{{ materia.capitalize() }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <h1>{{ materia.capitalize() }}</h1>
    <div class="container">
        {% for afc in afcs %}
            <a href="/{{ materia }}/{{ afc }}"><button class="btn">{{ afc }}</button></a>
        {% endfor %}
    </div>
</body>
</html>
```

### templates/afc.html
```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>{{ materia.capitalize() }} - {{ afc }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <h1>{{ materia.capitalize() }} - {{ afc }}</h1>
    <form action="" method="post">
        {% for i in range(1, 11) %}
            <label>Resposta da Questão {{ i }}:</label>
            <input type="text" name="Questão {{ i }}" value="{{ respostas.get('Questão ' ~ i, '') }}"><br>
        {% endfor %}
        <button type="submit" class="btn">Salvar Respostas</button>
    </form>
    <h2>Respostas Salvas</h2>
    {% for i in range(1, 11) %}
        <p>Resposta da Questão {{ i }}: {{ respostas.get('Questão ' ~ i, 'Nenhuma resposta salva.') }}</p>
    {% endfor %}
    <a href="/respostas"><button class="btn">Página de Respostas</button></a>
</body>
</html>
```

### templates/respostas.html
```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Página de Respostas</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <h1>Página de Respostas</h1>
    <div class="container">
        {% for materia, afcs in respostas.items() %}
            <h2>{{ materia.capitalize() }}</h2>
            {% for afc, resposta in afcs.items() %}
                <h3>{{ afc }}</h3>
                {% for i in range(1, 11) %}
                    <p>Resposta da Questão {{ i }}: {{ resposta.get('Questão ' ~ i, 'Nenhuma resposta salva.') }}</p>
                {% endfor %}
            {% endfor %}
        {% endfor %}
    </div>
</body>
</html>
```

### static/styles.css
```css
body { 
    background-image: url("https://i2.wp.com/multarte.com.br/wp-content/uploads/2018/12/fundo-roxo-escuro19.png?fit=1920%2C1080&ssl=1"); 
    background-size: cover; 
    color: white; 
    text-align: center; 
    font-family: Arial, sans-serif;
}

.container { 
    margin-top: 50px; 
}

.btn { 
    padding: 15px 30px; 
    margin: 10px; 
    background: linear-gradient(45deg, #7a1b8d, #9a2f5b);
    color: white; 
    border: none; 
    cursor: pointer;
    font-size: 18px;
    border-radius: 8px;
    transition: 0.3s;
}

.btn:hover { 
    background: linear-gradient(45deg, #9a2f5b, #7a1b8d); 
}
```


    
