from django.contrib import admin

from skydata.models import SkynexusData

# Register your models here.
class SkynexusDataAdmin(admin.ModelAdmin):
    """
    Customize the admin form
    By registering the SkynexusData model with 
    admin.site.register(SkynexusData), Django was able 
    to construct a default form representation. But often, 
    you'll want to customize how the admin form looks and works. 
    You can do this by defining a ModelAdmin class and 
    registering it with admin.site.register().
    """
    fieldsets = [
        (None, {'fields': ['city', 'country']}),
        ('Weather information', {'fields': ['temperature', 'feels_like',  'humidity', 'weather_description', 'wind_speed',]}),

    ]

    # By default, Django displays the str() of each object. But 
    # sometimes it’d be more helpful if we could display individual
    #  fields. To do that, use the list_display admin option, which 
    # is a list of field names to display, as columns, on the 
    # change list page for the object:
    list_display = ('city', 'country', 'temperature', 'feels_like', 'humidity', 'weather_description', 'wind_speed', 'created_at')

    # The list_filter option adds a filter sidebar to the change list page:
    list_filter = ['created_at', 'city', 'country']

    # The search_fields option adds a search box at the top of the change list page:
    search_fields = ['city', 'country']

admin.site.register(SkynexusData, SkynexusDataAdmin)