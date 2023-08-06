def mark_as_handleveled(modeladmin, request, queryset):
    queryset.update(is_handleveled=True)


def clear_handleveled(modeladmin, request, queryset):
    queryset.update(is_handleveled=False)
