from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist

from core.models import EmailRecovery

from django.conf import settings
from django.utils import timezone

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    TemplateId,
    From,
    Subject,
    Email,
    Personalization,
)

from uuid import UUID


# Create your views here.
def auth_login(request):
    if request.user.is_authenticated:
        return redirect("asset-list")

    email = None
    password = None
    msg = None

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password", None)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("asset-list")

        msg = "Email ou senha incorretos."

    return render(request, "login.html", {"email": email, "error": msg})


def auth_logout(request):
    logout(request)
    return redirect("index")


def password_recover_new(request):
    token_string = request.GET.get("token", None)
    try:
        UUID(token_string, version=4)
        obj = EmailRecovery.objects.get(token=token_string)
        expired = obj.expiration - timezone.now() < timezone.timedelta(hours=0)
        if expired:
            return render(
                request, "password/recover.html", {"error": "Token expirado."}
            )

        if request.method == "POST":
            pw = request.POST.get("password", None)
            pw2 = request.POST.get("password2", None)
            if pw == pw2:
                obj.user.set_password(pw)
                obj.user.save()
                obj.delete()
                logout(request)
                return redirect("/")

        return render(request, "password/new.html", {"token": token_string})
    except ObjectDoesNotExist:
        return redirect("/")
    except ValueError:
        return redirect("/")


def password_recover(request):
    error = ""
    success = ""
    email = ""
    if request.method == "POST":
        email = request.POST.get("email", None)
        if email:
            try:
                user = get_user_model().objects.get(email=email)
                obj = EmailRecovery.objects.filter(user=user).order_by("created_at")
                if not obj:
                    expiration = timezone.now() + timezone.timedelta(hours=1)
                    obj = EmailRecovery.objects.create(user=user, expiration=expiration)

                elif obj and obj[0].expiration - timezone.now() < timezone.timedelta(
                    hours=0
                ):
                    obj.delete()
                    expiration = timezone.now() + timezone.timedelta(hours=1)
                    obj = EmailRecovery.objects.create(user=user, expiration=expiration)
                else:
                    obj = obj[0]

                message = Mail()
                message.from_email = From("nikobeltrao@hotmail.com", "Beltrão Imóveis")
                message.subject = Subject("Recuperação de senha")
                message.template_id = TemplateId("d-625d7825c2494f2092aa2de9fa342543")

                personalization = Personalization()
                personalization.add_to(Email(obj.user.email))
                personalization.dynamic_template_data = {
                    "email": f"{obj.user.email}",
                    "link": f"https://beltraoimoveis.com/password/recover/new/?token={obj.token}",
                }

                message.add_personalization(personalization)
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                response = sg.send(message=message)

                if response.status_code == 202:
                    success = "Email de recuperação enviado"

            except ObjectDoesNotExist:
                error = "Um usuário com este email não existe"
            except Exception as e:
                print(f"Algo de errado aconteceu: {e}")
                error = "Algo de errado aconteceu."
        else:
            error = "Email Inválido"

    return render(
        request,
        "password/recover.html",
        {"error": error, "success": success, "email": email},
    )
