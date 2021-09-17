from django.contrib import admin

# Register your models here.
from policy.models import Policy


class PolicyAdmin(admin.ModelAdmin):
    model = Policy


admin.site.register(Policy, PolicyAdmin)
