from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Task, Note

class Calendar(HTMLCalendar):
    cssclass_month_head = "text-center month-head display-6"
    cssclasses_weekday_head = ["display-6", "display-6", "display-6","display-6","display-6","display-6","display-6",]

    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def generatePageUrl(self, day):
        return (f'/{self.year}/{self.month}/{day}') 
	
	# formats a day as a td
	# filter events by day
    def formatday(self, day, tasks):
        task_per_day = Task.objects.filter(due_date__day=day)
        notes_per_day = Note.objects.filter(created_on__day=day)
        
        d = ''
        for task in task_per_day:
            d += f'<li class="list-group-item"><i class="bi bi-clock"></i> {task.title} </li>'
        
        for note in notes_per_day:
            if note.is_important:
                d += f'<li class="list-group-item"><strong>!! {note.title}</strong> </li>'
            else:
                d += f'<li class="list-group-item">- {note.title} </li>'
                
        if day != 0:
            return f"<td><span class='date'><a class='nav-link' href='{self.generatePageUrl(day)}'> {day} </a></span><ul class='list-group list-group-flush'> {d} </ul></td>"
        return '<td></td>'

	# formats a week as a tr 
    def formatweek(self, theweek, tasks):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, tasks)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        tasks = Task.objects.filter(due_date__year = self.year, due_date__month=self.month)
        notes = Note.objects.filter(created_on__year=self.year,created_on__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar table table-bordered">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, tasks)}\n'
        cal += f'</table>'
        return cal