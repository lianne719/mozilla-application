from bugzilla.agents import BMOAgent
from bugzilla.utils import get_credentials
from datetime import date,timedelta,datetime

username, password = get_credentials()

bmo = BMOAgent(username, password)

start = date(2012,10,9)
end = date(2012,11,19)

options = {
    'changed_after':    start.strftime('%Y-%m-%d'),
    'changed_before':   end.strftime('%Y-%m-%d'),
    'changed_field':    'cf_tracking_firefox17',
    'changed_from':     '+',
    'include_fields':   '_default,attachments,history',
    'field0-0-0':       'cf_status_firefox17',
    'type0-0-0':        'not_equals',
    'value0-0-0':       'fixed',
    'field0-1-0':       'cf_status_firefox17',
    'type0-1-0':        'not_equals',
    'value0-1-0':       'verified',
    'field0-2-0':       'cf_status_firefox17',
    'type0-2-0':        'not_equals',
    'value0-2-0':       'disabled',
    'field0-3-0':       'cf_status_firefox17',
    'type0-3-0':        'not_equals',
    'value0-3-0':       'unaffected',
}

buglist = bmo.get_bug_list(options)

print "Found %s bugs" % (len(buglist))

period = (end-start).days + 1

added = [0]*(period)
removed = [0]*(period)
fixed = [0]*(period)
new = 0
total = len(buglist)

for bug in buglist:
    related = True
    
    if bug.status == 'NEW':
        new = new + 1
    for changeset in bug.history:
        mod_date = date(changeset.change_time.year,changeset.change_time.month,changeset.change_time.day)
        index = (mod_date-start).days
        if index >= 0 and index < 42:
            for change in changeset.changes:
                if change.field_name == 'cf_tracking_firefox17':
                    if change.added == '+':
                        added[index] = added[index] + 1
                    elif change.removed == '+':
                        removed[index] = removed[index] + 1
                elif change.field_name == 'status':
                    if change.added == 'RESOLVED':
                        fixed[index] = fixed[index] + 1
                    if change.added == 'REOPENED':
                        fixed[index] = fixed[index] - 1
                elif change.field_name == 'cf_status_firefox17':
                    print change.added
                    if change.added == 'wontfix' or change.added == 'fixed':
                        fixed[index] = fixed[index] + 1

print new
                
f = open('results.txt', 'w')
f.write('date,added,removed,closed,total remaining\n')
date = start
index = 0

for a,r in zip(added,removed):
    total = total - fixed[index]
    f.write(date.strftime('%Y-%m-%d')+','+repr(added[index])+','+repr(removed[index])+','+repr(fixed[index])+','+repr(total)+'\n')
    index = index + 1
    date = date + timedelta(days=1)
    
f.close()
