from django.urls import path

from .views import team_no_id_view, team_view
from .views import member_no_id_view, member_view
from .views import team_member_listing_view, team_member_detail_view
from .views import member_manager_get_view, member_manager_common_view

urlpatterns = [
  path(r'team', team_no_id_view),
  path(r'team/<int:pk>', team_view),
  path(r'member', member_no_id_view),
  path(r'member/<int:pk>', member_view),
  path(r'team/<int:team_pk>/member', team_member_listing_view),
  path(r'team/<int:team_pk>/member/<int:member_pk>', team_member_detail_view),
  path(r'member/<int:pk>/manager', member_manager_get_view),
  path(r'member/<int:member_pk>/manager/<int:manager_pk>', member_manager_common_view)
]