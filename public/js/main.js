document
  .getElementById("formSubmission")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    // אסוף את הנתונים מהטופס
    const formData = new FormData();
    formData.append("form_name", document.getElementById("form_name").value);
    formData.append("message", document.getElementById("message").value);
    formData.append("file", document.getElementById("file").files[0]);

    try {
      // שלח את הנתונים לשרת
      const response = await fetch("/form/submit", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      if (response.ok) {
        alert(`Success: ${result.message}`);
      } else {
        alert(`Error: ${result.message}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  });
