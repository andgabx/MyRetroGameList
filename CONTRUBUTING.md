# ✨ Guia de Contribuição
## 🔧 Setup Rápido
### Pré-requisitos
  - Python 3.8+
  - pip
  - Git

## Passos

### 1. Clone e ambiente:
   ```
    git clone https://github.com/andgabx/MyRetroGameList/
    cd MyRetroGameList
    python -m venv venv
    
    # Windows
    venv\Scripts\activate
    
    # Linux/MacOS
    source venv/bin/activate
   ```
### 2. Instalação:
   ```
   pip install -r requirements.txt
   ```
### 3. Database:
   ```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```
## 🚀 Como Contribuir

### 1. Atualize seu código:
  ```
  git checkout main
  git pull origin main
  git checkout -b feature/sua-feature
  ```
### 2. Commit e Push:
  ```
  git add .
  git commit -m "feat: adiciona nova feature"
  git push origin feature/sua-feature
  ```

## 🐛 Bugs
Ao reportar bugs, inclua:

- Descrição clara
- Passos para reprodução
- Screenshots (se necessário)
- Ambiente (SO, navegador)

## ❓ Dúvidas?

- Veja a documentação
- Busque issues similares
- Abra uma issue com tag question

---

Obrigado por se interessar em contribiur!
