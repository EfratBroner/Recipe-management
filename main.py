from API import  recipe_service
from fastapi.middleware.cors import CORSMiddleware  # <-- להוסיף את זה
from fastapi import FastAPI
from API.recipe_service import router

app = FastAPI()


# --- הוספת הגדרות ה-CORS ---
# זה החלק שחסר לך:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # מאפשר גישה מכל מקור (כולל הקובץ המקומי שלך)
    allow_credentials=True,
    allow_methods=["*"],      # מאפשר את כל סוגי הפעולות (GET, POST וכו')
    allow_headers=["*"],      # מאפשר את כל סוגי ה-Headers
)


# מחברים את ה-router של recipes
app.include_router(router)

# אופציונלי – בדיקה בסיסית
@app.get("/")
def root():
    return {"message": "API is working"}

