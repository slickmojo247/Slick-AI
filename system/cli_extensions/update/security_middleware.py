def validate_edit_permissions(file_path, user):
    RESTRICTED_PATHS = ['core/ai_models/', 'config/']
    if any(file_path.startswith(p) for p in RESTRICTED_PATHS):
        return user.role == 'admin'
    return True