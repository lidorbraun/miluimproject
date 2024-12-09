<!DOCTYPE html>
<html lang="he">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>מילוי טופס חדש</title>
</head>
<body>
    <h1>מלא טופס חדש</h1>
    <form action="submit_form.php" method="POST" enctype="multipart/form-data">
        <label for="form_type">בחר סוג טופס:</label>
        <select name="form_type" id="form_type">
            <option value="travel_reimbursement">החזר נסיעות</option>
            <option value="special_exam_request">בקשה למועד מיוחד</option>
        </select><br><br>
        <label for="document">העלה מסמך:</label>
        <input type="file" name="document" id="document"><br><br>
        <button type="submit">שלח טופס</button>
    </form>
</body>
</html>
