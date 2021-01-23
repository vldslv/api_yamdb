from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    '''
        All method allowed by admin users or superusers.
    '''

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):

    '''
        Safe method allowed by all users
        Other method allowed by admin users or superusers
    '''

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsOwnerOrAdmgroupOrReadOnly(permissions.BasePermission):

    '''
        Safe method allowed by all users
        Post method allowed by authentication users
        Other method allowed by object owner(author) or
        Administration group(moderator,admin,superuser)
    '''

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.method == 'POST' and request.user.is_authenticated or
                obj.author == request.user or
                request.user.is_moderator or
                request.user.is_admin)
