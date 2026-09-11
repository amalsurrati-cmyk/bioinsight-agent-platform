def calculate_tip (bill_amount, tip_percentage):
    return bill_amount * (tip_percentage / 100)
print(f'Tip for $100 at 15%: ${calculate_tip(100, 15)}')
print(f'Tip for $50 at 20%: ${calculate_tip(50, 20)}')
print(f'Tip for $75 at 18%: ${calculate_tip(75, 18)}')

task = {'title':'Buy groceries', 'done':True, 'priority':2}

if task['done']:
    print(f'✅ {task["title"]}')
else:
    print(f'❌ {task["title"]}')
task = {'title':'Buy groceries', 'done':False, 'priority':2}

if task['done']:
    print(f'✅ {task["title"]}')
else:
    print(f'❌ {task["title"]}')

