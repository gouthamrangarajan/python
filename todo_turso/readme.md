#### to run the app
- pip install -r requirements.txt
- uvicorn main:app --reload
- npx tailwindcss -i ./tailwind/input.css -o ./assets/app.css --watch. Check [tailwindcli](https://tailwindcss.com/docs/installation) for further information      
- create .env file with TURSO_DATABASE_URL & TURSO_AUTH_TOKEN entries. Check [Turso](https://docs.turso.tech/sdk/python/quickstart) for further information