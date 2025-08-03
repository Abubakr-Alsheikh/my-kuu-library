# My KUu Library


**My KUu Library** is a modern, full-featured web application for managing library resources. Built with Django and styled with Tailwind CSS, it provides a seamless experience for both regular users and library administrators. Users can browse, search, and view resources like books and e-journals, while administrators have access to a powerful dashboard to manage all aspects of the library, including users, resources, categories, and notifications.

## ✨ Features

The application is divided into two main parts: the user-facing site and the admin dashboard.

### User Features
- **Authentication:** Secure login system with a "Remember Me" option.
- **Homepage:** A welcoming landing page featuring a prominent search bar, featured resources, and browsable categories.
- **Resource Discovery:**
    - **Search:** A powerful search functionality to find books and e-journals by title or description.
    - **Browse:** Explore all available resources or filter them by category.
- **Resource Details:** View detailed information for each book or e-journal.
- **User Profile:** A personal profile page that displays the user's viewing history.
- **Reporting:** Users can create and view their own reports.
- **Notifications:** View system-wide announcements and notifications from the administration.

### Admin Dashboard Features (`/dashboard`)
- **Dashboard Home:** An overview of the latest activities in the library via an audit log.
- **User Management:** Full CRUD (Create, Read, Update, Delete) functionality for managing users and their roles (staff/regular user).
- **Resource Management:**
    - Add, edit, and delete books and e-journals.
    - Upload cover images for resources.
- **Category Management:** Full CRUD operations for resource categories, including image uploads.
- **Notification Management:** Create, edit, and delete system-wide notifications for all users.
- **Audit Logging:** All significant admin actions (creating/updating/deleting users, resources, etc.) are logged for accountability.

---

## 🛠️ Tech Stack

- **Backend:**
    - [Python](https://www.python.org/)
    - [Django](https://www.djangoproject.com/)
- **Frontend:**
    - [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
    - [Tailwind CSS](https://tailwindcss.com/)
    - [Flowbite](https://flowbite.com/) (UI Component Library)
    - [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- **Database:**
    - [SQLite3](https://www.sqlite.org/index.html) (Default)
- **Deployment & Tooling:**
    - [pip](https://pip.pypa.io/en/stable/)
    - [npm](https://www.npmjs.com/)
    - [django-compressor](https://django-compressor.readthedocs.io/en/latest/)

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- Node.js and npm

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/abubakr-alsheikh-my-kuu-library.git
    cd abubakr-alsheikh-my-kuu-library
    ```

2.  **Set up a Python virtual environment:**
    ```bash
    python -m venv venv
    ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      .\venv\Scripts\activate
      ```

3.  **Install Python dependencies:**
    *(Note: Your `requirements.txt` appears to be a binary file. The command below is standard, but if it fails, you may need to regenerate it. Key dependencies include `django` and `pillow`.)*
    ```bash
    pip install -r requirements.txt
    ```
    If the above fails, install the core packages manually:
    ```bash
    pip install django django-compressor pillow
    ```

4.  **Install frontend dependencies:**
    ```bash
    npm install
    ```

5.  **Build the Tailwind CSS:**
    Run the following command to compile `input.css` into `output.css`. For development, you can add a `--watch` flag to automatically re-compile on changes.
    ```bash
    npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css
    ```
    *Optional: Add a script to your `package.json` for convenience:*
    ```json
    "scripts": {
      "build": "tailwindcss -i ./static/src/input.css -o ./static/src/output.css",
      "watch": "tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch"
    }
    ```

6.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

7.  **Create a superuser to access the admin dashboard:**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create your admin account.

8.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## 📋 Usage

### Accessing the Application

- **User Site:** Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
- **Login Page:** [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/)
- **Admin Dashboard:** Navigate to [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/). You must be logged in as a staff user.

### User Roles

- **Regular User:** Can browse resources, view their profile, and create reports. To create a regular user, use the admin dashboard and ensure the "Is Staff" checkbox is **unchecked**.
- **Admin/Staff User:** Can access the `/dashboard` to manage the library. Log in with the superuser credentials you created or any user with the "Is Staff" flag set to true.

---

## 🏛️ Project Structure

The project follows a standard Django structure with a single `core` app handling most of the logic.

```
abubakr-alsheikh-my-kuu-library/
├── core/                   # Main application
│   ├── models.py           # Database models (Book, EJournal, Category, etc.)
│   ├── views.py            # View logic for user and dashboard pages
│   ├── urls.py             # URL routing for the core app
│   ├── forms.py            # Django forms for user/resource management
│   ├── admin.py            # Django admin site configuration
│   └── decorators.py       # Custom decorators (e.g., @admin_required)
├── my_kuu_library/         # Django project configuration
│   ├── settings.py         # Project settings
│   └── urls.py             # Root URL configuration
├── static/                 # Static files (CSS, JS, images)
│   ├── src/
│   │   ├── input.css       # Tailwind CSS input file
│   │   └── output.css      # Compiled Tailwind CSS
│   └── images/
├── templates/              # HTML templates
│   ├── home/               # Templates for the main user-facing site
│   ├── dashboard/          # Templates for the admin dashboard
│   ├── user/               # Templates for user-specific pages (profile, etc.)
│   ├── registration/       # Login template
│   └── include/            # Reusable template snippets (header, footer)
├── manage.py               # Django's command-line utility
├── requirements.txt        # Python dependencies
├── package.json            # Frontend (npm) dependencies
└── tailwind.config.js      # Tailwind CSS configuration
```
