# Report

- Full Name:
- Student Number:
- Full Name of person you made your full stack project with:
- Student Number of person you made your full stack project with:
- Brief description of your project and the technologies used for front- and back-end:

# Cryptography

## Before

By default, Django uses secure password hashing (PBKDF2 with SHA256) and built-in authentication via sessions and cookies. This was unchanged to keep the security measures unchanged.

## After

Nothing here was changed. I did not see any reason to change the already secure built-in user management tools.

## Code Examples

-

# Injections

Since the framework used was Django, and there was only one input window that already processes the text specifically for tokenization, it was quite difficult to figure out how to actually manage an injection.

## Before

Describe in a few sentences what the actual status is (before changing).

## After

Continued using Django’s ORM for all database operations, which automatically escapes query parameters and protects against SQL injection.

Ensured that data sent to NLP model is treated as plain text, without executing or rendering it in unsafe ways. For example: 
```
const userMessage = messageInput.value.replace(/<[^>]*>?/gm, "").trim();
```
The code above removes things like HTML tags, helping prevent XSS.

## Code Examples
-

# Class 04 Vulnerable & Outdated components

## SBOM & Dependency Check



## Vulnerabilities

Even though the sql injection risk was supposedly very low, the risk of it was found severe here.
![alt text](image-2.png)
To fix this issue, I only needed to update django to a newer version.
It found 3 other vulnerabilities.
![alt text](image-1.png)

## Vulnerabilities - Updated

The main issue only needed a dependency update (django). The other issues were solved by changing the code slightly, for example, changing InnerHTML to textContent in the javascript file to prevent exploits.

# Class 05/06/07 - Authentication, Session Management & Authorization

(guideline: max 2 A4 pages, images/code snippets not counted)
Describe each of the following functionalities in your application AS IS:

- User registration was implemented using the simple template provided by django. Users can register via a /register/ endpoint that creates a new user using Django’s built-in User model. Passwords are hashed using Django’s secure PBKDF2 mechanism.
- Login is done via Django’s LoginView that verifies the username and password using authenticate() and logs in users with login(request, user), creating a secure session cookie.
- This feature was not implemented.
- In theory, accessible only to authenticated users. After successful password change, the user is logged out to avoid session fixation. However, the built-in functionality was not used in the project.
- Session is stateful (Django default)
    - Stored: On server (default: DB-backed sessions).
    - Transferred: A session cookie named sessionid is sent to the browser.
    - Accessed: Anywhere via request.session.
    - Verified: Django middleware automatically validates the session cookie on each request.
    - Terminated: Via logout(request) which deletes the session.
- Access control is managed through the Admin page, which is also a django default. Mostly, the only differece between a user and an admin/manager is that the higher autorization level grants access to recipe additions, changes and deletions.

The missing functionalities, like resetting the password would most likely require for the reset to be sent through email or phone, which can get complex. That is not something that I know how to implement securely, so I left it out.

As for account deletion, it is accessible for admins, which should be enough for a small application like this.

- Verified CSRF token presence in HTML forms and AJAX headers.

- Checked that no sensitive data is exposed in cookies (cookies are HttpOnly, not accessible via JS).

- No session fixation after password change (confirmed logout happens).

- Not vulnerable to stored XSS anymore (escaped all output using .textContent).

- No direct object reference or IDOR – URLs are permission-guarded.

- CORS not enabled publicly – only this frontend allowed.

- Manual cookie editing or replay did not work when logged out.

# Class 08 - Secure CI/CD & Supply Chain

## Project for this course

Currently in the development and manual deployment/testing phase.

- No automated CI/CD pipeline is deployed (e.g., no GitHub Actions, GitLab CI, or Docker push/pull yet).

- A local build may include unverified dependencies, or someone could tamper with scripts or install packages that weren't reviewed.

- No attestation that the code was built from the right source or environment.

- Builds may vary across environments, especially with Python dependencies if not pinned.

## Project for the SE course

I do not take the SE course.

# Class 09 SSRF

Currently, the application does not directly process user-controlled URLs (e.g., image fetchers, link previews, or remote requests from user input). Therefore, an SSRF attack is not currently possible.

