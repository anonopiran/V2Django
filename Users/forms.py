from django.forms import ModelForm

from Users.models import Subscription


class SubscriptionForm(ModelForm):
    def get_initial_for_field(self, field, field_name):
        v_ = super().get_initial_for_field(field, field_name)
        if field_name == "volume":
            v_ /= 1024**3
        return v_

    def clean_volume(self):
        data = self.cleaned_data["volume"]
        return data * 1024**3

    class Meta:
        model = Subscription
        fields = "__all__"
