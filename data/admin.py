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


class GroupTableInline(admin.TabularInline):
    model = GroupTable
    extra = 1


class MatchInline(admin.StackedInline):
    model = Match
    extra = 1
    fieldsets = [
        (None,
            {'fields': ['stage', ('home_team', 'away_team'),
                        ('match_datetime'),
                        ('score_home', 'score_away'),
                        'report_url']}
         ),
        ('Playing Location',
            {'fields': [('arena', 'location', 'spectators')]}
         ),
        ('Officials',
            {'fields': [('referees', 'delegates')]}
         )
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "home_team" or db_field.name == "away_team":
            if request._obj_ is not None:
                kwargs["queryset"] = Club.objects.filter(
                    group__stage=request._obj_)
            else:
                kwargs["queryset"] = Club.objects.all()
        return super(MatchInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


class MatchTeamStatsInline(admin.TabularInline):
    model = MatchTeamStats
    extra = 1
    max_num = 2


class MatchPlayerStatsInline(admin.TabularInline):
    model = MatchPlayerStats


class ClubAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
            {'fields': [('name', 'short_name', 'initials'),
                        ('country', 'address'), 'ehf_id',
                        'logo', 'admin_thumbnail']}
         ),
        ('Links',
            {'fields': ['website', 'twitter', 'facebook'],
             'classes': ['collapse']}
         )
    ]
    inlines = [ClubNamesInline, PlayerContractInline, CoachContractInline]
    list_display = ('name', 'country', 'has_logo')
    list_filter = ['country']
    search_fields = ['name']
    readonly_fields = ('admin_thumbnail',)


class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal information',
            {'fields': [('first_name', 'last_name'),
                        ('birth_date', 'birth_place', 'country'),
                        ('height', 'gender'), 'photo', 'admin_thumbnail']}
         ),
        ('Playing information',
            {'fields': [('position', 'main_hand'),
                        ('retired', 'retirement_date'), 'ehf_id']})
    ]
    inlines = [PlayerNamesInline, PlayerContractInline]
    list_display = ('full_name', 'country', 'birth_date', 'has_photo')
    list_filter = ['country']
    search_fields = ['first_name', 'last_name']
    readonly_fields = ('admin_thumbnail',)


class CoachAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal information',
            {'fields': [('first_name', 'last_name'),
                        ('birth_date', 'birth_place', 'country'),
                        'player', 'photo', 'admin_thumbnail']}
         )
    ]
    readonly_fields = ('admin_thumbnail',)
    list_display = ('full_name', 'country', 'birth_date', 'has_photo')
    search_fields = ['first_name', 'last_name']
    inlines = [CoachContractInline]


class CompetitionAdmin(admin.ModelAdmin):
    inlines = [CompetitionSeasonInline]


class CompetitionSeasonAdmin(admin.ModelAdmin):
    inlines = [StageInline]


class StageAdmin(admin.ModelAdmin):
    inlines = [GroupInline, MatchInline]
    list_display = ('comp_season', 'name', 'order')
    list_filter = ['comp_season__competition__name', 'comp_season__season']
    search_fields = ['comp_season__competition__name', 'name']

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(StageAdmin, self).get_form(request, obj, **kwargs)


class MatchAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
            {'fields': ['stage', ('home_team', 'away_team'),
                        ('match_datetime'),
                        ('score_home', 'score_away'),
                        'report_url']}
         ),
        ('Playing Location',
            {'fields': [('arena', 'location', 'spectators')]}
         ),
        ('Officials',
            {'fields': [('referees', 'delegates')]}
         )
    ]
    inlines = [MatchTeamStatsInline]
    list_filter = ['match_datetime', 'stage']
    list_display = ('home_team', 'away_team', 'match_datetime', 'location')
    search_fields = ['home_team__name', 'away_team__name']


class GroupAdmin(admin.ModelAdmin):
    inlines = [GroupTableInline]


admin.site.register(Season)
admin.site.register(Club, ClubAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Coach, CoachAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(CompetitionSeason, CompetitionSeasonAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Match, MatchAdmin)
