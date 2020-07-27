grades = [100, 100, 90, 40, 80, 100, 85, 70, 90, 65, 90, 85, 50.5]

def grades_sum(scores):
    sum_of_grades = 0
    for score in scores:
        sum_of_grades += score
        
    print 'sum of grades: %s' % sum_of_grades
    return sum_of_grades

def grades_average(grades):
    grades_total = grades_sum(grades)
    grade_average = grades_total / float(len(grades))

    print 'grade average: %s' % grade_average
    return grade_average

grades_average(grades)