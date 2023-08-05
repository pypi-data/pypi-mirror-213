#!python3
from threading import Thread
from eyes_soatra import eyes
from eyes_soatra.constant.depends.app_date.start import depends as __starts
from eyes_soatra.constant.depends.app_date.end import depends as __ends
from eyes_soatra.constant.depends.app_date.period import depends as __periods
import pandas
import json
import argparse

read_from = 'test/data/active.csv'
records = pandas.read_csv(read_from).values
founds = []

def save_file(write_to):
    f = open(f'{write_to}test.json', "w")
        
    try:
        json_data = json.dumps(
            founds,
            ensure_ascii=False,
            indent=4
        )
    except:
        json_data = None
        
    f.write(json_data if json_data else str(founds))
    f.close()
    
    print(f'\n--- done ---\n')
    print('length = ', len(founds))
    print('\n-------------\n')

def worker(start, end):
    for i in range(start, end):
        url = records[i][2]
        
        try:
            res = eyes.time_app(
                url=url,
                show_detail=True
            )
            
            if (
                'app-start' in res or
                'app-end' in res or
                'app-period' in res
            ):
                founds.append(res)
                print(f'\n{i + 1}. +++ founded {url}\n')
            
            else:
                print(f'{i + 1}. --- no-found {url}')

        except Exception as ex:
            pass
        
def main(start_point, length, rows):
    length = (len(records) - start_point) if (start_point + length) > len(records) else length
    token = int(length / rows)
    write_to = f'test/checks/'
    threads = []
    
    for i in range(0, rows):
        start = start_point + (i * token)
        
        if i == rows - 1:
            end = length
            thread = Thread(
                target=worker,
                kwargs={'start': start, 'end': end}
            )
            threads.append(thread)
            
            for thread in threads:
                thread.start()
            
            for thread in threads:
                thread.join()
                
            save_file(write_to)

        else:
            end = start + token
            thread = Thread(
                target=worker,
                kwargs={'start': start, 'end': end}
            )
            threads.append(thread)
        
if __name__ == '__main__':
    defaults = {
        'start': 0,
        'length': 'all',
        'row': 200
    }
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", help="start point", default=defaults['start'])
    parser.add_argument("-l", "--length", help="length", default=defaults['length'])
    parser.add_argument("-r", "--row", help="row", default=defaults['row'])
    args = parser.parse_args()
    
    start_point = int(args.start)
    length = len(records) if args.length == 'all' else int(args.length)
    rows = int(args.row)

    main(start_point, length, rows)