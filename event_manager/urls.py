from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'event_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # user interface views
    url(r'^$', 'subscribe.views.index', name='index'),
    url(r'^login-gestione-eventi/', 'subscribe.views.subscribe', name='subscribe'),
    url(r'^gestione-eventi/', 'subscribe.views.gestioneEventi', name='gestioneEventi'),
    url(r'^gestione-ragazzi/', 'subscribe.views.gestioneRagazzi', name='gestioneEventi'),
    url(r'^logout/', 'subscribe.views.logout', name='logout'),

    # API views
    url(r'^events/', 'base.views.events', name='events'),
    url(r'^createEvent', 'base.views.createEvent', name='createEvent'),
    url(r'^storeEvent', 'base.views.storeEvent', name='storeEvent'),
    url(r'^event/(?P<happening_id>\d+)/subscribe/(?P<chief_code>[a-zA-Z0-9_\-]+)$', 'subscribe.views.event_subscribe', name='event'),
    url(r'^event/(?P<happening_id>\d+)/unsubscribe/(?P<chief_code>[a-zA-Z0-9_\-]+)$', 'subscribe.views.event_unsubscribe', name='event'),
    url(r'^units/', 'base.views.units', name='units'),
    url(r'^districts/', 'base.views.districts', name='districts'),
    url(r'^timeslots/', 'base.views.timeslots', name='timeslots'),
    url(r'^topics/', 'base.views.topics', name='topics'),
    url(r'^chiefs/', 'base.views.chiefs', name='chiefs'),
    
    url(r'^boys/', 'base.views.boys', name='boys'),
    url(r'^boys/page/(?P<frm>\d+)$', 'base.views.boys_paginate', name='boys_paginate'),
    # url(r'^boy/assign/(?P<codice_censimento>\d+)$', 'base.views.boy_assign', name='boy_assign'),
    
    url(r'^subscribedChiefs/(?P<happening_id>\d+)$', 'subscribe.views.subscribedChiefs', name='subscribedChiefs'),
    url(r'^freeChiefs/(?P<happening_id>\d+)$', 'subscribe.views.freeChiefs', name='freeChiefs'),
    url(r'^persons/', 'base.views.persons', name='persons'),
    url(r'^validate-chief/', 'subscribe.views.validate', name='validate'),

    url(r'^admin/base/rover/(?P<pk>\d+)/do-compute-soddisfacimento/$', 'ragazzi.views.boy_evaluate', name='boy_evaluate'),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^print-events/(?P<unit>.+)/$', 'subscribe.views.print_events', name='print_events'),
)
