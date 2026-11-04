const form = document.getElementById("capsule-form");
const formError = document.getElementById("form-error");
const list = document.getElementById("capsule-list");
const emptyText = document.getElementById("empty-text");
const reader = document.getElementById("reader");

// The earliest allowed date is tomorrow (in local time)
function tomorrowString() {
    const d = new Date();
    d.setDate(d.getDate() + 1);
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    return `${d.getFullYear()}-${month}-${day}`;
}
document.getElementById("open_date").min = tomorrowString();

function formatDate(isoDate) {
    return new Date(isoDate + "T00:00:00").toLocaleDateString("en-GB", {
        day: "numeric", month: "long", year: "numeric"
    });
}

async function loadCapsules() {
    const response = await fetch("/api/capsules");
    const capsules = await response.json();

    list.innerHTML = "";
    emptyText.style.display = capsules.length === 0 ? "block" : "none";

    for (const capsule of capsules) {
        list.appendChild(createCapsuleItem(capsule));
    }
}

function createCapsuleItem(capsule) {
    const li = document.createElement("li");
    li.className = capsule.locked ? "capsule locked" : "capsule unlocked";

    const title = document.createElement("h3");
    title.textContent = capsule.title;

    const info = document.createElement("p");
    if (capsule.locked) {
        const dayWord = capsule.days_left === 1 ? "day" : "days";
        info.textContent = `🔒 Opens in ${capsule.days_left} ${dayWord} (${formatDate(capsule.open_date)}) · by ${capsule.author}`;
    } else {
        info.textContent = `🔓 Ready to open · by ${capsule.author}`;
    }

    li.append(title, info);

    if (!capsule.locked) {
        const openBtn = document.createElement("button");
        openBtn.textContent = "Open";
        openBtn.addEventListener("click", () => openCapsule(capsule.id));
        li.appendChild(openBtn);
    }

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.className = "delete-btn";
    deleteBtn.addEventListener("click", () => deleteCapsule(capsule.id));
    li.appendChild(deleteBtn);

    return li;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    formError.textContent = "";

    const newCapsule = {
        title: document.getElementById("title").value,
        author: document.getElementById("author").value,
        message: document.getElementById("message").value,
        open_date: document.getElementById("open_date").value,
    };

    const response = await fetch("/api/capsules", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newCapsule),
    });

    if (!response.ok) {
        const data = await response.json();
        formError.textContent = data.error;
        return;
    }

    form.reset();
    loadCapsules();
});

async function openCapsule(id) {
    const response = await fetch(`/api/capsules/${id}`);
    const data = await response.json();

    if (response.status === 423) {
        alert("This capsule is still locked!");
        return;
    }
    if (!response.ok) {
        alert(data.error);
        return;
    }

    document.getElementById("reader-title").textContent = data.title;
    document.getElementById("reader-meta").textContent =
        `From ${data.author} · sealed on ${formatDate(data.created_at.slice(0, 10))}`;
    document.getElementById("reader-message").textContent = data.message;
    reader.classList.remove("hidden");
}

async function deleteCapsule(id) {
    if (!confirm("Delete this capsule forever?")) return;

    const response = await fetch(`/api/capsules/${id}`, { method: "DELETE" });
    if (!response.ok) {
        const data = await response.json();
        alert(data.error);
    }
    loadCapsules();
}

document.getElementById("reader-close").addEventListener("click", () => {
    reader.classList.add("hidden");
});

loadCapsules();