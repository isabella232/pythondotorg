from sponsors.models import Sponsorship, StatementOfWork
from sponsors import notifications


class CreateSponsorshipApplicationUseCase:
    def __init__(self, notifications):
        self.notifications = notifications

    def execute(self, user, sponsor, benefits, package=None, request=None):
        sponsorship = Sponsorship.new(sponsor, benefits, package, submited_by=user)

        for notification in self.notifications:
            notification.notify(request=request, sponsorship=sponsorship)

        return sponsorship

    @classmethod
    def build(cls):
        uc_notifications = [
            notifications.AppliedSponsorshipNotificationToPSF(),
            notifications.AppliedSponsorshipNotificationToSponsors(),
        ]
        return cls(uc_notifications)


class RejectSponsorshipApplicationUseCase:
    def __init__(self, notifications):
        self.notifications = notifications

    def execute(self, sponsorship, request=None):
        sponsorship.reject()
        sponsorship.save()

        for notification in self.notifications:
            notification.notify(request=request, sponsorship=sponsorship)

        return sponsorship

    @classmethod
    def build(cls):
        uc_notifications = [
            notifications.RejectedSponsorshipNotificationToPSF(),
            notifications.RejectedSponsorshipNotificationToSponsors(),
        ]
        return cls(uc_notifications)


class ApproveSponsorshipApplicationUseCase:
    def __init__(self, notifications):
        self.notifications = notifications

    def execute(self, sponsorship, request=None):
        sponsorship.approve()
        sponsorship.save()
        statement_of_work = StatementOfWork.new(sponsorship)

        for notification in self.notifications:
            notification.notify(
                request=request,
                sponsorship=sponsorship,
                statement_of_work=statement_of_work,
            )

        return sponsorship

    @classmethod
    def build(cls):
        uc_notifications = []
        return cls(uc_notifications)
