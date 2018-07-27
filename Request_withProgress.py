class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0,    unit='', sep='/', chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        _info = self.info % (self.title, self.status, self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status

        print(self.__get_info(), end=end_str, )


if __name__ == '__main__':

    import requests
    from contextlib import closing

    ip = "10.10.10.140"

    url1="http://"+ip+"/api/setData?path=systemManager%3AcreateLogFile&roles=activate&value=%7B%22saveLogType%22%3A%22beoWeb%22%7D&"
    url2="http://"+ip+"/api/stream//tmp/temp_data_logs.tgz?"

    url ="https://github.com/kennethreitz/requests/tarball/master"

    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])

        print('content_size', content_size,response.status_code ,  )
        progress = ProgressBar("razorback"
                    , total=content_size
                    , unit="KB"
                    , chunk_size=chunk_size
                    , run_status="Downloading"
                    , fin_status="Complete download")
            # chunk_size = chunk_size < content_size and chunk_size or content_size
        with open('./file.zip', "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))

        print('Complete download', )