const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const db = require("./server/config/db"); // חיבור למסד הנתונים
const app = express();
const PORT = 3000;

// Middleware לטיפול בבקשות JSON
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// הגדרת קבצים סטטיים
app.use(express.static(path.join(__dirname, "public")));

// יצירת תיקיית העלאות אם היא לא קיימת
if (!fs.existsSync("uploads")) {
  fs.mkdirSync("uploads");
}

// הגדרת אחסון למסמכים
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "uploads/");
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname));
  },
});

const upload = multer({ storage });

// נתיב לשמירת טופס עם העלאת קובץ
app.post("/form/submit", upload.single("file"), (req, res) => {
  console.log("Request body:", req.body); // הדפסת גוף הבקשה
  console.log("Uploaded file:", req.file); // הדפסת פרטי הקובץ שהועלה

  const { user_id, form_name, description } = req.body;

  if (!user_id || !form_name) {
    console.error("Missing required fields: user_id and form_name");
    return res
      .status(400)
      .send("Missing required fields: user_id and form_name");
  }

  db.query(
    "INSERT INTO forms (user_id, form_name, description, file_path, status) VALUES (?, ?, ?, ?, ?)",
    [
      user_id,
      form_name,
      description,
      req.file ? req.file.path : null,
      "pending",
    ],
    (err, result) => {
      if (err) {
        console.error("Error inserting form data:", err);
        return res.status(500).send("Error submitting form");
      }
      console.log("Form submitted successfully:", result);
      res.status(201).send("Form submitted successfully");
    }
  );
});

// הפעלת השרת
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
