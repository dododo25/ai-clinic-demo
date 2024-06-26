from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=256, null=False, unique=True)

    def __str__(self):
        return self.name

class Member(models.Model):
    first_name  = models.CharField(max_length=256, null=False)
    last_name   = models.CharField(max_length=256, null=False)
    email       = models.EmailField(null=False, unique=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class TeamMember(models.Model):
    team   = models.ForeignKey(Team, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    role   = models.CharField(max_length=256, null=False)

    def __str__(self):
        return str(self.team) + ' - ' + str(self.member) + ' - ' + self.role

class MemberHierarchyTree(models.Model):
    member  = models.ForeignKey(Member, related_name='%(class)s_member', on_delete=models.CASCADE, unique=True)
    manager = models.ForeignKey(Member, related_name='%(class)s_manager', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.manager) + ' -> ' + str(self.member)