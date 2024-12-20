document.getElementById("formSubmit").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(e.target);

  try {
    const response = await fetch("/form/submit", {
      method: "POST",
      body: formData,
    });

    const message = await response.text();
    alert(message);
  } catch (error) {
    alert("Error submitting form");
    console.error(error);
  }
});
