from django.urls import path, re_path


def add_module_prefix_to_url_path(module_name, patterns):
    prefixed_patterns = []
    for pattern in patterns:
        if hasattr(pattern, "pattern"):
            new_pattern = path(f"{module_name}/{pattern.pattern}", pattern.callback)
        else:
            new_pattern = re_path(f"{module_name}/{pattern.regex.pattern}", pattern.callback)
        prefixed_patterns.append(new_pattern)
    return prefixed_patterns
