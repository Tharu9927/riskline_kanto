import win32com.client

TASK_ENUM_HIDDEN = 1
TASK_STATE = {0: 'Unknown',
              1: 'Disabled',
              2: 'Queued',
              3: 'Ready',
              4: 'Running'}

scheduler = win32com.client.Dispatch('Schedule.Service')
scheduler.Connect()

n = 0
folders = [scheduler.GetFolder('\\')]
while folders:
    folder = folders.pop(0)
    folders += list(folder.GetFolders(0))
    tasks = list(folder.GetTasks(TASK_ENUM_HIDDEN))
    n += len(tasks)
    for task in tasks:
        settings = task.Definition.Settings
        if task.path in ('\水系','\縦断'):
            print('Path       : %s' % task.Path)
            print('Hidden     : %s' % settings.Hidden)
            print('State      : %s' % TASK_STATE[task.State])
            print('Last Run   : %s' % task.LastRunTime)
            print('Last Result: %s\n' % task.LastTaskResult)
print('Listed %d tasks.' % n)