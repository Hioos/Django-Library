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
    path('loginForUser',views.loginForUser,name="loginForUser"),
    path('logoutForUser',views.logoutForUser,name="logoutForUser"),
    path('history',views.historyAdmin,name='historyAdmin'),
    path('books/<int:id>',views.bookUser,name='bookUser'),
    path('profile_update/update',views.profileUpdate,name='AdminprofileUpdate'),
    path('lock/<int:id>',views.lockAdmin,name='lockAdmin'),
    path('promoteAdmin/<int:id>',views.promoteAdmin,name='promoteAdmin'),
    path('manual/extend/<int:id>',views.extendManual,name='extendManual'),
    path('history/log/<int:id>',views.adminLog,name='adminLog'),
    path('log/',views.activities,name='activities'),
    path('changePassword/admin',views.changePasswordAdmin,name='changePasswordAdmin'),
    path('changePasswordProc/admin',views.changePasswordAdminProc,name='changePasswordAdminProc'),
    path('updateUserInfoProc',views.updateUserInfoProc,name='updateUserInfoProc'),
    path('changePassword/user',views.changePasswordUser,name='changePasswordUser'),
    path('changePasswordProc/user',views.changePasswordUserProc,name='changePasswordUserProc')
    ]