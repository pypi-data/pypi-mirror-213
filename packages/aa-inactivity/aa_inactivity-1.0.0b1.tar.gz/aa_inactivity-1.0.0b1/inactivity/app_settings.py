from app_utils.django import clean_setting

# Default priority for all tasks
INACTIVITY_TASKS_DEFAULT_PRIORITY = clean_setting(
    "INACTIVITY_TASKS_DEFAULT_PRIORITY", 6
)
