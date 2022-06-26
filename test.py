def ReferShift(request, id, date):
    myshiftrs = Shifts.objects.all().values()
    for x in myshifts:
        if x[_idx] == id and x[date] == date:
            return x[start], x[end]
    return 0, 0

def ChangeShift(request, id, date, start, end):
    if ReferShift(request, id, date) == (0, 0):
        shift = Shifts(_id=id, date=date, start=start, end=end)
        shift.save()
        return 1
    else:
        myshiftrs = Shifts.objects.all().values()
        for x in myshifts:
            if x[_idx] == id and x[date] == date:
                shift = Shifts.objects.get(id=x[id])
                shift.start = start
                shift.end = end
                shift.shiftcheck = False
                shift.save()
                return 1
    return 0


def ApproveShift(request, id, date, start, end):
    myshiftrs = Shifts.objects.all().values()
    for x in myshifts:
        if x[_idx] == id and x[date] == date:
            shift = Shifts.objects.get(id=x[id])
            if start == end:
                shift.delete()
            else:
                shift.shiftcheck = True
                shift.save()
            return 1
    return 0

def EditShift(request, id, date, start, end):
    tempshift = tempShifts(_id=id, date=date, start=start, end=end)
    tempshift.save()
    return 1

def PostShift(request, id, date, start, end):
    tempshiftrs = tempShifts.objects.all().values()
    for x in tempshifts:
        ChangeShift(request, x[id], x[date], x[start], x[end])
    return 1
