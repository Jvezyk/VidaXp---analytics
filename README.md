# 🌱 Vida Analystics – Assistente de Organização Acadêmica

Projeto desenvolvido para a disciplina de **Programação Orientada a Objetos**, com o objetivo de aplicar conceitos como herança, composição, abstração, modularização, e interface com o usuário. O Projeto se encontra na forma simples, tendo poucas funcionalidades mas com grande chances de ser melhorado no futuro.

---

##  Objetivo

O **Vida Analystics** é um sistema web que permite aos estudantes universitários:

- Organizar tarefas e hábitos acadêmicos
- Visualizar o status das atividades
- Ver o seu desempenho diário por meio de um gráfico
- Marcar itens como concluídos
- Navegar por uma interface limpa e responsiva (desenvolvida com Flask + Bootstrap)

---

##  Conceitos de Orientação a Objetos aplicados

| Conceito OO       | Aplicação no Projeto                    |
|-------------------|------------------------------------------|
| **Abstração**     | Classe abstrata `Atividade`             |
| **Herança**       | `Tarefa` e `Habito` herdam de `Atividade` |
| **Composição**    | `Usuario` possui nome e senha para acessar |
| **Encapsulamento**| Métodos organizados por responsabilidade |
| **Modularização** | Separação clara entre lógica e interface |

---

##  Estrutura do Projeto
```
VidaXp---analytics/
├── main.py   # Aplicação principal (Flask)
├── popular_dados.py # Caso queira ver o gráfico sem esperar os dias
├── Procfile # Arquivo para o Render
├── README.md  # Documentação do projeto
├── requirements.txt  # Dependências
│
├── templates/ # HTML (interface com usuário)
│ ├── base.html
│ ├── criar_usuario.html
│ ├── editar_usuario.html
│ ├── index.html
│ └── login.html
│
├── static/ # CSS (customizado)/JavaScript(Interações)
| ├── dashboard.js
│ └── style.css
│
├── package/ # Lógica do sistema (orientado a objetos)
│ ├── atividades/
│ ├── atividade.py
│ ├── tarefa.py
│ └── habito.py
│
├── instance/ # Banco de dados local (SQL)
└── vidaxp.db
```
---

## Para instalar as bibliotecas necessarias 

`Bash:`

```
pip install -r requirements.txt
```
