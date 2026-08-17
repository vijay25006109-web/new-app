import streamlit as st
import re
import math

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Password Strength Checker",
    page_icon="🔐",
    layout="centered"
)

# -----------------------------
# Password Analysis
# -----------------------------
COMMON_PASSWORDS = {
    "password", "password123", "123456", "12345678", "123456789",
    "qwerty", "qwerty123", "admin", "letmein", "welcome",
    "abc123", "iloveyou", "monkey", "dragon", "login"
}


def analyze_password(password):
    score = 0
    checks = {}

    checks["At least 12 characters"] = len(password) >= 12
    checks["Uppercase letter"] = bool(re.search(r"[A-Z]", password))
    checks["Lowercase letter"] = bool(re.search(r"[a-z]", password))
    checks["Number"] = bool(re.search(r"\d", password))
    checks["Special character"] = bool(re.search(r"[^A-Za-z0-9]", password))

    # Award points for the basic requirements
    score += sum(checks.values())

    # Extra points for longer passwords
    if len(password) >= 16:
        score += 1

    # Penalize common passwords
    if password.lower() in COMMON_PASSWORDS:
        score = max(0, score - 3)
        checks["Not a common password"] = False
    else:
        checks["Not a common password"] = True

    # Penalize obvious repeated characters
    if re.search(r"(.)\1\1", password):
        score = max(0, score - 1)
        checks["No repeated-character pattern"] = False
    else:
        checks["No repeated-character pattern"] = True

    # Penalize simple sequential patterns
    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789",
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm"
    ]

    lower_password = password.lower()
    has_sequence = any(
        sequence[i:i + 4] in lower_password or
        sequence[i:i + 4][::-1] in lower_password
        for sequence in sequences
        for i in range(len(sequence) - 3)
    )

    if has_sequence:
        score = max(0, score - 1)
        checks["No obvious sequence"] = False
    else:
        checks["No obvious sequence"] = True

    score = min(score, 8)

    if score <= 2:
        strength = "WEAK"
        emoji = "🔴"
    elif score <= 4:
        strength = "MODERATE"
        emoji = "🟡"
    elif score <= 6:
        strength = "STRONG"
        emoji = "🟠"
    else:
        strength = "VERY STRONG"
        emoji = "🟢"

    return score, strength, emoji, checks


# -----------------------------
# Header
# -----------------------------
st.title("🔐 Password Strength Checker")
st.write(
    "Enter a password to check its estimated strength. "
    "Your password is analyzed locally and is not stored."
)

st.divider()

# -----------------------------
# Password Input
# -----------------------------
password = st.text_input(
    "Enter your password",
    type="password",
    placeholder="Type your password here..."
)

if password:
    score, strength, emoji, checks = analyze_password(password)

    st.subheader("Password Strength")
    st.progress(score / 8)

    st.markdown(f"## {emoji} {strength}")
    st.write(f"**Score: {score}/8**")

    st.divider()

    # -----------------------------
    # Security Checks
    # -----------------------------
    st.subheader("Security Checks")

    for check, passed in checks.items():
        if passed:
            st.success(f"✓ {check}")
        else:
            st.error(f"✗ {check}")

    # -----------------------------
    # Suggestions
    # -----------------------------
    suggestions = []

    if len(password) < 12:
        suggestions.append("Use at least 12 characters.")
    if not re.search(r"[A-Z]", password):
        suggestions.append("Add at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        suggestions.append("Add at least one lowercase letter.")
    if not re.search(r"\d", password):
        suggestions.append("Add at least one number.")
    if not re.search(r"[^A-Za-z0-9]", password):
        suggestions.append("Add at least one special character.")
    if len(password) < 16:
        suggestions.append("Consider using 16 or more characters.")
    if not checks["Not a common password"]:
        suggestions.append("Avoid common or easily guessed passwords.")
    if not checks["No repeated-character pattern"]:
        suggestions.append("Avoid repeating the same character several times.")
    if not checks["No obvious sequence"]:
        suggestions.append("Avoid obvious sequences such as 1234 or qwerty.")

    st.divider()
    st.subheader("💡 Suggestions")

    if suggestions:
        for suggestion in suggestions:
            st.write(f"• {suggestion}")
    else:
        st.success("Excellent! Your password passes all checks.")

else:
    st.info("Enter a password above to begin the security check.")

st.divider()
st.caption(
    "This tool estimates password strength using local rule-based checks. "
    "It does not guarantee that a password is secure."
)
