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
    class Meta:
        db_table = 'computer'
    def __str__(self):
        return f"{self.name} - {self.mac_adr}"


class Student(models.Model):
    STATUS = {
        'A': 'Active',
        'I': 'Inactive',
    }
    student_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    status = models.CharField(max_length=15, choices=STATUS, default=STATUS['I'])
    computer = models.ForeignKey(Computer, on_delete=models.PROTECT, null=True, to_field='name')
    def __str__(self):
        return f"{self.code} : {self.email} : {self.computer}"


