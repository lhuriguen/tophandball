from django.contrib import admin
from data.models import *


class ClubNamesInline(admin.TabularInline):
    model = ClubName
    extra = 1


class PlayerNamesInline(admin.TabularInline):
    model = PlayerName
    extra = 1


class PlayerContractInline(admin.TabularInline):
    model = PlayerContract
    extra = 1


class CoachContractInline(admin.TabularInline):
    model = CoachContract
    extra = 1


class ClubAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
            {'fields': ['name', 'short_name', 'country', 'ehf_id', 'address']}
         ),
        ('Links',
            {'fields': ['website', 'twitter', 'facebook'],
             'classes': ['collapse']}
         )
    ]
    inlines = [ClubNamesInline, PlayerContractInline, CoachContractInline]


class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['ehf_id', 'gender']}),
        ('Personal information',
            {'fields': [('first_name', 'last_name'),
                        ('birth_date', 'birth_place'),
                        'country', 'height']}
         ),
        ('Playing information',
            {'fields': ['position', 'main_hand', 'retired']})
    ]
    inlines = [PlayerNamesInline, PlayerContractInline]
    list_display = ('full_name', 'country', 'birth_date')
    list_filter = ['country']
    search_fields = ['first_name', 'last_name']


class CoachAdmin(admin.ModelAdmin):
    inlines = [CoachContractInline]


admin.site.register(Season)
admin.site.register(Club, ClubAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Coach, CoachAdmin)
