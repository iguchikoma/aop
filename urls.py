from django.conf.urls import patterns, include, url

urlpatterns = patterns('pm.views',
#    url(r'^ne_types$', 'ne_types_crud'),
#    url(r'^ne_types/(?P<ne_type>\w+)/nes$', 'nes_crud'),
#    url(r'^ne_types/(?P<ne_type>\w+)/nes/(?P<ne_name>[\w-]+)$', 'ne_crud'),
#    url(r'^ne_types/(?P<ne_type>\w+)/cmds$', 'tl1_cmds_crud'),
#    url(r'^ne_types/(?P<ne_type>\w+)/out_v$', 'out_v_crud'),
#    url(r'^ne_types/(?P<ne_type>\w+)/chk_res$', 'chk_res'),
#    url(r'^ne_types/(?P<ne_type>\w+)/(?P<ne_name>[\w-]+)/topology$', 'topology_chk'),
#    url(r'^nes$', 'nes_file_upload'),
    url(r'^v1/cfgs$', 'cfgs_crud'),
    url(r'^v1/vrfs$', 'vrfs_crud'),
    url(r'^v1/targets$', 'targets_crud'),
)
