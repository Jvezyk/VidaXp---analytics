# 🌱 VidaXP – Assistente de Organização Acadêmica

Projeto desenvolvido para a disciplina de **Programação Orientada a Objetos**, com o objetivo de aplicar conceitos como herança, composição, abstração, modularização, e interface com o usuário.

---

## 🎯 Objetivo

O **VidaXP** é um sistema web que permite aos estudantes universitários:

- Organizar tarefas e hábitos acadêmicos
- Visualizar o status das atividades
- Marcar itens como concluídos
- Navegar por uma interface limpa e responsiva (desenvolvida com Flask + Bootstrap)

---

## 🧠 Conceitos de Orientação a Objetos aplicados

| Conceito OO       | Aplicação no Projeto                    |
|-------------------|------------------------------------------|
| **Abstração**     | Classe abstrata `Atividade`             |
| **Herança**       | `Tarefa` e `Habito` herdam de `Atividade` |
| **Composição**    | `Usuario` possui listas de tarefas/hábitos |
| **Encapsulamento**| Métodos organizados por responsabilidade |
| **Modularização** | Separação clara entre lógica e interface |

---

## 🧱 Estrutura do Projeto

 ``` VidaXp---analytics/ ├── app.py # Aplicação principal (Flask) ├── README.md # Documentação do projeto ├── requirements.txt # Dependências │ ├── templates/ # HTML (interface com usuário) │ ├── base.html │ └── index.html │ ├── static/ # CSS customizado │ └── style.css │ ├── package/ # Lógica do sistema (orientado a objetos) │ ├── usuario.py │ └── atividades/ │ ├── atividade.py │ ├── tarefa.py │ └── habito.py │ ├── instance/ # Banco de dados local(SQL) │ └── vidaxp.db ```  

---

## Para instalar as bibliotecas necessarias 
*Bash:*
pip install -r requirements.txt
