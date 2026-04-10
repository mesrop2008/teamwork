from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from datetime import date, timedelta
from .models import Alliance, Group, Employee, Shift


def get_time_options():
    time_options = []
    for h in range(6, 24):
        for m in [0, 15, 30, 45]:
            if h == 6 and m < 30:
                continue
            time_options.append(f"{h:02d}:{m:02d}")
    return time_options


def get_summary(all_shifts):
    if not all_shifts.exists():
        return None
    day_names = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    by_day = [0] * 7
    before_11 = 0
    after_19 = 0
    total = all_shifts.count()
    for s in all_shifts:
        by_day[s.date.weekday()] += 1
        if s.start_time and s.start_time.hour < 11:
            before_11 += 1
        if s.end_time and s.end_time.hour >= 19:
            after_19 += 1
    return {
        'by_day': [
            {'name': day_names[i], 'count': by_day[i], 'percent': round(by_day[i] / total * 100, 2)}
            for i in range(7)
        ],
        'before_11': before_11,
        'before_11_pct': round(before_11 / total * 100, 2),
        'after_19': after_19,
        'after_19_pct': round(after_19 / total * 100, 2),
    }


def index(request):
    alliances = Alliance.objects.all()
    selected_alliance_id = request.GET.get('alliance')
    selected_group_id = request.GET.get('group')
    selected_employee_id = request.GET.get('employee')

    groups = Group.objects.filter(alliance_id=selected_alliance_id) if selected_alliance_id else Group.objects.none()
    employees = Employee.objects.filter(group_id=selected_group_id) if selected_group_id else Employee.objects.none()

    shifts = Shift.objects.none()
    selected_employee = None
    if selected_employee_id:
        selected_employee = Employee.objects.get(id=selected_employee_id)
        shifts = Shift.objects.filter(employee_id=selected_employee_id)

    today = date.today()
    dates = [today + timedelta(days=i) for i in range(14)]
    all_shifts = Shift.objects.select_related('employee__group__alliance').all()

    is_manager = request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)

    context = {
        'alliances': alliances,
        'groups': groups,
        'employees': employees,
        'shifts': shifts,
        'selected_employee': selected_employee,
        'selected_alliance_id': int(selected_alliance_id) if selected_alliance_id else None,
        'selected_group_id': int(selected_group_id) if selected_group_id else None,
        'selected_employee_id': int(selected_employee_id) if selected_employee_id else None,
        'dates': dates,
        'all_shifts': all_shifts,
        'time_options': get_time_options(),
        'summary': get_summary(all_shifts),
        'is_manager': is_manager,
    }
    return render(request, 'index.html', context)


def add_shift(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        shift_date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time') or None
        if start_time == 'day_off':
            start_time = None
            end_time = None
        Shift.objects.create(employee_id=employee_id, date=shift_date, start_time=start_time, end_time=end_time)
        employee = Employee.objects.get(id=employee_id)
        return redirect(f'/?alliance={employee.group.alliance_id}&group={employee.group_id}&employee={employee_id}')
    return redirect('/')


def delete_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    employee = shift.employee
    shift.delete()
    return redirect(f'/?alliance={employee.group.alliance_id}&group={employee.group_id}&employee={employee.id}')


def confirm_shift(request, shift_id):
    if not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)):
        return redirect('/')
    shift = get_object_or_404(Shift, id=shift_id)
    employee = shift.employee
    shift.is_confirmed = True
    shift.save()
    return redirect(f'/?alliance={employee.group.alliance_id}&group={employee.group_id}&employee={employee.id}')


def login_view(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            error = 'Неверный логин или пароль'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/')
