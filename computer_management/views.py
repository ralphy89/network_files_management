from django.shortcuts import render

# Create your views here.
# Sample list of computers
computers = [
    {
        "name": "Computer 1",
        "ip_address": "192.168.1.10",
        "mac_address": "00:1A:2B:3C:4D:5E",
        "status": "Available",
        "student": {
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
    },
    {
        "name": "Computer 2",
        "ip_address": "192.168.1.11",
        "mac_address": "11:22:33:44:55:66",
        "status": "Occupied",
        "student": {
            "name": "Jane Smith",
            "email": "jane.smith@example.com"
        }
    },
    {
        "name": "Computer 3",
        "ip_address": "192.168.1.12",
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "status": "Maintenance",
        "student": None
    },
    {
        "name": "Computer 4",
        "ip_address": "192.168.1.13",
        "mac_address": "12:34:56:78:90:AB",
        "status": "Available",
        "student": {
            "name": "Alice Brown",
            "email": "alice.brown@example.com"
        }
    },
    {
        "name": "Computer 5",
        "ip_address": "192.168.1.14",
        "mac_address": "98:76:54:32:10:FE",
        "status": "Occupied",
        "student": {
            "name": "Bob Green",
            "email": "bob.green@example.com"
        }
    }
]

# Sample data for testing student list
students = [
    {
        'name': 'John Smith',
        'email': 'john.smith@example.com',
        'computer': {
            'name': 'PC-001',
            'status': 'Active',
            'mac_address': '00:1B:44:11:3A:B7'
        }
    },
    {
        'name': 'Emma Watson',
        'email': 'emma.w@example.com',
        'computer': {
            'name': 'PC-002',
            'status': 'Active',
            'mac_address': '00:1B:44:11:3A:C8'
        }
    },
    {
        'name': 'Michael Johnson',
        'email': 'michael.j@example.com',
        'computer': None  # Not assigned to any computer
    },
    {
        'name': 'Sarah Davis',
        'email': 'sarah.d@example.com',
        'computer': {
            'name': 'PC-003',
            'status': 'Maintenance',
            'mac_address': '00:1B:44:11:3A:D9'
        }
    },
    {
        'name': 'David Wilson',
        'email': 'david.w@example.com',
        'computer': {
            'name': 'PC-004',
            'status': 'Active',
            'mac_address': '00:1B:44:11:3A:E0'
        }
    },
    {
        'name': 'Lisa Brown',
        'email': 'lisa.b@example.com',
        'computer': None  # Not assigned to any computer
    },
    {
        'name': 'James Anderson',
        'email': 'james.a@example.com',
        'computer': {
            'name': 'PC-005',
            'status': 'Inactive',
            'mac_address': '00:1B:44:11:3A:F1'
        }
    },
    {
        'name': 'Emily Martinez',
        'email': 'emily.m@example.com',
        'computer': {
            'name': 'PC-006',
            'status': 'Active',
            'mac_address': '00:1B:44:11:3A:G2'
        }
    },
    {
        'name': 'Robert Taylor',
        'email': 'robert.t@example.com',
        'computer': {
            'name': 'PC-007',
            'status': 'Maintenance',
            'mac_address': '00:1B:44:11:3A:H3'
        }
    },
    {
        'name': 'Maria Garcia',
        'email': 'maria.g@example.com',
        'computer': {
            'name': 'PC-008',
            'status': 'Active',
            'mac_address': '00:1B:44:11:3A:I4'
        }
    }
]



def computerManagements(request):
    template = 'computerManagement.html'
    page_object = {
        'computers': computers,
        'students': students  # Use the sample data
    }
    assert template == 'computerManagement.html', 'template should be \"computerManagement.html\"'
    return render(
        request,
        template,
        page_object,
    )