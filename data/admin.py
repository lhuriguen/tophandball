from django.contrib import admin

import reversion

from .models import *


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
            {'fields': ['group', ('home_team', 'away_team'),
                        ('match_datetime', 'week'),
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
                    group=request._obj_)
            else:
                kwargs["queryset"] = Club.objects.all()
        return super(MatchInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


class MatchTeamStatsInline(admin.TabularInline):
    model = MatchTeamStats
    extra = 1
    max_num = 2
    raw_id_fields = ('club', )


class MatchPlayerStatsInline(admin.TabularInline):
    model = MatchPlayerStats
    raw_id_fields = ('club', 'player')


class ClubAdmin(reversion.VersionAdmin):
    fieldsets = [
        (None,
            {'fields': [('name', 'short_name', 'initials'),
                        ('country', 'address', 'latitude', 'longitude'),
                        'ehf_id', 'logo', 'admin_thumbnail']}
         ),
        ('Links',
            {'fields': ['website', 'twitter', 'facebook'],
             'classes': ['collapse']}
         )
    ]
    inlines = [ClubNamesInline, CoachContractInline]
    list_display = ('name', 'country', 'has_logo')
    list_filter = ['country']
    search_fields = ['name']
    readonly_fields = ('admin_thumbnail',)


class PlayerAdmin(reversion.VersionAdmin):
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


class CoachAdmin(reversion.VersionAdmin):
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
    list_display = (
        'name', 'short_name', 'country',
        'is_international', 'level')
    search_fields = ('name',)
    readonly_fields = ('admin_thumbnail',)


class CompetitionSeasonAdmin(admin.ModelAdmin):
    inlines = [StageInline]
    list_filter = ['competition', 'season']


class StageAdmin(admin.ModelAdmin):
    inlines = [GroupInline]
    list_display = ('comp_season', 'name', 'order')
    list_filter = ['comp_season__competition__name', 'comp_season__season']
    search_fields = ['comp_season__competition__name', 'name']


class MatchAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
            {'fields': ['group', ('home_team', 'away_team'),
                        ('match_datetime', 'week'),
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
    inlines = [MatchTeamStatsInline, MatchPlayerStatsInline]
    list_filter = ['match_datetime', 'group__stage__comp_season']
    list_display = ('home_team', 'away_team', 'match_datetime', 'location')
    search_fields = ['home_team__name', 'away_team__name']
    # raw_id_fields = ('referees', 'delegates')
    filter_horizontal = ('referees', 'delegates')


class GroupAdmin(admin.ModelAdmin):
    inlines = [GroupTableInline, MatchInline]
    list_display = ['stage', 'order', 'name']
    list_filter = ['stage__comp_season__competition',
                   'stage__comp_season__season']
    search_fields = ['stage__name']

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(GroupAdmin, self).get_form(request, obj, **kwargs)


class MatchTeamStatsAdmin(admin.ModelAdmin):
    list_display = ['club', 'match', 'halftime_score', 'finaltime_score']
    list_filter = ['match__match_datetime', 'match__group__stage__comp_season']
    search_fields = ['club__name']


class RefereeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'country']


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    filter_horizontal = ('competitions',)

admin.site.register(Season)
admin.site.register(Club, ClubAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Coach, CoachAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(CompetitionSeason, CompetitionSeasonAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Referee, RefereeAdmin)
admin.site.register(Delegate)
admin.site.register(MatchTeamStats, MatchTeamStatsAdmin)
admin.site.register(Category, CategoryAdmin)
