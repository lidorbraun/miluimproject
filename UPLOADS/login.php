<!DOCTYPE html>
<html lang="he">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>התחברות למערכת</title>
</head>
<body>
    <h1>התחברות למערכת</h1>
    <form action="process_login.php" method="POST">
        <label for="username">שם משתמש:</label>
        <input type="text" name="username" id="username" required><br><br>
        <label for="password">סיסמה:</label>
        <input type="password" name="password" id="password" required><br><br>
        <button type="submit">התחבר</button>
    </form>
</body>
</html>
