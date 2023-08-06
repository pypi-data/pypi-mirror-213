from typing import Optional

import humanize

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.html import format_html
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from allianceauth.notifications import notify

from .forms import CreateRequestForm, RejectRequestForm
from .helpers import user_for_display
from .models import InactivityPing, InactivityPingConfig, LeaveOfAbsence, Webhook


def add_common_context(request, context: Optional[dict] = None) -> dict:
    """adds the common context used by all view"""
    context = context or {}
    new_context = {
        **{
            "app_title": "Leave of Absence",
            "unapproved_count": LeaveOfAbsence.objects.unapproved_count(),
        },
        **context,
    }
    return new_context


def make_action_button_html(
    label: str,
    url: str,
    button_type: str = "default",
    tooltip: str = "",
    disabled: bool = False,
) -> str:
    """Make HTML for an action button."""
    return format_html(
        '<a href="{}" class="btn btn-{}"{}{}>{}</a>',
        url,
        button_type,
        format_html(' title="{}"', tooltip) if tooltip else "",
        format_html(' disabled="disabled"') if disabled else "",
        label,
    )


@login_required
@permission_required("inactivity.basic_access")
def index(request):
    return redirect("inactivity:my_requests")


# ---- my requests -----


@login_required
@permission_required("inactivity.basic_access")
def my_requests(request):
    context = {"page_title": _("My Requests")}
    return render(
        request, "inactivity/my_requests.html", add_common_context(request, context)
    )


@login_required
@permission_required("inactivity.basic_access")
def my_open_requests_data(request):
    data = []
    for loa_request in LeaveOfAbsence.objects.filter_pending().filter(
        user=request.user
    ):
        row = loa_request.to_output_dict()
        actions = make_action_button_html(
            label=_("Cancel"),
            url=reverse("inactivity:cancel_loa_request", args=[loa_request.pk]),
            button_type="danger",
            tooltip="Cancel this request",
        )
        row["actions"] = actions
        data.append(row)
    return JsonResponse({"data": data})


@login_required
@permission_required("inactivity.basic_access")
def my_completed_requests_data(request):
    data = []
    for loa_request in (
        LeaveOfAbsence.objects.filter_processed()
        .filter(user=request.user)
        .annotate_status()
    ):
        row = loa_request.to_output_dict()
        data.append(row)
    return JsonResponse({"data": data})


@login_required
@permission_required("inactivity.basic_access")
def create_loa_request(request):
    if request.method == "POST":
        form = CreateRequestForm(request.POST, user=request.user)
        if form.is_valid():
            loa: LeaveOfAbsence = form.save()
            messages.info(
                request,
                format_html(_("Your request has been submitted for review: %s") % loa),
            )
            message = _("New request: %s") % loa
            Webhook.objects.send_message_to_active_webhooks(
                loa, Webhook.NotificationType.LOA_NEW, message
            )
            return redirect("inactivity:index")

    else:
        form = CreateRequestForm(user=request.user)

    context = {"form": form}
    return render(request, "inactivity/create_loa.html", context)


@login_required
@permission_required("inactivity.basic_access")
def cancel_loa_request(request, loa_request_pk):
    loa = get_object_or_404(LeaveOfAbsence, pk=loa_request_pk, user=request.user)
    loa.delete()
    messages.info(request, format_html(_("%s has been canceled.") % loa))
    return redirect("inactivity:index")


# ---- manage requests -----


@login_required
@permission_required("inactivity.manage_leave")
def manage_requests(request):
    context = {"page_title": _("Manage Requests")}
    return render(
        request, "inactivity/manage_requests.html", add_common_context(request, context)
    )


@login_required
@permission_required("inactivity.manage_leave")
def list_pending_loa_requests(request):
    data = []
    for loa_request in LeaveOfAbsence.objects.filter_pending():
        row = loa_request.to_output_dict()
        actions = [
            make_action_button_html(
                label="Approve",
                url=reverse("inactivity:approve_loa_request", args=[loa_request.pk]),
                button_type="success",
                tooltip=_("Approve this request"),
            ),
            make_action_button_html(
                label=_("Deny"),
                url=reverse("inactivity:deny_loa_request", args=[loa_request.pk]),
                button_type="danger",
                tooltip=_("Deny this request"),
            ),
        ]
        row["actions"] = " ".join(actions)
        data.append(row)
    return JsonResponse({"data": data})


@login_required
@permission_required("inactivity.manage_leave")
def list_processed_loa_requests(request):
    data = []
    for loa_request in LeaveOfAbsence.objects.filter_processed().annotate_status():
        row = loa_request.to_output_dict()
        row["actions"] = ""
        data.append(row)
    return JsonResponse({"data": data})


@login_required
@permission_required("inactivity.manage_leave")
def approve_loa_request(request, loa_request_pk):
    loa: LeaveOfAbsence = get_object_or_404(LeaveOfAbsence, pk=loa_request_pk)
    loa.approver = request.user
    loa.save()
    messages.success(request, format_html(_("Your have approved: %s") % loa))
    message = _("%(loa)s has been approved by %(approver_name)s") % {
        "loa": loa,
        "approver_name": loa.approver_name,
    }
    notify.success(loa.user, title="LOA approved", message=message)
    Webhook.objects.send_message_to_active_webhooks(
        loa, Webhook.NotificationType.LOA_APPROVED, message
    )
    return redirect("inactivity:manage_requests")


@login_required
@permission_required("inactivity.manage_leave")
def deny_loa_request(request, loa_request_pk):
    loa_request: LeaveOfAbsence = get_object_or_404(LeaveOfAbsence, pk=loa_request_pk)
    requestor = loa_request.user

    if request.method == "POST":
        form = RejectRequestForm(request.POST)
        if form.is_valid():
            loa_request.approver = request.user
            loa_request.reason = form.cleaned_data["reason"]
            loa_request.save()
            messages.info(request, _("%s has been denied") % loa_request)
            manager_display = user_for_display(loa_request.approver)
            message = _(
                "%(loa)s has been denied by %(manager)s. Reason: %(reason)s"
            ) % {
                "loa": loa_request,
                "manager": manager_display.name,
                "reason": loa_request.reason,
            }
            notify.danger(requestor, "LOA rejected", message)
            return redirect("inactivity:manage_requests")

    else:
        form = RejectRequestForm(initial={"request": str(loa_request)})

    return render(
        request,
        "inactivity/reject_request.html",
        {"form": form, "loa_request": loa_request},
    )


# ---- inactive users -----


@login_required
@permission_required("inactivity.basic_access")
def inactive_users(request):
    has_policies = InactivityPingConfig.objects.exists()
    context = {"page_title": _("Inactive users"), "has_policies": has_policies}
    return render(
        request, "inactivity/inactive_users.html", add_common_context(request, context)
    )


@login_required
@permission_required("inactivity.basic_access")
def inactive_users_data(request):
    data = []
    for obj in InactivityPing.objects.all():
        obj: InactivityPing
        user_obj = user_for_display(obj.user)
        row = {
            "pk": obj.pk,
            "user_html": {"display": user_obj.html, "sort": user_obj.name},
            "last_login_at": {
                "display": humanize.naturaltime(obj.last_login_at, when=now())
                if obj.last_login_at
                else "?",
                "sort": obj.last_login_at.isoformat() if obj.last_login_at else None,
            },
            "policy": obj.config.name,
            "notified_at": {
                "display": humanize.naturaltime(obj.timestamp, when=now()),
                "sort": obj.timestamp.isoformat(),
            },
        }
        data.append(row)
    return JsonResponse({"data": data})
