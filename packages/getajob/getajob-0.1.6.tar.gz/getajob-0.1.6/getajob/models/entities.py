from enum import Enum


class Entity(str, Enum):
    USERS = "users"
    ADMIN_USERS = "admin_users"
    RECRUITERS = "recruiters"
    SKILLS = "skills"
    COVER_LETTERS = "cover_letters"
    RESUMES = "resumes"
    USER_DETAILS = "user_details"
    COMPANIES = "companies"
    JOBS = "jobs"
    APPLICATIONS = "applications"
    USER_NOTIFICATIONS = "user_notifications"
