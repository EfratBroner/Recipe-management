# Recipe Project - שרת מתכונים

פרויקט זה הוא **שרת FastAPI להצגת מתכונים**, עם יכולת CRUD מלאה (יצירה, קריאה, עדכון, מחיקה) לכל המתכונים, וחיבור אפשרי ל-Gemini API לקבלת תשובות לשאלות בתחום האפייה.

--

## מבנה הפרויקט

recipe_project/

│

├─ db/

│   └─ recipes.json           # קובץ הנתונים

├─ dal/

│   └─ recipes_dal.py         # פונקציות גישה ל-DB

├─ api/

│   └─ main.py                # שרת FastAPI עם נקודות קצה

├─ client/

│   └─ client_example.py      # קוד צד לקוח

├─ requirements.txt           # ספריות נדרשות

└─ README.md                  # מדריך זה