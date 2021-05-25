from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app import ml, viz, plotly

app = FastAPI(
    title='Spotifinder',
    description="Find the next best song for you based on your personal tastes and preferences",
    docs_url='/',
)

app.include_router(plotly.router, tags=['Machine Learning'])
app.include_router(viz.router, tags=['Visualization'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)

