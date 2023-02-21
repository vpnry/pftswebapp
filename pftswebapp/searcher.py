import sqlite3
import os


def format_result(tup):
    if not tup:
        return 'Not found'
    li = [pat + '\n' + cont for pat, cont in tup]
    return '\n<br>'.join(li)


def search_this(keyword, db_path, search_mode='distance',
                distance_value=10, extract_len=64, hit_limit=100, order_by='rank'):
    if not os.path.isfile(db_path):
        return [(f'The selected {db_path} is not found!', '')]
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    if not distance_value:
        distance_value = 10
    if not hit_limit:
        hit_limit = 100
    if not extract_len:
        extract_len = 64

    u1 = '<u>'
    u2 = '</u>'

    esc_keyword = keyword.replace('"', '""')
    if order_by == 'bm25':
        order_by = 'bm25(pn)'

    # distance: (default) word distance search
    query_me = query_distance = f'''
        SELECT path, snippet(pn, 1, '{u1}', '{u2}', ' ~~ ',{extract_len})
        cont FROM pn
        WHERE cont MATCH 'NEAR("{esc_keyword}", {distance_value})'
        ORDER BY {order_by} LIMIT {hit_limit}
    '''

    # exact: exact phrase search
    qry_exact = f'''
        SELECT path, snippet(pn, 1, '{u1}', '{u2}', ' ~~ ',{extract_len})
        cont FROM pn
        WHERE cont MATCH '"{esc_keyword}"'
        ORDER BY {order_by} LIMIT {hit_limit}
    '''

    # prefix: word prefix search
    qry_prefix = f'''
        SELECT path, snippet(pn, 1, '{u1}', '{u2}', ' ~~ ',{extract_len})
        cont FROM pn
        WHERE cont MATCH '"{esc_keyword}" * '
        ORDER BY {order_by} LIMIT {hit_limit}
    '''

    if search_mode == 'exact':
        query_me = qry_exact
    elif search_mode == 'prefix':
        query_me = qry_prefix

    # print(query_me)

    cur.execute(query_me)
    result = cur.fetchall()
    conn.close()
    if result:
        return result
    else:
        return []
