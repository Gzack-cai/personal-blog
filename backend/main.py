# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import routers.profile
import routers.projects
import routers.articles
import routers.life
import routers.friends
import routers.contact

try:
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表已就绪")
except Exception as e:
    print(f"⚠️ 数据库连接失败: {e}")
    print("   请确保 MySQL 已启动并执行了 sql/init.sql")

app = FastAPI(title="Personal Blog API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.profile.router, prefix="/api", tags=["Profile"])
app.include_router(routers.projects.router, prefix="/api", tags=["Projects"])
app.include_router(routers.articles.router, prefix="/api", tags=["Articles"])
app.include_router(routers.life.router, prefix="/api", tags=["Life"])
app.include_router(routers.friends.router, prefix="/api", tags=["Friends"])
app.include_router(routers.contact.router, prefix="/api", tags=["Contact"])


@app.get("/")
def root():
    return {"message": "Personal Blog API is running", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
