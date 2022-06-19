from django.urls import path
from .views import (
    AlertListView, CareerGroupJobsAjaxView,
    BackupListView, BackupFormView, RestoreFormView,
    DownloadBackupView, DeleteBackupView, RestoreBackupView
)
app_name = 'core'

urlpatterns = [
    path('alerts/', AlertListView.as_view(), name='alerts'),
    path('careers/<group_id>/', CareerGroupJobsAjaxView.as_view(), name='careers'),
    path('backup/', BackupListView.as_view(), name="backups"),
    path('backup/new/', BackupFormView.as_view(), name="new_backup"),
    path('backup/<name>/download/', DownloadBackupView.as_view(), name="download_backup"),
    path('backup/<name>/delete/', DeleteBackupView.as_view(), name="delete_backup"),
    path('restore/', RestoreFormView.as_view(), name="restore"),
    path('restore/<name>/', RestoreBackupView.as_view(), name="restore_backup"),
]