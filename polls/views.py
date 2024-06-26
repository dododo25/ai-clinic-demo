from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Team, Member, TeamMember, MemberHierarchyTree
from .serializers import TeamSerializer, MemberSerializer, TeamMemberSerializer, MemberHierarchyTreeSerializer

@api_view(['GET', 'POST'])
def team_no_id_view(request):
    if request.method == 'GET':
        return Response(TeamSerializer(Team.objects.all(), many=True).data)

    if request.method == 'POST':
        serialized = TeamSerializer(data=request.data)

        if not serialized.is_valid():
            first_error = list(serialized.errors.items())[0]

            return Response(
                data   = {'message': str(first_error[0]) + ' - ' + first_error[1][0]},
                status = status.HTTP_400_BAD_REQUEST
            )

        serialized.save()

        return Response(
            data   = serialized.data,
            status = status.HTTP_201_CREATED
        )

@api_view(['GET', 'DELETE'])
def team_view(request, pk):
    if request.method == 'GET':
        try:
            return Response(TeamSerializer(Team.objects.get(pk=pk)).data)
        except ObjectDoesNotExist as e:
            return Response (
                data    = {'message': str(e)},
                status  = status.HTTP_400_BAD_REQUEST
            )

    if request.method == 'DELETE':
        filtered = Team.objects.filter(pk=pk)

        if filtered.exists():
            filtered[0].delete()

        return Response(status = status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def member_no_id_view(request):
    if request.method == 'GET':
        return Response(MemberSerializer(Member.objects.all(), many=True).data)

    if request.method == 'POST':
        serialized = MemberSerializer(data=request.data)

        if not serialized.is_valid():
            first_error = list(serialized.errors.items())[0]

            return Response(
                data   = {'message': str(first_error[0]) + ' - ' + first_error[1][0]},
                status = status.HTTP_400_BAD_REQUEST
            )

        serialized.save()

        return Response(
            data   = serialized.data,
            status = status.HTTP_201_CREATED
        )

@api_view(['GET', 'DELETE'])
def member_view(request, pk):
    if request.method == 'GET':
        try:
            return Response(MemberSerializer(Member.objects.get(pk=pk)).data)
        except ObjectDoesNotExist as e:
            return Response (
                data    = {'message': str(e)},
                status  = status.HTTP_400_BAD_REQUEST
            )

    if request.method == 'DELETE':
        filtered = Member.objects.filter(pk=pk)

        if filtered.exists():
            filtered[0].delete()

        return Response(status = status.HTTP_200_OK)

@api_view(['GET'])
def team_member_listing_view(request, team_pk):
    if request.method == 'GET':
        if not Team.objects.filter(pk=team_pk).exists():
            return Response (
                data = {'message': 'Team matching query does not exist.'},
                status  = status.HTTP_400_BAD_REQUEST
            )

        selected   = TeamMember.objects.filter(team__pk=team_pk)
        serialized = TeamMemberSerializer(selected, many=True)

        return Response(serialized.data)

@api_view(['POST', 'DELETE'])
def team_member_detail_view(request, team_pk, member_pk):
    filtered_teams   = Team.objects.filter(pk=team_pk)
    filtered_members = Member.objects.filter(pk=member_pk)

    if not filtered_teams.exists():
        return Response (
            data    = {'message': 'Team matching query does not exist.'},
            status  = status.HTTP_400_BAD_REQUEST
        )

    if not filtered_members.exists():
        return Response (
            data    = {'message': 'Member matching query does not exist.'},
            status  = status.HTTP_400_BAD_REQUEST
        )

    team   = filtered_teams[0]
    member = filtered_members[0]

    if request.method == 'POST':
        team_member = TeamMember(team=team, member=member, role=request.data['role'])

        if TeamMember.objects.filter(team=team, member=member).exists():
            return Response (
                data    = {'message': 'This member already in this team.'},
                status  = status.HTTP_400_BAD_REQUEST
            )

        team_member.save()

        return Response(
            data    = TeamSerializer(team).data,
            status  = status.HTTP_201_CREATED
        )

    if request.method == 'DELETE':
        TeamMember.objects.filter(team=team, member=member).delete()
        return Response()

@api_view(['GET'])
def member_manager_get_view(request, pk):
    member = Member.objects.filter(pk=pk)

    if not member.exists():
        return Response (
            data    = {'message': 'Member matching query does not exist.'},
            status  = status.HTTP_400_BAD_REQUEST
        )

    hierarchy = MemberHierarchyTree.objects.filter(member=member[0])

    if not hierarchy.exists():
        return Response(data=None)

    return Response(MemberHierarchyTreeSerializer(hierarchy[0]).data)

@api_view(['POST', 'DELETE'])
def member_manager_common_view(request, member_pk, manager_pk):
    def contains_loop(member, manager):
        current = manager

        while True:
            if current == member:
                return True

            current = MemberHierarchyTree.objects.filter(member=current)

            if not current.exists():
                break

            current = current[0].manager

        return False

    filtered_members  = Member.objects.filter(pk=member_pk)
    filtered_managers = Member.objects.filter(pk=manager_pk)

    if not filtered_members.exists():
        return Response (
            data    = {'message': 'Member matching query does not exist.'},
            status  = status.HTTP_400_BAD_REQUEST
        )

    if not filtered_managers.exists():
        return Response (
            data    = {'message': 'manager member matching query does not exist.'},
            status  = status.HTTP_400_BAD_REQUEST
        )

    member  = filtered_members[0]
    manager = filtered_managers[0]

    if contains_loop(member, manager):
        return Response (
            data    = {'message': 'Loop detected!'},
            status  = status.HTTP_400_BAD_REQUEST
        )

    if request.method == 'POST':
        if MemberHierarchyTree.objects.filter(member=member).exists():
            return Response (
                data    = {'message': 'Manager is already defined for this member.'},
                status  = status.HTTP_400_BAD_REQUEST
            )

        MemberHierarchyTree(member=member, manager=manager).save()

        return Response(
            data    = MemberSerializer(member).data,
            status  = status.HTTP_201_CREATED
        )

    if request.method == 'DELETE':
        MemberHierarchyTree.objects.filter(member=member, manager=manager).delete()
        return Response()