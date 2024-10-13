import csv
import glob


if line['country'] == 'USA':
                line['country'] = 'United States'
            university_entry = (
                int(line['publications']),
                int(line['influence']),
                int(line['patents'])
            )

            
def extract_year_from_filename(filename):
    index = filename.find('_')
    year = filename[index - 4:index]
    return year

def read_university_primary_data(filename):
    university_data = {}
    with open(filename, 'r', encoding='utf-8') as file_in:
        reader = csv.DictReader(file_in)
        for line in reader:
            
            adjust_usa_name(line)

            university_entry = get_university_entry(line)
            
            if line['country'] not in university_data:
                university_data[line['country']] = {}
                
            if line['institution'] not in university_data[line['country']]:
                university_data[line['country']][line['institution']] = {}

            year = line['year']
            university_data[line['country']][line['institution']][year] = [university_entry]
            
    return university_data

def read_rankings_secondary_data(all_filenames, university_data):
    rankings_data = {}
    
    for filename in all_filenames:
        current_year = extract_year_from_filename(filename)
        with open(filename, 'r', encoding='utf-8') as file_in:
            file_in.readline()  
            reader = csv.reader(file_in)
            
            for line in reader:
                country = line[15]
                if country == 'Russian Federation':
                    country = 'Russia'
                research_rank = int(line[12])
                citations_rank = int(line[14])
                university_name = line[2]

                if country in data_dict:
                    if university_name in data_dict[country]:
                        if year in data_dict[country][university_name]:
                            data_dict[country][university_name].append(current_tule)

##                if country not in rankings_data:
##                    rankings_data[country] = {}
##                if university_name not in rankings_data[country]:
##                    rankings_data[country][university_name] = {}
##                data_values = {current_year: [research_rank, citations_rank]}
##                rankings_data[country][university_name][current_year] = [(research_rank, citations_rank)]
    return rankings_data

def merge_university_and_rankings_data(university_data, rankings_data):
    years = ['2012', '2013', '2014', '2015']
    
    for year in years:
        for country in university_data:
            if country not in rankings_data:
                continue
            for university_name in university_data[country]:
                if university_name not in rankings_data[country]:
                    continue
                if year in university_data[country][university_name]:
                    if year not in rankings_data[country][university_name]:
                        rankings_data[country][university_name][year] = [('NA', 'NA')]
                    university_data[country][university_name][year].append(rankings_data[country][university_name][year][0])
                else:
                    university_data[country][university_name][year] = [('NA', 'NA', 'NA'), ('NA', 'NA')]
    return university_data

def write_formatted_data_to_file(university_rankings_data, final_list):
    with open('formatted_data.txt', 'w', encoding='utf-8') as file_out:
        empty_str = ''
        rank_labels = 'Publications   Influence   Patents   Research Rank   Citations Rank    '
        header = f'{"Country":<20} {"University Name":<58} {"2012":>30} {"2013":>71} {"2014":>71} {"2015":>71}\n'
        header2 = f'{empty_str:^78} {rank_labels:^50} {rank_labels:^50} {rank_labels:^50} {rank_labels:^50}\n\n'
        file_out.write(header)
        file_out.write('-' * 364 + '\n')
        file_out.write(header2)
        for country, universities in university_rankings_data.items():
            if country not in final_list:
                continue
            for university_name, stats in universities.items():
                if university_name not in final_list[country]:
                    continue
                stats_sorted = dict(sorted(stats.items()))
               
                file_out.write(f'{country:<20}{university_name:<60}')
                for year_data in stats_sorted:
                    sline = f'{stats_sorted[year_data][0][0]:>6}{stats_sorted[year_data][0][1]:>13}' \
                            f'{stats_sorted[year_data][0][2]:>11}{stats_sorted[year_data][1][0]:>12}' \
                            f'{stats_sorted[year_data][1][1]:>17}             '
                    file_out.write(f'{sline:^22}')
                file_out.write('\n')

def main():
    university_data = read_university_primary_data('world-university-rankings.csv')
    filenames = glob.glob('*_rankings.csv')
    rankings_data = read_rankings_secondary_data(filenames, university_data)
    university_rankings_data = merge_university_and_rankings_data(university_data, rankings_data)
    write_formatted_data_to_file(university_rankings_data, rankings_data)


main()
