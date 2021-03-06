# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class BdpAuthRole(models.Model):
    rid = models.AutoField(primary_key=True)
    role_name = models.CharField(unique=True, max_length=50)
    role_type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bdp_auth_role'


class BdpAuthRoleReport(models.Model):
    id = models.BigAutoField(primary_key=True)
    rid = models.ForeignKey(BdpAuthRole, models.DO_NOTHING, db_column='rid')
    report = models.ForeignKey('BdpReportConfig', models.DO_NOTHING)
    field = models.ForeignKey('BdpReportField', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'bdp_auth_role_report'
        unique_together = (('rid', 'field', 'report'),)


class BdpAuthRoleUrl(models.Model):
    id = models.BigAutoField(primary_key=True)
    rid = models.ForeignKey(BdpAuthRole, models.DO_NOTHING, db_column='rid')
    url = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'bdp_auth_role_url'
        unique_together = (('rid', 'url'),)


class BdpAuthUser(models.Model):
    uid = models.IntegerField(primary_key=True)
    user_name = models.CharField(unique=True, max_length=50)
    real_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=64)
    salt = models.CharField(max_length=16)
    state = models.IntegerField()
    city_id_list = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bdp_auth_user'


class BdpAuthUserConfig(models.Model):
    uid = models.IntegerField(primary_key=True)
    area = models.TextField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    channel_belong_to = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bdp_auth_user_config'


class BdpAuthUserRole(models.Model):
    uid = models.ForeignKey(BdpAuthUser, models.DO_NOTHING, db_column='uid')
    rid = models.ForeignKey(BdpAuthRole, models.DO_NOTHING, db_column='rid')

    class Meta:
        managed = False
        db_table = 'bdp_auth_user_role'


class BdpCustomAuth(models.Model):
    cid = models.ForeignKey('BdpCustomTable', models.DO_NOTHING, db_column='cid')
    uid = models.IntegerField()
    auth_type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bdp_custom_auth'


class BdpCustomClass(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(unique=True, max_length=16)

    class Meta:
        managed = False
        db_table = 'bdp_custom_class'


class BdpCustomTable(models.Model):
    cid = models.AutoField(primary_key=True)
    custom_name = models.CharField(unique=True, max_length=30)
    custom_name_cn = models.CharField(max_length=30)
    class_field = models.ForeignKey(BdpCustomClass, models.DO_NOTHING, db_column='class_id')  # Field renamed because it was a Python reserved word.
    notes = models.CharField(max_length=100, blank=True, null=True)
    create_uid = models.IntegerField()
    create_time = models.IntegerField()
    update_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bdp_custom_table'


class BdpDataVisualBlockConfig(models.Model):
    bid = models.AutoField(primary_key=True)
    vid = models.ForeignKey('BdpDataVisualReport', models.DO_NOTHING, db_column='vid')
    region_id = models.IntegerField()
    block_name = models.CharField(max_length=64)
    source_name = models.CharField(max_length=64, blank=True, null=True)
    block_type = models.IntegerField()
    chart_type = models.IntegerField(blank=True, null=True)
    block_content = models.TextField(blank=True, null=True)
    report_type = models.IntegerField(blank=True, null=True)
    source_filter = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'bdp_data_visual_block_config'


class BdpDataVisualBlockField(models.Model):
    fid = models.AutoField(primary_key=True)
    bid = models.ForeignKey(BdpDataVisualBlockConfig, models.DO_NOTHING, db_column='bid')
    field_name = models.CharField(max_length=64)
    field_name_cn = models.CharField(max_length=64)
    method = models.IntegerField(blank=True, null=True)
    formula = models.CharField(max_length=400, blank=True, null=True)
    field_type = models.IntegerField()
    is_sort = models.IntegerField()
    furl_mode = models.IntegerField(blank=True, null=True)
    is_filter = models.IntegerField(blank=True, null=True)
    is_show = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bdp_data_visual_block_field'


class BdpDataVisualMenu(models.Model):
    mid = models.AutoField(primary_key=True)
    menu_name = models.CharField(max_length=128)
    create_time = models.IntegerField()
    create_uid = models.IntegerField()
    update_time = models.IntegerField()
    update_uid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bdp_data_visual_menu'


class BdpDataVisualReport(models.Model):
    vid = models.AutoField(primary_key=True)
    mid = models.ForeignKey(BdpDataVisualMenu, models.DO_NOTHING, db_column='mid')
    visual_report_name = models.CharField(max_length=64)
    is_down = models.IntegerField()
    online = models.IntegerField()
    create_time = models.IntegerField()
    create_uid = models.IntegerField()
    update_time = models.IntegerField()
    update_uid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bdp_data_visual_report'


class BdpReportConfig(models.Model):
    rid = models.AutoField(primary_key=True)
    mid = models.ForeignKey('BdpReportMenu', models.DO_NOTHING, db_column='mid')
    report_name = models.CharField(max_length=64)
    source_type = models.IntegerField()
    source_name = models.CharField(max_length=64)
    source_filter = models.CharField(max_length=256)
    chart_type = models.IntegerField()
    report_type = models.IntegerField()
    is_down = models.IntegerField()
    summary = models.CharField(max_length=6)
    tips = models.TextField(blank=True, null=True)
    tab_sort = models.IntegerField()
    online = models.IntegerField()
    create_time = models.IntegerField()
    create_uid = models.IntegerField()
    update_time = models.IntegerField()
    update_uid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bdp_report_config'


class BdpReportField(models.Model):
    fid = models.AutoField(primary_key=True)
    rid = models.ForeignKey(BdpReportConfig, models.DO_NOTHING, db_column='rid')
    display_order = models.IntegerField()
    field_name = models.CharField(max_length=30)
    field_name_cn = models.CharField(max_length=30)
    parent_name = models.CharField(max_length=30)
    field_type = models.IntegerField()
    furl_mode = models.IntegerField()
    sort = models.IntegerField()
    row_filter = models.IntegerField()
    method = models.IntegerField()
    formula = models.CharField(max_length=400)
    display_mode = models.IntegerField()
    display_mode_value = models.IntegerField()
    display_chart = models.IntegerField()
    special = models.IntegerField()
    special_value = models.CharField(max_length=30)
    input_switch = models.IntegerField()
    input_default = models.TextField(blank=True, null=True)
    input_user = models.TextField(blank=True, null=True)
    tips = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'bdp_report_field'


class BdpReportMenu(models.Model):
    mid = models.AutoField(primary_key=True)
    parent_mid = models.IntegerField()
    menu_path = models.CharField(max_length=64)
    menu_name = models.CharField(max_length=128)
    is_terminal = models.IntegerField()
    display_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bdp_report_menu'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
