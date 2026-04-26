from fastapi import FastAPI, APIRouter, HTTPException
from DAL import recipe_repository
from fastapi import Query
from DAL.models import Recipe
import google.generativeai as genai



router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.get("/")
def read_all_recipes():
    return recipe_repository.get_all_recipes_DAL()


genai.configure(api_key="AIzaSyBqibMJRtiDbNvRHeJkD9rqAB5MYh9um8E")

print("--- בודק מודלים זמינים... ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"מודל שאפשר להשתמש בו: {m.name}")
except Exception as e:
    print(f"שגיאה בשליפת מודלים: {e}")
print("----------------------------")

model = genai.GenerativeModel('gemini-flash-latest')


@router.get("/ask_ai")
async def ask_ai(question: str = Query(..., description="השאלה של המשתמש")):
    try:
        # כאן אנחנו מגדירים את ה"גבולות" של המודל
        system_instruction = """
        אתה עוזר מטבח ומומחה לאפייה ובישול בלבד. 
        1. ענה אך ורק על שאלות הקשורות למתכונים, טכניקות בישול, תחליפי רכיבים או אפייה.
        2. אם המשתמש שואל על נושא אחר (פוליטיקה, היסטוריה, מדע, עניינים אישיים וכו'), 
           ענה בנימוס: "אני מתמחה בבישול ואפייה בלבד, אשמח לעזור לך במטבח!"
        3. ענה בקצרה ובעברית.
        """

        # שילוב ההנחיה עם השאלה
        full_prompt = f"{system_instruction}\n\nהשאלה של המשתמש: {question}"

        response = model.generate_content(full_prompt)
        return {"answer": response.text}

    except Exception as e:
        print(f"AI Error: {e}")
        return {"answer": "מצטער, השף עסוק כרגע."}





@router.get("/category/{category}")
def read_by_category(category: str):
    return recipe_repository.get_recipe_by_category_DAL(category)

@router.get("/{recipe_id}")
def read_recipe_by_id(recipe_id: int):
    recipe = recipe_repository.get_recipe_by_id_DAL(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post("/")
def add_recipe(recipe: Recipe):
    if recipe is None:
        raise HTTPException(status_code=400, detail="לא התקבלו נתוני מתכון בבקשה.")

    if not recipe.name or recipe.name.strip() == "":
        raise HTTPException(status_code=400, detail="שם המתכון הוא שדה חובה ולא יכול להיות ריק.")

    if not recipe.category or recipe.category.strip() == "":
        raise HTTPException(status_code=400, detail="יש להזין קטגוריה עבור המתכון.")

    if not recipe.ingredients or recipe.ingredients.strip() == "":
        raise HTTPException(status_code=400, detail="רשימת הרכיבים חסרה. יש להזין לפחות רכיב אחד.")

    if not recipe.instructions or recipe.instructions.strip() == "":
        raise HTTPException(status_code=400, detail="הוראות ההכנה חסרות. יש להסביר איך מכינים את המנה.")

    if recipe.prep_time <= 0:
        raise HTTPException(status_code=400, detail="זמן ההכנה קטן מהזמן המינימלי.")

    return recipe_repository.create_recipe_DAL(recipe)
@router.put("/")
def edit_recipe( recipe: Recipe):
    return recipe_repository.update_recipe_DAL(recipe)

@router.delete("/{recipe_id}")
def remove_recipe(recipe_id: int):
    if recipe_id is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe_repository.delete_recipe_DAL(recipe_id)



