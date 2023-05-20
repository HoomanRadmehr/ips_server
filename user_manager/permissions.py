from rest_framework.permissions import BasePermission,SAFE_METHODS


class IsCustomerOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_customer and request.user.is_verified and not request.user.is_deleted:
            return True
        return False

class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser and request.user.is_verified and not request.user.is_deleted:
            return True
        return False
    
class IsSupporterOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_supporter and request.user.is_verified and not request.user.is_deleted:
            return True
        return False
    
class IsDeveloperOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_developer and request.user.is_verified and not request.user.is_deleted:
            return True
        return False


class IsInstallerOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_installer and request.user.is_verified and not request.user.is_deleted:
            return True
        return False

    
class IsSellerOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_seller and request.user.is_verified and not request.user.is_deleted:
            return True
        return False
    
    
class IsOwnerOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.id == obj.id
    
    
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or (request.user.is_authenticated and request.user.is_superuser):
            return True
        else:
            return False
        