from src.ranking import score

queries = [
    'harry potter, dirty',
    'brad pitt, guns',
    'magic, fantasy, portal',
    'love fantasy',
    'kidnapping child'
]

time_availables = [100, 150, 200, 250, 300, 400, 450, 500, 550, 600, 650, 700] # in minutes

def display_result(time_label, time_diff):
    print(f'Average Time Difference for {time_label}')
    print(f'Time Diff: {time_diff}')
    print('-'*20)
    print()

def get_total_time(movies):
    total_time = 0
    for movie in movies:
        total_time += int(movie['movie_runtime'])
    return total_time

def get_time_diff_result(time_available):
    diffs = []
    for query in queries:
        movie_results = score(query, time_available)
        total_time = get_total_time(movie_results)
        diffs.append(time_available-total_time)

    return sum(diffs)/len(diffs)

def main():
    results = []
    # for each time available, get diff
    for time in time_availables:
        time_diff = get_time_diff_result(time)
        results.append(time_diff)
        display_result(f'{time} minutes', time_diff)

    # Keep average time diff for each time available
    average_diff = sum(results)/len(results)
    display_result('All Time Available', average_diff)

if __name__ == '__main__':
    main()