
document.addEventListener("DOMContentLoaded", function() {
    const uploadForm = document.getElementById("uploadForm");
    const message = document.getElementById("message");

    uploadForm.addEventListener("submit", async function(event) {
        event.preventDefault();  // Prevent default form submission

        let formData = new FormData();
        formData.append("subject", document.getElementById("subject").value);
        formData.append("topic", document.getElementById("topic").value);
        formData.append("file", document.getElementById("file").files[0]);

        const token = localStorage.getItem("authToken"); // Ensure the user is authenticated

        if (!token) {
            message.textContent = "You must be logged in to upload notes.";
            message.style.color = "red";
            return;
        }

        try {
            let response = await fetch("/api/notes/upload/", {
                method: "POST",
                body: formData,
                headers: {
                    "Authorization": `Bearer ${token}` // Include JWT token or session auth
                }
            });

            let result = await response.json();
            if (response.ok) {
                message.textContent = "Note uploaded successfully!";
                message.style.color = "green";
                uploadForm.reset();
            } else {
                message.textContent = "Error: " + JSON.stringify(result);
                message.style.color = "red";
            }
        } catch (error) {
            message.textContent = "Failed to upload note. Try again.";
            message.style.color = "red";
        }
    });
});

document.getElementById("viewNotes").addEventListener("click", async function() {
    const token = localStorage.getItem("authToken");
    if (!token) {
        alert("You must be logged in to view notes.");
        return;
    }

    let response = await fetch("/api/notes/", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    let notes = await response.json();
    let notesList = document.getElementById("notesList");
    notesList.innerHTML = ""; // Clear previous notes

    notes.forEach(note => {
        let listItem = document.createElement("li");
        listItem.innerHTML = `<strong>${note.subject} - ${note.topic}</strong> 
            <a href="${note.file}" target="_blank">Download</a>`;
        notesList.appendChild(listItem);
    });
});

