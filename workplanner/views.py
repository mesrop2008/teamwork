from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from datetime import date, timedelta
from .models import Alliance, Group, Employee, Shift


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
    }
    return render(request, 'index.html', context)


def add_shift(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        shift_date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        Shift.objects.create(
            employee_id=employee_id,
            date=shift_date,
            start_time=start_time,
            end_time=end_time,
        )

    employee = Employee.objects.get(id=employee_id)
    return redirect(f'/?alliance={employee.group.alliance_id}&group={employee.group_id}&employee={employee_id}')


def delete_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    employee = shift.employee
    shift.delete()
    return redirect(f'/?alliance={employee.group.alliance_id}&group={employee.group_id}&employee={employee.id}')


def get_groups(request):
    alliance_id = request.GET.get('alliance_id')
    groups = list(Group.objects.filter(alliance_id=alliance_id).values('id', 'name'))
    return JsonResponse(groups, safe=False)


def get_employees(request):
    group_id = request.GET.get('group_id')
    employees = list(Employee.objects.filter(group_id=group_id).values('id', 'full_name'))
    return JsonResponse(employees, safe=False)