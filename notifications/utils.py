from.models import Notification

def create_notif(title, message, recipient, school, i_d, user_notif):
    notif=Notification()
    notif.title=title
    notif.school=school
    notif.message=message
    notif.i_d=i_d
    notif.recipient=recipient
    notif.is_user_notif=user_notif
    notif.save()
