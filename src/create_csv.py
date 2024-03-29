
months={
    'Mar':'03',
    'Apr':'04',
    'May':'05'
}
def format_day(day):
    r = day if len(day)==2 else '0'+str(day)
    return r
x = '1 Mar, 2 Mar, 3 Mar, 4 Mar, 5 Mar, 6 Mar, 7 Mar, 8 Mar, 9 Mar, 10 Mar, 11 Mar, 12 Mar, 13 Mar, 14 Mar, 15 Mar, 16 Mar, 17 Mar, 18 Mar, 19 Mar, 20 Mar, 21 Mar, 22 Mar, 23 Mar, 24 Mar, 25 Mar, 26 Mar, 27 Mar, 28 Mar, 29 Mar, 30 Mar, 31 Mar, 1 Apr, 2 Apr, 3 Apr, 4 Apr, 5 Apr, 6 Apr, 7 Apr, 8 Apr, 9 Apr, 10 Apr, 11 Apr, 12 Apr, 13 Apr, 14 Apr, 15 Apr, 16 Apr, 17 Apr, 18 Apr, 19 Apr, 20 Apr, 21 Apr, 22 Apr, 23 Apr, 24 Apr'
date = [format_day(i.split(' ')[0])+'-'+months[i.split(' ')[1]]+'-20' for i in x.split(', ')]
y = '0, 2, 4, 6, 9, 13, 21, 30, 39, 41, 59, 78, 112, 169, 245, 331, 448, 642, 785, 1020, 1280, 1600, 2060, 2362, 2995, 3544, 4268, 5170, 5962, 6408, 7443, 8251, 9034, 9886, 10524, 11278, 11730, 12442, 13141, 13956, 15472, 15987, 16585, 16934, 17448, 18091, 18841, 19022, 19685, 20206, 20863, 21379, 21982, 22353, 22797'
cases_cul = y.split(', ')

y2='0, 2, 2, 2, 3, 4, 8, 9, 9, 2, 18, 19, 34, 57, 76, 86, 117, 194, 143, 235, 260, 320, 460, 302, 633, 549, 724, 902, 792, 446, 1035, 808, 783, 852, 638, 754, 452, 712, 699, 815, 1516, 515, 598, 349, 514, 643, 750, 181, 663, 521, 657, 516, 603, 371, 444'
cases_daily = y2.split(', ')

y3='0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 3, 6, 12, 14, 23, 33, 43, 60, 76, 100, 119, 140, 160, 187, 209, 246, 266, 295, 311, 345, 380, 409, 435, 470, 504, 535, 567, 599, 629, 657, 687, 714, 735, 762, 785, 820, 854'
deaths_cul = y3.split(', ')

y4 = '0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 3, 3, 3, 3, 5, 5, 5, 14, 22, 22, 43, 43, 43, 43, 43, 43, 43, 68, 68, 75, 75, 140, 184, 196, 205, 233, 266, 277, 277, 347, 383, 493, 519, 610, 610, 610, 917, 1143, 1201, 1228'
recoveries = y4.split(', ')

y5 = '0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 9, 18, 17, 20, 30, 26, 35, 41, 47, 48, 61, 61, 71, 89, 136, 164, 188, 230, 240, 245, 251, 267, 270, 271, 245, 241, 226, 233, 228, 188, 218, 208, 229, 222, 228, 224, 215, 213, 207, 204, 188'
uci = y5.split(', ')

y6='0, 0, 0, 0, 9, 13, 21, 30, 38, 40, 57, 107, 107, 114, 139, 139, 206, 89, 89, 126, 156, 169, 201, 203, 276, 191, 354, 418, 486, 571, 627, 726, 1042, 1058, 1075, 1084, 1099, 1180, 1211, 1173, 1179, 1175, 1177, 1187, 1227, 1200, 1302, 1284, 1253, 1243, 1208, 1172, 1146, 1095, 1068'
stable = y6.split(', ')

y7 = '0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2, 2, 6, 2, 9, 10, 10, 17, 16, 24, 19, 21, 20, 27, 22, 37, 20, 29, 16, 34, 35, 29, 26, 35, 34, 31, 32, 32, 30, 28, 30, 27, 21, 27, 23, 35, 34'
deaths_daily = y7.split(', ')

y8 = '0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, -1, 9, -1, 3, 10, 6, 9, 6, 6, 1, 27, 0, 10, 18, 47, 28, 24, 42, 10, 5, 6, 16, 3, 1, -26, -4, -15, 7, -5, -40, 30, -10, 21, -7, 6, -4, -9, -2, -6, -3, -16, -2'
icu_variation = y8.split(', ')
print(deaths_daily)
print(len(cases_cul), len(date), len(cases_daily), len(deaths_cul), len(recoveries), len(uci), len(stable), len(deaths_daily))

with open('portugal_data.csv', 'w') as f:
    f.write('date,total_cases,daily_cases,total_deaths,daily_deaths,recovered,hospital_stable,hospital_icu,icu_variation\n')
    for i in range(len(date)):
        f.write(date[i]+','+cases_cul[i]+','+cases_daily[i]+','+deaths_cul[i]+','+deaths_daily[i]+','+recoveries[i]+','+stable[i]+','+uci[i]+','+icu_variation[i]+'\n')
