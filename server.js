// סרבר
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

// סטטי לשימוש בקבצי frontend
app.use(express.static("public"));

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

// נתיב לשמירת טופס
app.post("/form/submit", upload.single("file"), (req, res) => {
  const { user_id, form_name, description } = req.body;
  // בדיקה
  if (!user_id || !form_name) {
    return res
      .status(400)
      .send("Missing required fields: user_id and form_name");
  }

  const filePath = req.file ? req.file.path : null;

  db.query(
    "INSERT INTO forms (user_id, form_name, description, file_path, status, submission_date) VALUES (?, ?, ?, ?, 'pending', NOW())",
    [user_id, form_name, description, filePath],
    (err, result) => {
      if (err) {
        console.error("Error inserting form data:", err);
        return res.status(500).send("Error submitting form");
      }
      res.status(201).send("Form submitted successfully");
    }
  );
});

// נתיב להחזרת סטטוס טפסים לפי משתמש
app.get("/form/status/:user_id", (req, res) => {
  const user_id = req.params.user_id;

  db.query(
    "SELECT id, form_name, status, submission_date, description, file_path FROM forms WHERE user_id = ?",
    [user_id],
    (err, results) => {
      if (err) {
        console.error("Error fetching form data:", err);
        return res.status(500).send("Error fetching form data");
      }
      res.status(200).json(results);
    }
  );
});

// נתיב להחזרת היסטוריית טפסים לפי משתמש
app.get("/form/history/:user_id", (req, res) => {
  const user_id = req.params.user_id;
  const { date, status } = req.query;

  let query =
    "SELECT id, form_name, status, submission_date, description, file_path FROM forms WHERE user_id = ?";
  let queryParams = [user_id];

  if (date) {
    query += " AND DATE(submission_date) = ?";
    queryParams.push(date);
  }

  if (status) {
    query += " AND status = ?";
    queryParams.push(status);
  }

  db.query(query, queryParams, (err, results) => {
    if (err) {
      console.error("Error fetching form history:", err);
      return res.status(500).send("Error fetching form history");
    }
    res.status(200).json(results);
  });
});

// הפעלת השרת
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
