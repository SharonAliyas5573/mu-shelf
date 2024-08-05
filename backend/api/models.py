from django.db import models
import uuid
from .managers import user_manager
from django.conf import settings

# Copied from mulearnbackend
class User(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    discord_id = models.CharField(unique=True, max_length=36, blank=True, null=True)
    muid = models.CharField(unique=True, max_length=100)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, max_length=200)
    mobile = models.CharField(unique=True, max_length=15, blank=True, null=True)
    exist_in_guild = models.BooleanField(default=False)
    suspended_at = models.DateTimeField(blank=True, null=True)
    suspended_by = models.ForeignKey("self", on_delete=models.SET(settings.SYSTEM_ADMIN_ID), blank=True, null=True,
                                     related_name="user_suspended_by_user", db_column="suspended_by", default=None)
    objects = user_manager.ActiveUserManager()
    every = models.Manager()

    class Meta:
        managed = False
        db_table = 'user'

class ProblemStatement(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField()
    reward = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="problem_statements_created", on_delete=models.CASCADE, db_column="created_by")
    approved_by = models.ForeignKey(User, related_name="approved_problem_statements", on_delete=models.SET_NULL, null=True)
    end = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'mushelf_problem_statements'

class Solution(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_winner = models.BooleanField(default=False)
    problem_statement = models.ForeignKey(ProblemStatement, related_name="solutions", on_delete=models.CASCADE, db_column="problem_statement")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="solutions_submitted", on_delete=models.CASCADE, db_column="created_by")

    class Meta:
        managed = False
        db_table = 'mushelf_solutions'



class Contributor(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    muid = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=200)
    solution = models.ForeignKey(Solution, related_name="contributors", on_delete=models.CASCADE, db_column="solution")

    class Meta:
        managed = False
        db_table = 'mushelf_contributors'


# Copied from mulearnbackend
class Organization(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4())
    title = models.CharField(max_length=100)
    code = models.CharField(unique=True, max_length=12)
    org_type = models.CharField(max_length=25)
    updated_by = models.ForeignKey(User, on_delete=models.SET(settings.SYSTEM_ADMIN_ID), db_column='updated_by',
                                   related_name='organization_updated_by')
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET(settings.SYSTEM_ADMIN_ID), db_column='created_by',
                                   related_name='organization_created_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'organization'


class CompanyProfile(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    organization = models.CharField(max_length=36) # Relation to organization table
    email = models.EmailField(unique=True, max_length=200)
    mobile = models.CharField(unique=True, max_length=15, blank=True, null=True)
    website = models.URLField(null=True)
    size = models.IntegerField()
    bio = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="company_created", on_delete=models.CASCADE, db_column="created_by")


# Copied from mulearnbackend
class UserOrganizationLink(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_organization_link_user')
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='user_organization_link_org')
    verified = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete=models.SET(settings.SYSTEM_ADMIN_ID), db_column='created_by',
                                   related_name='user_organization_link_created_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'user_organization_link'