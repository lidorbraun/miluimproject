const mysql = require("mysql2");

const db = mysql.createConnection({
  host: "localhost",
  user: "root", // שם המשתמש
  password: "", // הסיסמה שלך
  database: "miluim", // שם מסד הנתונים שלך
});

db.connect((err) => {
  if (err) {
    console.error("Database connection failed:", err.message);
    process.exit(1);
  }
  console.log("Connected to the database");
});

module.exports = db;
