from student.models import Student


def attendance_percentage(request, student_id):
    student = Student.objects.get(id=student_id)
    
    # Total attendance records for the student
    total_attendances = student.attendance_status.count()
    
    # The number of days the student was present
    present_days = student.attendance_status.filter(status=attended).count()

    # Calculate the percentage
    percentage = 0.0
    if total_attendances > 0:
        percentage = (present_days / total_attendances) * 100
    return percentage