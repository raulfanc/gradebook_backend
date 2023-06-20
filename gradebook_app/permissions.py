from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Administrator").exists()


class IsLecturer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="lecturer").exists()

    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH':
            # Validate that only 'grade' field is being updated
            if set(request.data.keys()) <= {'grade'}:
                return True
        return False


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="student").exists()

    def has_object_permission(self, request, view, obj):
        # Students can only view their own grades
        if request.method == 'GET':
            return obj.enrolled_student.user == request.user

        return False