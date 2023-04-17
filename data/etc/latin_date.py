totalDays = 366
Nonde_Ignore_dates = ['Mar.', 'May.', 'Jul.', 'Oct.']
monthDates = [[1, 'Kalendae'], [5, 'Nonde'], [13, 'Idas']]
months = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']
mongthLength = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

days = {
    1 : "uno",
    2 : "duo",
    3 : "tertio",
    4 : "quarto",
    5 : "quinquo",
    6 : "senio",
    7 : "septimo",
    8 : "octo",
    9 : "nono",
    10 : "decimo"
}

#month, day
date = [1, 24]
output = ''

if months[date[0] - 1] in Nonde_Ignore_dates:
    for a in range(len(monthDates)):
        if date[1] == monthDates[a][0] and  monthDates[a][1] != 'Nonde':
            output = monthDates[a][1]

elif months[date[0] - 1] not in Nonde_Ignore_dates:
    for a in range(len(monthDates)):
        if date[1] == monthDates[a][0]:
            output = monthDates[a][1]

if output == '':
    if date[1] < 5 and months[date[0] - 1] not in Nonde_Ignore_dates:
        important_date = 'Nonde'
        time_difference = 5 - date[1]
    elif date[1] < 13:
        important_date = 'Idas'
        time_difference = 13 - date[1]
    elif date[1] > 13:
        important_date = 'Kalendae'
        time_difference = mongthLength[months.index(months[date[0] - 1])] - date[1]
    
    if time_difference <= 10:
        if important_date == 'Kalendae':
            time_difference += 1
            date[0] += 1
        output = f'{days[time_difference + 1]} die ante {important_date} {months[date[0] - 1]}'
    elif time_difference >= 11:
        output = f'{days[time_difference - 8]} {days[10]} die ante {important_date} {months[date[0]]}'

print(output)