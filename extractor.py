# coding=utf-8
import traceback
import re
import csv


# header patterns

pattern_header = ur'(.*?)((ДТП\s*с\s*погибшими)|(ДТП\s*с\s*ранеными)|(ДТП\s*с\s*детьми)|(\d{2}\.\d{2}\.\d{4}))'
pattern_header_dtp = ur'([Вв]\s*?[Нн]ижегородской\s*?области[^,\.]*?)?(\d+)\s*ДТП'
pattern_header_death = ur'([Вв]\s*?[Нн]ижегородской\s*?области[^\.]*?)?(?:(\d+)(?:\s*человека?)?\s*(?:погиб(?:л[ио])?))'
pattern_header_hurt = ur'([Вв]\s*?[Нн]ижегородской\s*?области[^\.]*?)?(?:(\d+)\s*(?:человека?)?\s*(?:получили? ранени[яе]))'
pattern_header_material_damage = ur'с материальным ущербом:\s*В.*?области.*?(\d+).*?в т\.ч\. в.*?Новгороде.*?(\d+)'
pattern_header_violation = ur'выявлено\s*(\d+)\s*нарушений'
pattern_header_drunk = ur'(\d+)[а-яА-Я\s-]*опьянения'
pattern_header_speeding = ur'(\d+)[а-яА-Я\s-]*скоростного'
pattern_header_again_drunk = ur'(\d+)[а-яА-Я\s,-]*повторно[а-яА-Я\s,-]*опьянен'




pattern_accident_body = ur'((?:\d+\s+(?:погибши[хй]|ранены[хй])\s*,*\s*)+.*?В результате ДТП.*?$)' \
                        ur'((?:(?:\s*-\s*(?:(?:не установленн[ыа][йя]\s*?)*?' \
                        ur'(?:[жм]\s*\.*)|(?:мальчик)|(?:девочка)|(?:женщина)|(?:мужчина)|(?:юноша)|(?:девушка)).*?$)|(?:\s*?(?:[Вв]одитель|[Пп]ассажир).*?$))+)'

pattern_victim_city = ur'(?:(?:(\d+)\s+погибши[хй]\s*,*\s*)|(?:(\d+)\s*ранен{1,2}ы[хй]\s*,*\s*))+' \
                      ur'(?:((?:г\.|с\.|(?:р\.п\.)|(?:п\.)|(?:г\.о\.)|село|деревня)\s*[А-Я][ёа-я]*(?:[\.\s-]+[А-Я][ёа-я-]*)*)|' \
                      ur'([А-Я][ёа-я]*(?:[\s\.-]+[А-Я][ёа-я-]*)*\s*(?:(?:район)|(?:р-о?н))))\s*(.*?$)'

pattern_date_driver = ur'\s*?((?:\d{2}\.)?\d{2}.\d{2,4}).*?в\s*?(\d{1,2}:\d{2})\s+?(?:на)?(.*?)(?:(?:неустановленный\s)*?водитель|(женщина-водитель)|(?:в результате)|(?:\())'
patter_birth_experience = ur'\((.*?)?(\d{4}).*?(?:(?:\))|(?:стаж(.*?))(?=[,\)]))(.*?$)'


pattern_car = ur'(?:управляя\s*(.*?)(?:(?:,)|(?:в результате)|(?:соверш)))(.*?$)'

pattern_victims = ur'(?:-\s*((?:[ЖМжм])|(?:мальчик)|(?:девочка)|(?:женщина)|(?:мужчина)|(?:юноша)|(?:девушка))\s*\.?).*?(\d{4}).*?(?:[Дд]/[зЗ]|Диагноз):(.*?)\..*?$'


