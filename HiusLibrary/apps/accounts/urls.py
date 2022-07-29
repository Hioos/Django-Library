from django.urls import path
from . import views

urlpatterns = [
    path('logIn',views.login_user,name="LogInAdmin"),
    path('logOut',views.logout_user,name="LogOutAdmin"),
    path('account/user',views.userIndex,name="userIndex"),
    path('account/user/add',views.add,name="userAdd"),
    path('account/user/adding',views.addUser,name="addUser"),
    path('account/admin/',views.adminIndex,name="adminIndex"),
    path('account/admin/add',views.addAdmin,name="addAdmin"),
    path('account/admin/adding',views.addAdminProccess,name="addAdminProccess"),
    path('profile_update',views.updateProfile,name="updateProfile"),
    path('info/<int:id>',views.info,name="adminInfo"),
    path('extend/',views.extendMembership,name="extendMembership"),
    path('ban',views.banUser,name="banUser"),
    path('loginForUser',views.loginForUser,name="loginForUser")
    ]