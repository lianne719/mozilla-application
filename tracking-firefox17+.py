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
    'field0-0-0':       'cf_status_firefox17',
    'type0-0-0':        'not_equals',
    'value0-0-0':       'disabled',
    'field0-1-0':       'cf_status_firefox17',
    'type0-1-0':        'not_equals',
    'value0-1-0':       'unaffected',
    #'field0-2-0':       'cf_status_firefox17',
    #'type0-2-0':        'not_equals',
    #'value0-2-0':       'verified',
    'field0-2-0':       'cf_tracking_firefox17',
    'type0-2-0':        'equals',
    'value0-2-0':       '+',
    #'field0-3-0':       'cf_status_firefox17',
    #'type0-3-0':        'not_equals',
    #'value0-3-0':       'wontfix',
    #'field0-3-0':       'cf_status_firefox17',
    #'type0-3-0':        'not_equals',
    #'value0-3-0':       'fixed',
    'include_fields':   '_default,attachments,history',
}

buglist = bmo.get_bug_list(options)

print "Found %s bugs" % (len(buglist))

period = (end-start).days + 1

added = [0]*(period)
removed = [0]*(period)
fixed = [0]*(period)
new = 0
total = len(buglist)
fixed_bugs = []

for bug in buglist:
    related = True
    for changeset in bug.history:
        mod_time = changeset.change_time - timedelta(hours=8)
        mod_date = date(mod_time.year,mod_time.month,mod_time.day)
        index = (mod_date-start).days
        if index >= 0 and index < period:
            for change in changeset.changes:
                if change.field_name == 'cf_tracking_firefox17':
                    if change.added == '+':
                        added[index] = added[index] + 1
                    elif change.removed == '+':
                        removed[index] = removed[index] + 1
                elif change.field_name == 'status':
                    print change.added
                    if (change.added == 'RESOLVED' or change.added == 'VERIFIED') and bug not in fixed_bugs:
                        fixed[index] = fixed[index] + 1
                        fixed_bugs.append(bug)
                    if change.added == 'REOPENED' and bug in fixed_bugs:
                        fixed[index] = fixed[index] - 1
                        fixed_bugs.remove(bug)
                elif change.field_name == 'cf_status_firefox17':
                    if (change.added == 'fixed' or change.added == 'wontfix' or change.added == 'verified') and bug not in fixed_bugs:
                        print change.added
                        fixed[index] = fixed[index] + 1
                        fixed_bugs.append(bug)

for bug in fixed_bugs:
    if bug in buglist:
        buglist.remove(bug)
        
print buglist
                
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