def parse_header(text):
    match = re.search(pattern_header, text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if match is not None:
        return match.group(1)
    else:
        return None

def parse_one_match(pattern, text):
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if match is not None:
        if match.group(1) is not None:
            return match.group(1)
        else:
            return '0'
    else:
        return 'None'

def parse_simple_double_match(pattern, text):
    var_1 = 'None'
    var_2 = 'None'
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if match is not None:
        if match.group(1) is not None:
            var_1 = match.group(1)
        if match.group(2) is not None:
            var_2 = match.group(2)
    return var_1, var_2

def parse_double_match(pattern, text):
    var_1 = '0'
    var_2 = '0'
    for match in re.finditer(pattern, text, re.MULTILINE | re.DOTALL | re.IGNORECASE):
        if match is not None:
            if match.group(1) is not None and match.group(2) is not None:
                var_1 = match.group(2)
            elif match.group(1) is None and match.group(2) is not None:
                var_2 = match.group(2)

    return var_1, var_2

accident_counter = 0

with open('data/raw_data.csv', 'rb') as raw_data, open('data/overall_info', 'wb') as overall_info, open('data/accidents_data', 'wb') as accidents_data, open('data/victims_data', 'wb') as victims_data:

    raw_data_reader = csv.reader(raw_data, delimiter=";")

    ov_inf_writer = csv.writer(overall_info, delimiter=';')
    acc_data_writer = csv.writer(accidents_data, delimiter=';')
    vict_data_write = csv.writer(victims_data, delimiter=';')

    ov_inf_writer.writerow(['link',
                            'date',
                            'num_dtp_region',
                            'num_dtp_city',
                            'num_death_region',
                            'num_death_city',
                            'num_hurt_region',
                            'num_hurt_city',
                            'num_material_damage_region',
                            'num_material_damage_city',
                            'num_violation_pdd',
                            'num_drunk',
                            'num_speeding',
                            'num_again_drunk'])

    acc_data_writer.writerow(['accident_id',
                              'date',
                              'time',
                              'place',
                              'address'
                              'num_death',
                              'num_hurt',
                              'accident',
                              'drivers_vehicle',
                              'drivers_birth_year',
                              'drivers_experience',
                              'accident_details'])

    vict_data_write.writerow(['accident_id',
                              'gender',
                              'birth_year',
                              'injury'])


    for id, raw_data_row in enumerate(raw_data_reader):

        num_dtp_region = 'None'
        num_dtp_city = 'None'
        num_death_region = 'None'
        num_death_city = 'None'
        num_hurt_region = 'None'
        num_hurt_city = 'None'
        num_material_damage_region = 'None'
        num_material_damage_city = 'None'
        num_violation_pdd = 'None'
        num_drunk = 'None'
        num_speeding = 'None'
        num_again_drunk = 'None'
        common_date = 'None'

        link = raw_data_row[0]
        day_summary = raw_data_row[1].decode('utf-8')

        match = parse_header(day_summary)
        if match is not None:

            header = match

            num_dtp_region, num_dtp_city = parse_double_match(pattern_header_dtp, header)

            # as same as 'if header is blank'
            if num_dtp_region != '0' and num_dtp_city != '0':

                num_dtp_region, num_dtp_city = parse_double_match(pattern_header_dtp, header)
                num_death_region, num_death_city = parse_double_match(pattern_header_death, header)
                num_hurt_region, num_hurt_city = parse_double_match(pattern_header_hurt, header)

                num_material_damage_region, num_material_damage_city = parse_simple_double_match(pattern_header_material_damage, header)

                num_violation_pdd = parse_one_match(pattern_header_violation, header)
                num_drunk = parse_one_match(pattern_header_drunk, header)
                num_speeding = parse_one_match(pattern_header_speeding, header)
                num_again_drunk = parse_one_match(pattern_header_again_drunk, header)

            else:
                num_dtp_region = 'None'
                num_dtp_city = 'None'

        for match_all in re.finditer(pattern_accident_body, day_summary, re.MULTILINE | re.DOTALL | re.IGNORECASE):

            num_death = '0'
            num_hurt = '0'
            place = 'None'
            accident = 'None'
            date = 'None'
            time = 'None'
            specific_place = 'None'

            drivers_birth_year = 'None'
            experience = 'None'
            details = 'None'
            car = 'None'

            if match_all.group(1) is not None:
                accident_summary = match_all.group(1)

                try:
                    match = re.search(pattern_victim_city, accident_summary, re.MULTILINE | re.DOTALL)

                    if match is not None:

                        num_death = match.group(1) or '0'
                        num_hurt = match.group(2) or '0'
                        place = match.group(3) or (match.group(4) or 'None')
                        accident = match.group(5) or 'None'

                    match = re.search(pattern_date_driver, accident_summary, re.MULTILINE | re.DOTALL)

                    if match is not None:

                        if match.group(1) is not None and match.group(2) is not None:
                            date = match.group(1)
                            time = match.group(2)

                        specific_place = match.group(3) or 'None'
                        specific_place = specific_place.rstrip().lstrip()
                        if len(specific_place) > 0 and specific_place[-1] == ',':
                            specific_place = specific_place[:-1]

                    match = re.search(patter_birth_experience, accident_summary, re.MULTILINE | re.DOTALL)

                    if match is not None:

                        drivers_birth_year = match.group(1) or 'None'
                        experience = match.group(2) or 'None'

                        right_part = match.group(3)

                        if right_part is not None:
                            match = re.search(pattern_car, accident_summary, re.MULTILINE | re.DOTALL)

                            if match is not None:

                                car = match.group(1) or 'None'
                                details = match.group(2) or 'None'

                    acc_data_writer.writerow([str(accident_counter),
                                              date.encode('utf-8'),
                                              time.encode('utf-8'),
                                              place.encode('utf-8'),
                                              specific_place.encode('utf-8'),
                                              num_death.encode('utf-8'),
                                              num_hurt.encode('utf-8'),
                                              accident.encode('utf-8'),
                                              car.encode('utf-8'),
                                              drivers_birth_year.encode('utf-8'),
                                              experience.encode('utf-8'),
                                              details.encode('utf-8')])

                    if common_date == 'None' and date != 'None':
                        common_date = date

                    victims = match_all.group(2)

                    # print victims

                    for victim_row in victims.split('\n'):

                        m = re.search(pattern_victims, victim_row, re.MULTILINE | re.DOTALL)

                        date_birth = 'None'
                        injury = 'None'
                        gender = 'None'

                        if m is not None:

                            gender = m.group(1) or 'None'
                            date_birth = m.group(2) or 'None'
                            injury = m.group(3) or 'None'

                            if gender in {u'м.', u'м', u'мальчик', u'юноша', u'мужчина'}:
                                gender = u'м'
                            elif gender in {u'женщина', u'девушка', u'ж.', u'ж', u'девочка'}:
                                gender = u'ж'

                            vict_data_write.writerow([str(accident_counter), gender.encode('utf-8'), date_birth.encode('utf-8'), injury.encode('utf-8')])

                            # print gender, date_birth, injury

                except AttributeError as e:
                    # for debug
                    # print match_all.group(0)
                    traceback.print_exc(e)

                accident_counter = accident_counter + 1
                # print accident_counter


        ov_inf_writer.writerow([link,
                                common_date.encode('utf-8'),
                                num_dtp_region.encode('utf-8'),
                                num_dtp_city.encode('utf-8'),
                                num_death_region.encode('utf-8'),
                                num_death_city.encode('utf-8'),
                                num_hurt_region.encode('utf-8'),
                                num_hurt_city.encode('utf-8'),
                                num_material_damage_region.encode('utf-8'),
                                num_material_damage_city.encode('utf-8'),
                                num_violation_pdd.encode('utf-8'),
                                num_drunk.encode('utf-8'),
                                num_speeding.encode('utf-8'),
                                num_again_drunk.encode('utf-8')])