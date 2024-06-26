from django.contrib import admin

from .models import Team, Member, TeamMember, MemberHierarchyTree

admin.site.register(Team)
admin.site.register(Member)
admin.site.register(TeamMember)
admin.site.register(MemberHierarchyTree)
