const express = require("express");
const db = require("./server/config/db");
const formController = require("./server/controllers/formController");
const app = express();
const PORT = 3000;

// Middleware לטיפול בנתונים בפורמט JSON
app.use(express.json());

// מסלול לקבלת סטטוס טופס
app.get("/form/:form_id", formController.getFormStatus);

// הפעלת השרת
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

app.post("/form/submit", (req, res) => {
  console.log("Request body:", req.body); // זה ידפיס את הנתונים המתקבלים

  try {
    const { name, email } = req.body;
    db.query(
      "INSERT INTO forms (name, email) VALUES (?, ?)",
      [name, email],
      (err, result) => {
        if (err) {
          console.error("Error inserting data:", err); // הדפס את השגיאה אם יש
          return res.status(500).send("Internal Server Error");
        }
        res.status(200).send("Form submitted successfully");
      }
    );
  } catch (err) {
    console.error("Error:", err); // הדפס את השגיאה אם יש
    res.status(500).send("Internal Server Error");
  }
});
