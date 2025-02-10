from django.db import models

# Create your models here.
class Computer(models.Model):
    STATUS = {
        'A': 'Available',
        'O': 'Occupied',
        'M': 'Maintenance',
    }
    computer_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    mac_adr = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=15, choices=STATUS, default=STATUS['A'])
    # student = models.JSONField()
    student_assigned = models.JSONField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    computer_position = models.JSONField(null=True)
    class Meta:
        db_table = 'computer'
    def __str__(self):
        return f"{self.name} - {self.mac_adr}"


class Student(models.Model):
    STATUS = {
        'A': 'Active',
        'I': 'Inactive',
        'D': 'Deleted'
    }
    TYPE = {
        'S': 'Student',
        'G': 'Guest',
    }
    student_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    status = models.CharField(max_length=15, choices=STATUS, default=STATUS['I'])
    computer = models.ForeignKey(Computer, on_delete=models.PROTECT, null=True, to_field='name')
    option = models.CharField(max_length=255, null=True)
    student_history = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    curr_hist_id = models.BigIntegerField(null=True)
    number_of_uses = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=100, choices=TYPE, default=TYPE['S'])
    def __str__(self):
        return f"{self.type} : {self.code} : {self.email} : {self.computer}"

    class Meta:
        ordering = ['-updated', '-created']

class Schedule(models.Model):

    DAY = {
        'M' : 'Monday',
        'T' : 'Tuesday',
        'W' : 'Wednesday',
        'Th' : 'Thursday',
        'F' : 'Friday',
        'Sa' : 'Saturday',
        'Su' : 'Sunday'
    }

    schedule_id = models.BigAutoField(primary_key=True)
    day = models.CharField(max_length=20, choices=DAY)
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    computer = models.ForeignKey(Computer, on_delete=models.PROTECT, to_field='name')
    student = models.ForeignKey(Student, on_delete=models.PROTECT, to_field='code')
    # description = models.CharField(max_length=500, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.day} : {self.start_hour}-{self.end_hour}"
    class Meta:
        ordering = ['-updated', '-created']


class History(models.Model):
    history_id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, to_field='code')
    computer = models.ForeignKey(Computer, on_delete=models.PROTECT, to_field='name')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=765, null=True)
    title = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ['-end_date']

    def __str__(self):
        return f'{self.student.code} - {self.title} - {self.computer.name} - Sart date : {self.start_date} <==> End date : {self.end_date}'