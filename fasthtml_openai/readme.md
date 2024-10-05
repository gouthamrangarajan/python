#### to run the app
- ```pip install -r requirements.txt```
- 1<sup>st</sup> terminal ```uvicorn main:app --reload```
- 2<sup>nd</sup> terminal ```npx tailwindcss -i ./tailwind/input.css -o ./assets/app.css --watch```. Check [tailwindcli](https://tailwindcss.com/docs/installation) for further information      
- create .env file with the below entries
    - OPENAI_API_KEY
    - OPENAI_API_MODEL