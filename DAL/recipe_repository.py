from DB.connection import get_connection
from DAL.models import Recipe


def get_all_recipes_DAL():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Recipes"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    # המרה ל-Pydantic
    return [Recipe(id=row[0], name=row[1], category=row[2], ingredients=row[3], instructions=row[4], prep_time=row[5])
            for row in rows]


def get_recipe_by_id_DAL(recipe_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Recipes WHERE id = ?"
    cursor.execute(query, (recipe_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return Recipe(id=row[0], name=row[1], category=row[2], ingredients=row[3], instructions=row[4], prep_time=row[5])


def get_recipe_by_category_DAL(category):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Recipes WHERE category = ?"
    cursor.execute(query, (category,))
    rows = cursor.fetchall()
    conn.close()

    return [Recipe(id=row[0], name=row[1], category=row[2], ingredients=row[3], instructions=row[4], prep_time=row[5])
            for row in rows]


def create_recipe_DAL(recipe):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO Recipes (name, category, ingredients, instructions, prep_time)
    VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(query, (
        recipe.name,
        recipe.category,
        recipe.ingredients,
        recipe.instructions,
        recipe.prep_time
    ))
    conn.commit()
    conn.close()
    return recipe


def update_recipe_DAL(recipe):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE Recipes SET name = ?, category = ?, ingredients = ?, instructions = ?, prep_time = ? WHERE id = ?"
    cursor.execute(query, (recipe.name,
                           recipe.category,
                           recipe.ingredients,
                           recipe.instructions,
                           recipe.prep_time,
                           recipe.id))
    conn.commit()
    conn.close()
    return recipe

def delete_recipe_DAL(Recipes_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Recipes WHERE id = ?"
    cursor.execute(query, (Recipes_id,))
    conn.commit()
    conn.close()
    return {"message": "Recipe deleted successfully"}




