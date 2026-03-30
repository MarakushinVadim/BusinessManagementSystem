from fastapi import FastAPI

app = FastAPI(
    title='Business Management System'
)


@app.get('/')
async def get_main():
    return {'message': 'hello'}