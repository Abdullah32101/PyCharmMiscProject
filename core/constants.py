# constants.py

# ---------- URLs ----------
# Direct book purchase URL for testing
BOOK_URL = "https://staging.solutioninn.com/textbooks/accounting-information-systems-9th-edition-9781305465114"

# Membership question page URLs (different from book purchase)
PRIMARY_URL = "https://staging.solutioninn.com/15"
SECONDARY_URL = "https://staging.solutioninn.com/study-help/the-macro-economy/using-data-from-the-endpapers-of-this-book-graph-real"

# ---------- User Info ----------
DEFAULT_PASSWORD = "Zeeshan@9671"
DEFAULT_UNIVERSITY = "Punjab University Lahore"
DEFAULT_FIRST_NAME = "Zeeshan"
DEFAULT_LAST_NAME = "Ali"
EMAIL_DOMAIN = "example.com"

# ---------- Contact ----------
COUNTRY = "Pakistan"
STATE = "Punjab"
CITY = "Lahore"
POSTAL_CODE = "54000"
ADDRESS = "House No 11, sector A2, Gulberg"
PHONE_NUMBER = "032064970863333"

# ---------- Payment ----------
CARD_NUMBER = "4242424242424242"
CARD_HOLDER_NAME = "Zeeshan Ali"
CVC = "123"
EXPIRY_MONTH = "03"
EXPIRY_YEAR = "2032"
EXPIRY_MONTH_LABEL = "March (03)"
EXPIRY_YEAR_LABEL = "2032"

# ---------- Selectors ----------

# ---------- View Solution Button Selectors ----------
VIEW_SOLUTION_BTN_CSS = ".view_solution_btn.step1PopupButton"

# ---------- Plan Button Selectors ----------
POPULAR_PLAN_BUTTON_XPATH = "//button[contains(@class,'new-btn-blue-area activate_button')]"
MONTHLY_PLAN_BUTTON_XPATH = "//div[@class='new-month-day-trail-1 plans-card-header']//button[@type='button'][normalize-space()='View Solution']"
SIX_MONTH_PLAN_BUTTON_XPATH = "//div[@class='new-month-day-trail-6 plans-card-header']//button[@type='button'][normalize-space()='View Solution']"
ONE_TIME_PLAN_BUTTON_XPATH = "//button[normalize-space()='Buy solution']"

# ---------- Payment Toggle Selectors ----------
PAYMENT_TOGGLE_SELECTORS = [
    "//input[@id='radio7']",
    "//label[@for='radio7']",
    "//input[@name='payment_method' and @value='card']",
    "//input[@type='radio' and contains(@class, 'payment')]",
    "//input[@type='radio' and contains(@class, 'card')]",
]

# ---------- Join Now Button Selectors ----------
JOIN_NOW_BUTTON_SELECTORS = [
    "//button[contains(text(), 'Join Now')]",
    "//button[contains(text(), 'join now')]",
    "//input[@value='Join Now']",
]

# ---------- Form Field IDs ----------
EMAIL_FIELD_ID = "emailR"
PASSWORD_FIELD_ID = "passwordR"
UNIVERSITY_FIELD_ID = "uni"
SIGNUP_BUTTON_ID = "signup-button"
CARD_NUMBER_FIELD_ID = "cc_num"
CARD_HOLDER_FIELD_ID = "cc_card_holder"
CVC_FIELD_ID = "cc-cvc"
POSTAL_CODE_FIELD_ID = "zipcode"
SUBMIT_BUTTON_ID = "submit_btn_checkout"

# ---------- Expiry Dropdown IDs ----------
EXPIRY_MONTH_IDS = ["cc_expiry_month", "cc-exp-month", "cc_exp_month"]
EXPIRY_YEAR_IDS = ["cc_expiry_year", "cc-exp-year", "cc_exp_year"]

# ---------- One Time Plan Fallback Selectors ----------
ONE_TIME_PLAN_FALLBACK_SELECTORS = [
    "//button[contains(@class,'new-btn-blue-area activate_button')]",
    "//button[contains(text(), 'One Time')]",
    "//button[contains(text(), 'one time')]",
    "//button[contains(text(), 'One-Time')]",
    "//button[contains(text(), 'one-time')]",
    "//a[contains(text(), 'One Time')]",
    "//a[contains(text(), 'one time')]",
    "//a[contains(text(), 'One-Time')]",
    "//a[contains(text(), 'one-time')]",
]

# ---------- Popular Plan Fallback Selectors ----------
POPULAR_PLAN_FALLBACK_SELECTORS = [
    "//button[contains(@class,'new-btn-blue-area activate_button')]",
    "//button[contains(text(), 'Popular')]",
    "//button[contains(text(), 'popular')]",
    "//button[contains(@class, 'popular')]",
    "//a[contains(text(), 'Popular')]",
    "//a[contains(@class, 'popular')]",
]

# ---------- Payment Toggle Fallback Selectors ----------
PAYMENT_TOGGLE_FALLBACK_SELECTORS = [
    "//label[@for='radio7']",
    "//input[@id='radio7']",
    "//label[contains(text(), 'Credit Card')]",
    "//label[contains(text(), 'Card')]",
    "//input[@type='radio'][@name='payment_method']",
    "//input[@type='radio']",
    "//label[contains(@class, 'payment')]",
    "//div[contains(@class, 'payment')]//input[@type='radio']",
]
