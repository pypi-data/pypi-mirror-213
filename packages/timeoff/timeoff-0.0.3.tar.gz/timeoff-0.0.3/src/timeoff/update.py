from datetime import datetime

from timeoff.exceptions import PolicyNotFoundError
from timeoff.model.entry import Accrued
from timeoff.model.policy import Policy
from timeoff.model.setting import Setting


def effective_policy(policies, date):
    """Return the policy in effect on the given date."""
    all_policy_dates = sorted(policies.keys())
    last = None
    for policy_date in all_policy_dates:
        if policy_date <= date:
            last = policy_date
        else:
            break
    if last is not None:
        return policies[last]
    msg = "No policy found for date."
    raise PolicyNotFoundError(msg)


def update_pto():
    all_policies = Policy.get()

    all_accrued_pto = Accrued.get()
    last_updated = Setting.get().starting_date if len(all_accrued_pto) == 0 else sorted(all_accrued_pto.keys())[-1]

    current_date = last_updated
    while current_date < datetime.today().date():
        policy = effective_policy(all_policies, current_date)
        current_date = policy.schedule.next_date(current_date)
        if current_date < datetime.today().date():
            Accrued(current_date, policy.rate).save()

