from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )
'''class IsAdminOrDoctorOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin can update any doctor
        if request.user.is_staff or request.user.role == "admin":
            return True

        
        return (
            request.user.role == "doctor" and
            obj.user == request.user
        )
class IsAdminOrPatientOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin can update any patient
        if request.user.is_staff or request.user.role == "admin":
            return True

        # Patient can update only their own profile
        return (
            request.user.role == "patient"
            and obj.user == request.user
        ) '''

class IsDoctor(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == "doctor"
        )
class IsPatient(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == "patient"
        )