However, if such a feature is introduced (e.g., validating user-provided links or loading images from URLs), I would mitigate SSRF by:

    - Allowlisting safe domains/IPs,

    - Blocking internal IP ranges (e.g., 127.0.0.1, 169.254.x.x),

    - Using a sandboxed proxy to fetch external content safely.

# Class 09 Logging & Monitoring

Logs must have a timestamp – Enabled via Django's default log format.

Logs must include severity level – All logs are categorized (INFO, WARNING, ERROR).

Logs must not contain sensitive data – User passwords and tokens are not logged.

Logs must be readable – Logs are in a structured and readable format via Python's logging module.

Logs must provide context – Logs include the view name and user ID if authenticated.

Logs must be written to a centralized location – Currently, logs are written to a local logfile.log file (for development).

Logs must be monitored – Manual inspection is used; integration with a real-time monitor (e.g., Sentry) is a planned improvement.

P.S. I'm unable to install the spacy extension for whatever reason, and since I'm doing this part sort of last-minute, I can't provide a log screenshot, I am sorry about that.

# Class 09 SAST

I installed Bandit for Python in my IDE (VS Code).

```
[bandit] B105: Use of hard-coded password
[bandit] B303: Use of insecure MD5 hash function
[bandit] B601: Potentially vulnerable function - os.system
```


Hard-coded password (B105): Removed the test user with password='admin123' and used Django’s built-in user creation tools with hashed passwords.

# Class 09 DAST

-

# Class 10 topic

-

# Conclusion

Throughout this project, the most important change I implemented was improving the security of both client- and server-side code by addressing critical issues like XSS vulnerabilities, missing CSRF protection, and weak session handling. I also learned how important it is to follow secure coding practices from the beginning—especially in user input handling and dependency management.

Below are examples of how I applied each of the key security principles in this project:

1. Least Privilege
Example: User roles were implemented with limited access—only admins can remove projects or users, while regular users can only view or join projects.

2. Defense in Depth
Example: I used CSRF tokens on all POST requests, input validation on both frontend and backend, and security headers (Content-Security-Policy, X-Frame-Options, etc.) for layered protection.

3. Fail Securely
Example: If the server encounters an error, it returns a generic error message to the user while logging the full exception securely, avoiding information leakage.

4. Secure by Default
Example: Django’s secure settings (e.g., SESSION_COOKIE_SECURE, CSRF_COOKIE_HTTPONLY) were enabled to prevent insecure defaults during deployment.

5. Keep It Simple
Example: Authentication was handled using Django’s built-in auth system, avoiding custom and error-prone login logic.

6. Separation of Duties
Example: Different components handle different responsibilities: authentication is managed by Django, input processing is handled by NLP services, and frontend rendering is kept separate.

7. Don’t Trust User Input
Example: All user input is sanitized and validated—JavaScript no longer uses innerHTML directly, and server-side input is parsed and cleaned before processing.

# Appendix

## Tools used

Below is the list of tools, libraries, and settings I used to improve the security of my application:

    - OWASP ZAP – for automated DAST scans (pre- and post-authenticated)

    - Bandit – Python SAST tool used to detect security issues in code

    - Django Security Middleware – enforced settings such as X-Content-Type-Options, X-Frame-Options, and CSRF protection

    - Django's built-in auth system – for secure user authentication and session handling

    - Subprocess module – replaced os.system() calls to prevent command injection risks

    - hashlib.sha256 – replaced insecure MD5 usage

    - CSRF tokens – included in every sensitive request to protect against CSRF attacks

    - Cookie flags – set HttpOnly, Secure, and SameSite on session cookies

    - Browser developer tools – for validating cookie/session flags and HTTP headers
### ZAP Test (non authenticated)
### ZAP Test (authenticated)

## Vulnerabilities discovered

Put here the full list of CVE's you found that were applicable to your code (or the libraries you used)

### SBOM

[text](../Documents/GitHub/architektura/sbom.json)

## Most interesting conversation with a GenAI tool

Here, I expect you to copy paste a full transcript of the most interesting conversation you had with a genAI tool (also mention which one and what version).
