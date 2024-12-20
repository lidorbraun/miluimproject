<<<<<<< HEAD
<<<<<<< HEAD
// לוגיקה עסקית של השרת
=======
const db = require("../config/db");

// פונקציה להגיש טופס
const submitForm = (req, res) => {
  const { user_id, form_name } = req.body;

  const query = "INSERT INTO forms (user_id, form_name) VALUES (?, ?)";
  db.query(query, [user_id, form_name], (err, results) => {
    if (err) {
      console.error("Error submitting form:", err);
      return res.status(500).send("Error submitting form");
    }
    res.status(201).send("Form submitted successfully");
  });
};

// פונקציה לבדוק את סטטוס הטופס
const getFormStatus = (req, res) => {
  const { form_id } = req.params;

  const query = "SELECT * FROM forms WHERE id = ?";
  db.query(query, [form_id], (err, results) => {
    if (err) {
      console.error("Error fetching form status:", err);
      return res.status(500).send("Error fetching form status");
    }
    res.json(results);
  });
};

module.exports = { submitForm, getFormStatus };
>>>>>>> master
=======
>>>>>>> 4cd7ab616d070fe31d2b76f8dd8fa6d76a23d5b8
