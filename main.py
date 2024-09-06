import uvicorn
from config.globals import PORT,HOST

app_name = 'app.main:app'

if __name__ == '__main__':
    uvicorn.run(app_name,host="0.0.0.0",port=int(PORT),reload=True)