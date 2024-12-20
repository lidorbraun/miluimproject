const mysql = require("mysql2");

// הגדרת החיבור למסד הנתונים
const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: " ", // עדכן את הסיסמה אם יש צורך
  database: "miluim", // שם מסד הנתונים
});

db.connect((err) => {
  if (err) {
    console.error("Database connection failed:", err.message);
    process.exit(1);
  }
  console.log("Connected to the database successfully!");
});

module.exports = db;
