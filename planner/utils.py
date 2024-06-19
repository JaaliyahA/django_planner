from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Task, Note

class Calendar(HTMLCalendar):
    #cssclasses_weekday_head = ["mon col-1", "tue col-1", "wed col-1", "thu col-1", "fri col-1", "sat col-1", "sun col-1"]

    def __init__(self, year=None, month=None, user=None):
        self.year = year
        self.month = month
        self.user = user
        super(Calendar, self).__init__()

    def generatePageUrl(self, day):
        return (f'/{self.year}/{self.month}/{day}') 
	
	# formats a day as a td
	# filter events by day
    def formatday(self, day):
        task_per_day = Task.objects.filter(due_date__day=day,
                                           due_date__month=self.month,
                                           due_date__year = self.year,
                                           user = self.user)
        notes_per_day = Note.objects.filter(created_on__day=day, 
                                            created_on__month = self.month,
                                            created_on__year = self.year,
                                            user = self.user)
        
        d = ''
        for task in task_per_day:
            d += f'<li class=""><i class="bi bi-clock"></i> {task.title} </li>'
        
        for note in notes_per_day:
            if note.is_important:
                d += f'<li class="px-0"><strong>!! {note.title}</strong> </li>'
            else:
                d += f'<li class="px-0">- {note.title} </li>'
                
        if day != 0:
            return f"<td class='p-0'><span class='pt-0 mt-0'><a class='nav-link text-center' href='{self.generatePageUrl(day)}'> {day} </a></span><ul class='px-1'> {d} </ul></td>"
        return '<td></td>'

	# formats a week as a tr 
    def formatweek(self, theweek):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        cal = f'<table class="calendar table table-bordered ">\n'
        cal += f'<thead>{self.formatweekheader()}</thead>\n'
        print(cal)
        cal += f'<tbody>\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week)}\n'
        cal += f'</tbody>\n</table>'
        return cal