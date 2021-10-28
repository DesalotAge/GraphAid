import requests
import threading

HOST = 'https://www.tks.ru/'


def get_rw_urls() -> list[str]:

    not_used_pages = set(range(1, 86))
    ans = []

    def request_for_page(page: int) -> requests.Request:
        return requests.get(
            HOST +
            f'db/rwstation?mode=search&second=x&page={page}&kodstan=&naimstan=&koddor=&kodotd=&kodtam=&namt=&freight='
        )

    def load_by_page(page: int) -> list[str]:
        nonlocal ans
        url_list = []

        retrieve = 30

        res = request_for_page(page)

        while retrieve > 0 and res.status_code != 200:
            res = request_for_page(page)
            retrieve -= 1

        html_doc = res.text

        for after_correct_url_beginning in html_doc.split('/db/rwstation/'):
            cur_id = ''
            for i in after_correct_url_beginning:
                if i.isnumeric():
                    cur_id += i
                else:
                    break

            if cur_id:
                url_list.append('/db/rwstation/' + cur_id)
        ans += list(set(url_list))
        not_used_pages.remove(page)
        return url_list

    for page in range(1, 86):
        t = threading.Thread(target=load_by_page, args=(page, ))
        t.start()

    # waiting all threads to end
    while len(not_used_pages):
        pass

    return ans
