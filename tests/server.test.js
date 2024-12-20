const request = require("supertest");
const app = require("../server/server"); // חיבור לקובץ השרת שלך

// בדיקה על טופס ריק
describe("POST /form/submit", () => {
  it("should return an error if the form is empty", async () => {
    const response = await request(app).post("/form/submit").send({}); // שולח בקשה עם אובייקט ריק

    expect(response.status).toBe(400);
    expect(response.text).toBe(
      "Missing required fields: user_id and form_name"
    );
  });
});

// בדיקה על סטטוס טופס
describe("GET /form/status/:user_id", () => {
  it('should return at least one form with status "approved"', async () => {
    const response = await request(app).get("/form/status/1"); // בודקים את הסטטוס של טפסים למשתמש עם מזהה 1

    expect(response.status).toBe(200); // מצפה לסטטוס 200 (OK)
    const forms = response.body;

    // מצפה למצוא לפחות טופס אחד עם סטטוס "approved"
    const approvedForm = forms.find((form) => form.status === "approved");
    expect(approvedForm).toBeDefined(); // לוודא שמצאנו טופס מאושר
  });
});

// בדיקה על היסטוריית טפסים
describe("GET /form/history/:user_id", () => {
  it("should return at least one form in the history for the given user_id", async () => {
    const response = await request(app).get("/form/history/1");

    expect(response.status).toBe(200);
    const forms = response.body;

    // לבדוק שההיסטוריה מכילה לפחות טופס אחד
    expect(forms.length).toBeGreaterThan(0);
  });

  it("should return an empty array if no forms exist for the given user_id", async () => {
    const response = await request(app).get("/form/history/999");

    // מצפה שההיסטוריה תהיה ריקה במקרה הזה
    expect(response.status).toBe(200); // מצפה לסטטוס 200 (OK)
    expect(response.body).toEqual([]); // המערך של ההיסטוריה צריך להיות ריק
  });

  // בדיקות Codex
  it("should ensure that the history contains at least one form for valid user_id", async () => {
    const response = await request(app).get("/form/history/1");

    expect(response.status).toBe(200);
    const forms = response.body;
    expect(forms.length).toBeGreaterThan(0); // לוודא שההיסטוריה לא ריקה
  });

  it("should return empty history for invalid user_id", async () => {
    const response = await request(app).get("/form/history/999");

    expect(response.status).toBe(200);
    expect(response.body).toEqual([]); // אין טפסים למשתמש זה
  });

  it("should display a proper message if no forms are found for the given user", async () => {
    // במקרה שבו אין טפסים, המערכת צריכה להחזיר הודעה מתאימה
    const response = await request(app).get("/form/history/999");

    expect(response.status).toBe(200);
    const message = response.body.message; // אם יש הודעה
    expect(message).toBe("No forms found for this user");
  });
});

// **בדיקות Detox**

describe("Submit form successfully", () => {
  it("should fill in the form and submit successfully", async () => {
    // מילוי שדות הקלט
    await expect(element(by.id("user_id"))).toBeVisible();
    await element(by.id("user_id")).typeText("12345"); // לדוגמה, מזהה המשתמש
    await element(by.id("form_name")).typeText("Test Form");
    await element(by.id("description")).typeText("Description for the form");

    // שליחת הטופס
    await element(by.id("submit_button")).tap(); // כפתור השליחה

    // מצפה שהמערכת תראה הודעה שהטופס נשלח בהצלחה
    await expect(element(by.text("Form submitted successfully"))).toBeVisible();
  });
});

describe("Submit form with missing fields", () => {
  it("should show an error if required fields are missing", async () => {
    // שליחת טופס ריק (לא ממלאים את השדות)
    await element(by.id("submit_button")).tap();

    // מצפה להודעת שגיאה על שדות חסרים
    await expect(
      element(by.text("Missing required fields: user_id and form_name"))
    ).toBeVisible();
  });
});

describe("Submit form with invalid data", () => {
  it("should show an error if user_id is invalid", async () => {
    // מילוי שדות עם נתונים לא חוקיים
    await expect(element(by.id("user_id"))).toBeVisible();
    await element(by.id("user_id")).typeText("invalid_id"); // נתון לא חוקי
    await element(by.id("form_name")).typeText("Test Form");

    // שליחת הטופס
    await element(by.id("submit_button")).tap();

    // מצפה להודעת שגיאה על מזהה לא חוקי
    await expect(element(by.text("Invalid user_id provided"))).toBeVisible();
  });
});

// **בדיקות Cypress - מעקב סטטוס טפסים**

describe("Form Status - Approved", () => {
  it('should display at least one form with status "approved"', () => {
    cy.visit("/form/status/1");

    // מצפה שהמערכת תחזיר לפחות טופס אחד עם סטטוס "Approved"
    cy.get(".form-item").should("have.length.greaterThan", 0); // לפחות טופס אחד מוצג
    cy.get(".form-status").contains("Approved").should("be.visible");
  });
});

describe("Form Status - No Approved Forms", () => {
  it('should not display a form with status "approved" if no forms are approved', () => {
    cy.visit("/form/status/2");

    // מצפה שהמערכת לא תציג שום טופס עם סטטוס "Approved"
    cy.get(".form-item").should("have.length.greaterThan", 0);
    cy.get(".form-status").contains("Approved").should("not.exist"); // לא אמור להיות טופס עם סטטוס זה
  });
});

describe("Form Status - No Forms", () => {
  it("should display a message when no forms are found for the given user", () => {
    cy.visit("/form/status/999"); // נניח שאין טפסים למשתמש עם ID = 999

    // מצפה שהמערכת תציג הודעה מתאימה כאשר אין טפסים
    cy.get(".no-forms-message")
      .should("be.visible")
      .contains("No forms found for this user");
  });
});
