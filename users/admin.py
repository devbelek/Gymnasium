from django.contrib import admin
from .models import UserProfile, Comment, CommentReply, Like, Donation, ConfirmedDonation


admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(CommentReply)
admin.site.register(Like)

class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date', 'is_verified')
    readonly_fields = ('user', 'amount', 'date', 'comment', 'confirmation_file')
    list_filter = ('is_verified',)
    actions = ['mark_as_verified']

    def mark_as_verified(self, request, queryset):
        for donation in queryset:
            donation.is_verified = True
            donation.save()
            ConfirmedDonation.objects.create(
                donation=donation,
                user=donation.user,
                comment=donation.comment
            )
            self.message_user(request, f"Donation ID {donation.id} has been verified.")
    mark_as_verified.short_description = "Сделать подтвержденными выбранные переводы"

admin.site.register(Donation, DonationAdmin)


@admin.register(ConfirmedDonation)
class ConfirmedDonationAdmin(admin.ModelAdmin):
    readonly_fields = ['donation', 'user', 'date', 'comment']