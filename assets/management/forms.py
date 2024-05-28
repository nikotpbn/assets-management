from django import forms

class AssetEditAndCreateForm(forms.ModelForm):
    class Meta:
        fields = ["name", "address", "cover", "slug"]