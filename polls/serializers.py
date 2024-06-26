from rest_framework import serializers

from .models import Team, Member, TeamMember, MemberHierarchyTree

class MemberSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), required=False)

    class Meta:
        model  = Member
        fields = ('id', 'first_name', 'last_name', 'email')

class TeamMemberSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)

    class Meta:
        model  = TeamMember
        fields = ('member', 'role')

class TeamSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), required=False)
    members = serializers.SerializerMethodField()

    def get_members(self, obj):
        def prepare_member(team_member):
            return TeamMemberSerializer(team_member).data

        return tuple(map(prepare_member, TeamMember.objects.filter(team__pk=obj.id).all()))

    class Meta:
        model  = Team
        fields = ('id', 'name', 'members')

class MemberHierarchyTreeSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)
    manager = MemberSerializer(read_only=True)

    class Meta:
        model  = MemberHierarchyTree
        fields = ('member', 'manager')
