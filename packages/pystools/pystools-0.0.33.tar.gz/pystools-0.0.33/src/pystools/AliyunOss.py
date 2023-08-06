# -*- coding: utf-8 -*-
import oss2
import urllib3

HTTP_POOL = urllib3.PoolManager(num_pools=1000)
import urllib.parse


class AliyunOSS(object):
    def __init__(self, accesskey_id, accesskey_secret, endpoint, bucket, domian, **kwargs):


        self.__dict__.update(locals())

        self.key_id = accesskey_id
        self.key_secret = accesskey_secret
        self.endpoint = endpoint
        self.bucket_name = bucket
        self.domian = domian

        auth = oss2.Auth(self.key_id, self.key_secret)
        self.bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)

    def upload_data(self, data, oss_key,
                    headers=None,
                    progress_callback=None):

        """
        上传一个普通文件。
        用法 ::
            >>> bucket.put_object('readme.txt', 'content of readme.txt')
            >>> with open(u'local_file.txt', 'rb') as f:
            >>>     AliyunOSS.upload_data('remote_file.txt', f)
        :param key: 上传到OSS的文件名

        :param data: 待上传的内容。
        :type data: bytes，str或file-like object

        :param headers: 用户指定的HTTP头部。可以指定Content-Type、Content-MD5、x-oss-meta-开头的头部等
        :type headers: 可以是dict，建议是oss2.CaseInsensitiveDict

        :param progress_callback: 用户指定的进度回调函数。可以用来实现进度条等功能。参考 :ref:`progress_callback` 。

        :return: :class:`PutObjectResult <oss2.models.PutObjectResult>`
        """

        self.bucket.put_object(oss_key, data, headers, progress_callback)
        path = self.domian + "/" + urllib.parse.quote(oss_key)
        return path

    def upload_from_local_file(
            self, local_file_path, oss_key,
            headers=None,
            progress_callback=None
    ) -> str:
        '''
        将文件上传到oss上
        :param local_file_path: 要上传的文件
        :param oss_key: oss上的路径, 要存在oss上的那个文件
        :return:
        '''

        # 上传
        res = self.bucket.put_object_from_file(oss_key, local_file_path, headers, progress_callback)
        path = self.domian + "/" + urllib.parse.quote(oss_key)
        return path

    def upload_from_url(self, url, oss_key, headers=None, progress_callback=None) -> str:

        resp = HTTP_POOL.request(method="GET", url=url)
        if resp.status != 200:
            raise Exception("request url error: %s" % url)

        resp_data = resp.data
        resp_header = resp.info()
        content_type = resp_header.get('Content-Type')
        # Content_Disposition = resp_header.get('Content-Disposition')
        if not headers:
            headers = {'Content-Type': content_type}
        return self.upload_data(resp_data, oss_key, headers=headers, progress_callback=progress_callback)

    # 判断文件在不在
    def oss_file_exist(self, oss_key) -> dict:
        return self.bucket.object_exists(oss_key)

    def upload_feishu_file(self, feishu, feishu_file_item, oss_key_or_folder, headers=None,
                           progress_callback=None) -> str:
        '''
        上传飞书文件
        :param oss_key_or_folder: 如果是以/结尾的, 则是文件夹, 否则是文件
        :param feishu_file_item:
            {
                "file_token": "Vl3FbVkvnowlgpxpqsAbBrtFcrd",
                "name": "飞书.jpeg",
                "size": 32975,
                "tmp_url": "https://open.feishu.cn/open-apis/drive/v1/medias/batch_get_tmp_download_url?file_tokens=Vl3FbVk11owlgpxpqsAbBrtFcrd&extra=%7B%22bitablePerm%22%3A%7B%22tableId%22%3A%22tblBJyX6jZteblYv%22%2C%22rev%22%3A90%7D%7D",
                "type": "image/jpeg",
                "url": "https://open.feishu.cn/open-apis/drive/v1/medias/Vl3FbVk11owlgpxpqsAbBrtFcrd/download?extra=%7B%22bitablePerm%22%3A%7B%22tableId%22%3A%22tblBJyX6jZteblYv%22%2C%22rev%22%3A90%7D%7D"
			}
        :param headers:
        :param progress_callback:
        :return:
        '''

        oss_key = oss_key_or_folder
        if oss_key.endswith("/"):
            oss_key = oss_key_or_folder + feishu_file_item['name']
        if not headers:
            headers = {'Content-Type': feishu_file_item['type']}

        file_token = feishu_file_item.get('file_token')
        download_url = feishu.medias_batch_get_tmp_download_url(file_tokens=file_token)
        tmp_download_url = download_url.get("tmp_download_urls")[0].get('tmp_download_url')
        return self.upload_from_url(tmp_download_url, oss_key, headers=headers, progress_callback=progress_callback)

    def download_content_bytes(self, key):
        # 下载文件
        result = self.bucket.get_object(key)
        content_got = b''
        for chunk in result:
            content_got += chunk
        return content_got

    def download_to_local(self, key, local_path):
        res = self.bucket.get_object_to_file(key, local_path)
        return res

    def download_stream(self, key):
        object_stream = self.bucket.get_object(key)
        return object_stream
        # print(object_stream.read())
        # # 由于get_object接口返回的是一个stream流，需要执行read()后才能计算出返回Object数据的CRC checksum，因此需要在调用该接口后进行CRC校验。
        # if object_stream.client_crc != object_stream.server_crc:
        #     print("The CRC checksum between client and server is inconsistent!")
