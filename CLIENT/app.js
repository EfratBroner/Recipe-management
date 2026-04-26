const API_BASE = "http://localhost:8001";

// --- טעינת קטגוריות מהשרת ---
async function loadCategories() {
    const res = await fetch(`${API_BASE}/recipes/`);
    const data = await res.json();

    const categories = [...new Set(data.map(r => r.category))];

    const select = document.getElementById("category-filter");
    select.innerHTML = `<option value="all">סינון לפי קטגוריה</option>`;

    categories.forEach(cat => {
        const opt = document.createElement("option");
        opt.value = cat;
        opt.textContent = cat;
        select.appendChild(opt);
    });
}

// --- טעינת מתכונים מהשרת ---
async function loadRecipes(category = "all") {
    let url = `${API_BASE}/recipes/`;

    if (category !== "all") {
        url = `${API_BASE}/recipes/category/${category}`;
    }

    const res = await fetch(url);
    const data = await res.json();

    const list = document.getElementById("recipes-list");
    list.innerHTML = "";

    data.forEach(r => {
        const card = document.createElement("li");
        card.className = "recipe-card";

        card.innerHTML = `
            <div class="recipe-title">${r.name} (${r.category})</div>

            <div class="recipe-details">
                <p><strong>רכיבים:</strong> ${r.ingredients}</p>
                <p><strong>הוראות:</strong> ${r.instructions}</p>
                <p><strong>זמן הכנה:</strong> ${r.prep_time} דקות</p>

                <button class="edit-btn" data-id="${r.id}">ערוך</button>
                <button class="delete-btn" data-id="${r.id}">מחק</button>
            </div>
        `;

        card.addEventListener("click", (e) => {
            if (e.target.classList.contains("delete-btn")) return;
            if (e.target.classList.contains("edit-btn")) return;

            const details = card.querySelector(".recipe-details");
            details.style.display = details.style.display === "block" ? "none" : "block";
        });

        list.appendChild(card);
    });
}

// --- מחיקה ---
document.getElementById("recipes-list").addEventListener("click", async (e) => {
    if (e.target.classList.contains("delete-btn")) {
        const id = e.target.dataset.id;

        await fetch(`${API_BASE}/recipes/${id}`, { method: "DELETE" });

        loadRecipes(document.getElementById("category-filter").value);
        loadCategories();
    }
});

// --- עריכה: פתיחת חלון ---
document.getElementById("recipes-list").addEventListener("click", async (e) => {
    if (e.target.classList.contains("edit-btn")) {
        const id = e.target.dataset.id;

        const res = await fetch(`${API_BASE}/recipes/${id}`);
        const r = await res.json();

        document.getElementById("edit-id").value = r.id;
        document.getElementById("edit-name").value = r.name;
        document.getElementById("edit-category").value = r.category;
        document.getElementById("edit-ingredients").value = r.ingredients;
        document.getElementById("edit-instructions").value = r.instructions;
        document.getElementById("edit-prep").value = r.prep_time;

        document.getElementById("edit-modal").style.display = "block";
    }
});

// --- שמירת עריכה ---
document.getElementById("save-edit-btn").addEventListener("click", async () => {
    const id = document.getElementById("edit-id").value;

    await fetch(`${API_BASE}/recipes/`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id,
            name: document.getElementById("edit-name").value,
            category: document.getElementById("edit-category").value,
            ingredients: document.getElementById("edit-ingredients").value,
            instructions: document.getElementById("edit-instructions").value,
            prep_time: parseInt(document.getElementById("edit-prep").value)
        })
    });

    document.getElementById("edit-modal").style.display = "none";
    loadRecipes();
});

// --- סגירת חלון עריכה ---
document.getElementById("close-edit-btn").addEventListener("click", () => {
    document.getElementById("edit-modal").style.display = "none";
});

// --- הוספת מתכון ---
document.getElementById("add-recipe-btn").addEventListener("click", async () => {
    await fetch(`${API_BASE}/recipes/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: document.getElementById("recipe-name").value,
            category: document.getElementById("recipe-category").value,
            ingredients: document.getElementById("recipe-ingredients").value,
            instructions: document.getElementById("recipe-instructions").value,
            prep_time: parseInt(document.getElementById("recipe-prep-time").value)
        })
    });

    loadRecipes();
    loadCategories();
});

// --- שאלת AI ---
document.getElementById("ask-ai-btn").addEventListener("click", async () => {
    const q = document.getElementById("ai-question").value;

    const res = await fetch(`${API_BASE}/recipes/ask_ai?question=${encodeURIComponent(q)}`);
    const data = await res.json();

    document.getElementById("ai-answer").textContent = data.answer;
});

// --- סינון ---
document.getElementById("category-filter").addEventListener("change", (e) => {
    loadRecipes(e.target.value);
});

// --- הצג הכול ---
document.getElementById("show-all-btn").addEventListener("click", () => {
    document.getElementById("category-filter").value = "all";
    loadRecipes();
});

// --- הפעלה ראשונית ---
loadCategories();
loadRecipes();
