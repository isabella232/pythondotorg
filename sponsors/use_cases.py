from sponsors import notifications
from sponsors.models import Sponsorship, StatementOfWork


class BaseUseCaseWithNotifications:
    notifications = []

    def __init__(self, notifications):
        self.notifications = notifications

    def notify(self, **kwargs):
        for notification in self.notifications:
            notification.notify(**kwargs)

    @classmethod
    def build(cls):
        return cls(cls.notifications)


class CreateSponsorshipApplicationUseCase(BaseUseCaseWithNotifications):
    notifications = [
        notifications.AppliedSponsorshipNotificationToPSF(),
        notifications.AppliedSponsorshipNotificationToSponsors(),
    ]

    def execute(self, user, sponsor, benefits, package=None, request=None):
        sponsorship = Sponsorship.new(sponsor, benefits, package, submited_by=user)
        self.notify(sponsorship=sponsorship, request=request)
        return sponsorship


class RejectSponsorshipApplicationUseCase(BaseUseCaseWithNotifications):
    notifications = [
        notifications.RejectedSponsorshipNotificationToPSF(),
        notifications.RejectedSponsorshipNotificationToSponsors(),
    ]

    def execute(self, sponsorship, request=None):
        sponsorship.reject()
        sponsorship.save()
        self.notify(request=request, sponsorship=sponsorship)
        return sponsorship


class ApproveSponsorshipApplicationUseCase(BaseUseCaseWithNotifications):
    def execute(self, sponsorship, start_date, end_date, **kwargs):
        sponsorship.approve(start_date, end_date)
        level_name = kwargs.get("level_name")
        fee = kwargs.get("sponsorship_fee")
        if level_name:
            sponsorship.level_name = level_name
        if fee:
            sponsorship.sponsorship_fee = fee

        sponsorship.save()
        statement_of_work = StatementOfWork.new(sponsorship)

        self.notify(
            request=kwargs.get("request"),
            sponsorship=sponsorship,
            statement_of_work=statement_of_work,
        )

        return sponsorship
