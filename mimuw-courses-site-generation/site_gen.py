import scraper


def get_site_link(code):
    return "https://informatorects.uw.edu.pl/pl/courses/view?prz_kod=" + code

site = open('../index.md', 'w')

site.write('---\n')
site.write('layout: home\n')
site.write('---\n')

site.write('![image](elitarny_mimuw.png "Elitarny MIMUW")\n\n')
site.write('Strona zawiera listę przedmiotów obowiązkowych na kierunku informatyka na MIMUW. ')
site.write('Lista przedmiotów, informacje o przedmiotach oraz listy polecanych książek ')
site.write('są generowane automatycznie na podstawie wyników wyszukiwania w DuckDuckGo.\n\n')

site.write('# Lista przedmiotów\n')

courses = scraper.get_courses_data()

for course in courses:
    site.write('## [' + course['course_name'] + '](/mimuw-courses-site/' + course['course_code'] + '/) \n')
    site.write('- Liczba godzin: \n')
    site.write('\t - Wykłady: ' + course['lecture_hours'] + '\n')
    site.write('\t - Ćwiczenia: ' + course['practical_hours'] + '\n')
    site.write('\t - Labolatoria: ' + course['lab_hours'] + '\n')
    site.write('- ECTS: ' + course['ects'] + '\n')
    site.write('- Forma zaliczenia: ' + course['form_of_credit'] + '\n')
    site.write('\n')

    # Generate course-specific page
    sub_site = open('../' + course['course_code'] + '.md', 'w')
    sub_site.write('---\n')
    sub_site.write('layout: default\n')
    sub_site.write('permalink: /mimuw-courses-site/' + course['course_code'] + '/\n')
    sub_site.write('---\n')
    sub_site.write('Więcej informacji na temat przedmiotu: [strona kursu](' + get_site_link(course['course_code']) + ') \n\n')

    books = scraper.get_books(course['course_name'])

    sub_site.write('### Polecane książki:\n')
    for book in books:
        sub_site.write('- [' + book['title'] + '](' + book['href'] + ')\n')

    sub_site.close()

site.close()
