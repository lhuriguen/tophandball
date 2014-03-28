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


class CompetitionSeasonInline(admin.TabularInline):
    model = CompetitionSeason
    extra = 1


class StageInline(admin.TabularInline):
    model = Stage
    extra = 1


class GroupInline(admin.TabularInline):
    model = Group
    extra = 1


class MatchInline(admin.StackedInline):
    model = Match
    extra = 1
    # fieldsets = [
    #     (None,
    #         {'fields': [('home_team', 'away_team'), ('date', 'time'),
    #          'location', ('refereeA', 'refereeB')]}
    #      )
    # ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "home_team" or db_field.name == "away_team":
            if request._obj_ is not None:
                kwargs["queryset"] = Club.objects.filter(
                    group__stage=request._obj_)
            else:
                kwargs["queryset"] = Club.objects.all()
        return super(MatchInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


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
    list_display = ('name', 'country')
    list_filter = ['country']
    search_fields = ['name']


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


class CompetitionAdmin(admin.ModelAdmin):
    inlines = [CompetitionSeasonInline]


class CompetitionSeasonAdmin(admin.ModelAdmin):
    inlines = [StageInline]


class StageAdmin(admin.ModelAdmin):
    inlines = [GroupInline, MatchInline]

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(StageAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Season)
admin.site.register(Club, ClubAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Coach, CoachAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(CompetitionSeason, CompetitionSeasonAdmin)
admin.site.register(Stage, StageAdmin)
