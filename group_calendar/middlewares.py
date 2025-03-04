from django.contrib.auth.middleware import AuthenticationMiddleware


class AdminFakeUser:
    id = pk = -1
    is_active = True
    is_staff = True
    is_superuser = True

    ADMIN_PERMISSIONS = [
        "events.add_calendar",
        "events.change_calendar",
        "events.add_event",
        "events.change_event",
        "events.add_member",
        "events.change_member",
    ]

    def get_short_name(self) -> str:
        return "Anonymous"

    def has_module_perms(self, *args, **kwargs):
        return True

    def has_perm(self, permission) -> bool:
        return permission in self.ADMIN_PERMISSIONS


def is_admin_list_view(path: str, app_name: str, model_name: str) -> bool:
    return path == f"/admin/{app_name}/{model_name}/"


def is_admin_change_view(path: str, app_name: str, model_name: str) -> bool:
    return path.startswith(f"/admin/{app_name}/{model_name}") and path.endswith(
        "/change/"
    )


def is_anonymous_allowed(request) -> bool:
    return request.path.startswith("/admin/") and not (
        request.path == "/admin/login/"
        or is_admin_list_view(request.path, "events", "calendar")
        or is_admin_list_view(request.path, "events", "event")
        or is_admin_list_view(request.path, "events", "member")
    )


class AutoAuthMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        if is_anonymous_allowed(request):
            request.user = AdminFakeUser()
        else:
            return super().process_request(request)
