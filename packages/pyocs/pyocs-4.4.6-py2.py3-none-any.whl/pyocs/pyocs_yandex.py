#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
import pathlib
import os
import requests
import functools
import tqdm
import logging
import time
import socket
import paramiko
import zipfile
from bs4 import BeautifulSoup
from paramiko.py3compat import u
from pprint import pformat
from pyocs import pyocs_software
from pyocs.pyocs_demand import PyocsDemand
from pyocs.pyocs_cplm import PyocsCplm

class Yadiredo:
    API_ENDPOINT = 'https://cloud-api.yandex.net/v1/disk/public/resources/?public_key={}&path=/{}&offset={}'
    _logger = logging.getLogger(__name__)
    newlink = None
    url = None
    download_root_dir = os.environ['HOME'] + '/yandex_software/'
    yadiredo_hostname = '10.22.1.49'
    yadiredo_port = 22

    def __init__(self, url):
        self._logger.setLevel(level=logging.INFO)  # 控制打印级别
        self.is_nextcloud = self.is_nextclould_link(url)
        self.original_url = url
        self.url = self.get_nextcloud_zip_link(url)
        self.newlink = self.is_yandex_newlink(self.url)
        self.cplm = PyocsCplm()

    def download_file(self, target_path, url):
        # self._logger.info(url)
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url, stream=True, allow_redirects=True, verify=False)
        if r.status_code != 200:
            r.raise_for_status()  # Will only raise for 4xx codes, so...
            raise RuntimeError("请求网站时出现错误!")
        file_size = int(r.headers.get('Content-Length', 0))

        path = pathlib.Path(target_path).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        desc = "(Unknown total file size)" if file_size == 0 else ""
        r.raw.read = functools.partial(r.raw.read, decode_content=True)  # Decompress if needed
        with tqdm.tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
            with path.open("wb") as f:
                shutil.copyfileobj(r_raw, f)


    def try_as_file(self, j, current_path):
        if 'file' in j:
            file_save_path = os.path.join(current_path, j['name'])
            self._logger.info(f' processing, file save path: ./{file_save_path}')
            self.download_file(file_save_path, j['file'])
            return True
        return False

    def remove_ndays_before_create_dir(self, day):
        for dir in os.listdir(self.download_root_dir):
            temp_path = os.path.join(self.download_root_dir, dir)
            dir_create_time = os.path.getctime(temp_path)
            current_time = time.time()
            if current_time - dir_create_time > (24*60*60) * int(day):
                shutil.rmtree(temp_path)

    def init_reset_env(self, target_path, source_path, is_init):
        current_path = os.path.join(target_path, source_path)
        if pathlib.Path(current_path).exists():
            self._logger.info("Clear download cache directory: %s" % current_path)
            shutil.rmtree(current_path)
        if is_init:
            self.remove_ndays_before_create_dir(2)
            self._logger.info("Create download cache directory: %s" % current_path)
            pathlib.Path(current_path).mkdir(parents=True, exist_ok=True)


    def list_all_files(self, target_path):
        files = []
        fdlist = os.listdir(target_path) #列出文件夹下所有的目录与文件
        for i in range(0,len(fdlist)):
            path = os.path.join(target_path,fdlist[i])
            if os.path.isdir(path):
                files.extend(self.list_all_files(path))
            if os.path.isfile(path):
                files.append(path)
        return files


    def unpack_rename_upload_sber_software(self, target_path, source_path, task_id, test_type):
        #unpack
        unpack_dir = target_path + '/unpack/'
        self._logger.info(f'*** unpack...')
        start_time = time.time()
        for it in pathlib.Path(target_path).iterdir():
            zip_file_path = pathlib.Path(target_path).joinpath(it.name)
            if zipfile.is_zipfile(zip_file_path):
                shutil._unpack_zipfile(zip_file_path, unpack_dir)
        end_time = time.time()
        self._logger.info("Unpack used time: {:.2f} S".format(end_time - start_time))

        for file_name in os.listdir(unpack_dir):
            if os.path.isfile(os.path.join(unpack_dir, file_name)):
                if file_name.startswith('EMMCBIN'):
                    zip_emmcbin_path = unpack_dir + file_name
                elif file_name.endswith('.zip') and (not file_name.startswith('EMMCBIN')):
                    zip_usb_path = unpack_dir + file_name

        #upload to cplm
        start_time = time.time()
        upload_body = self.cplm.get_cplm_upload_software_parma(task_id, zip_usb_path, test_type)
        ret1 = self.cplm.upload_software_to_cplm_soft_task_api(upload_body)
        if ret1:
            self._logger.info(f'upload sber usb upgrade package succeed to {task_id}')
        else:
            self._logger.warn(f'upload sber usb upgrade package failure to {task_id}')
        self.cplm.clean_var_www_sw_bin_files()
        end_time = time.time()
        self._logger.info("Upload usb upgrade package to CPLM used time: {:.2f} S".format(end_time - start_time))

        start_time = time.time()
        upload_body = self.cplm.get_cplm_upload_software_parma(task_id, zip_emmcbin_path, test_type)
        ret2 = self.cplm.upload_software_to_cplm_soft_task_api(upload_body)
        if ret2:
            self._logger.info(f'upload sber emmcbin package succeed to {task_id}')
        else:
            self._logger.warn(f'upload sber emmcbin package failure to {task_id}')
        self.cplm.clean_var_www_sw_bin_files()
        end_time = time.time()
        self._logger.info("Upload emmcbin package to CPLM used time: {:.2f} S".format(end_time - start_time))

        #clean
        self.init_reset_env(target_path, source_path, False)


    def unpack_rename_upload_yandex_software(self, target_path, source_path, task_id, test_type):
        #unpack
        self._logger.info(f'*** unpack...')
        start_time = time.time()
        for it in pathlib.Path(target_path).iterdir():
            zip_file_path = pathlib.Path(target_path).joinpath(it.name)
            if zipfile.is_zipfile(zip_file_path):
                shutil._unpack_zipfile(zip_file_path, target_path)
        end_time = time.time()
        self._logger.info("Unpack used time: {:.2f} S".format(end_time - start_time))

        #rename & repakage
        files = self.list_all_files(target_path)
        for fi in files:
            if '.xml' in fi:
                sw_xml_file = fi
                new_usb_sw_name = fi.split('/')[-1].replace('.xml', '')
            if 'sos.bin' in fi:
                usb_bin_file = fi
            if 'mboot.bin' in fi:
                mboot_file = fi
            if 'rom_emmc_boot.bin' in fi:
                rom_emmc_boot_file = fi
            if 'NativeEmmc.bin' in fi:
                native_emmc_file = fi

        self._logger.info(f'*** make usb upgrade zip package...')
        start_time = time.time()
        usb_sw_path = os.path.join(target_path, 'usb_sw')
        if os.path.exists(usb_sw_path):
            shutil.rmtree(usb_sw_path) # 如果路径存在，先删除，之后再重建，避免前一次的异常，影响到重新处理
        pathlib.Path(usb_sw_path).mkdir(parents=True, exist_ok=True)
        shutil.move(usb_bin_file, usb_sw_path)
        shutil.move(mboot_file, usb_sw_path)
        base_name = target_path + '/' + new_usb_sw_name
        zip_usb_path = shutil.make_archive(base_name, 'zip', root_dir=target_path, base_dir='usb_sw', logger=self._logger)
        end_time = time.time()
        self._logger.info("Make usb upgrade zip packge used time: {:.2f} S".format(end_time - start_time))

        #calculate checksum
        p = os.popen('CalChecksum ' + rom_emmc_boot_file + ' ' + native_emmc_file)
        checksum = p.read().strip()
        self._logger.info(f'EMMCBIN checksum: {checksum}')

        self._logger.info(f'*** make EMMCBIN  zip package...')
        start_time = time.time()
        emmc_bin_sw_path = os.path.join(target_path, 'emmc_bin_sw')
        if os.path.exists(emmc_bin_sw_path):
            shutil.rmtree(emmc_bin_sw_path) # 如果路径存在，先删除，之后再重建，避免前一次的异常，影响到重新处理
        pathlib.Path(emmc_bin_sw_path).mkdir(parents=True, exist_ok=True)
        shutil.move(rom_emmc_boot_file, emmc_bin_sw_path)
        shutil.move(native_emmc_file, emmc_bin_sw_path)
        base_name = target_path + '/EMMCBIN_' + checksum + '_' + new_usb_sw_name
        zip_emmcbin_path = shutil.make_archive(base_name, 'zip', root_dir=target_path, base_dir='emmc_bin_sw', logger=self._logger)
        end_time = time.time()
        self._logger.info("Make EMMCBIN zip package used time: {:.2f} S".format(end_time - start_time))

        xml_path = shutil.move(sw_xml_file, target_path)

        if task_id is None:
            task_id = self.cplm.get_task_id(xml_path)
            self._logger.info(f'task_id : {task_id}')

        #upload to cplm
        start_time = time.time()
        upload_body = self.cplm.get_cplm_upload_software_parma(task_id, zip_usb_path, test_type)
        ret1 = self.cplm.upload_software_to_cplm_soft_task_api(upload_body)
        if ret1:
            self._logger.info(f'upload yandex usb upgrade package succeed to {task_id}')
        else:
            self._logger.warn(f'upload yandex usb upgrade package failure to {task_id}')
        self.cplm.clean_var_www_sw_bin_files()
        end_time = time.time()
        self._logger.info("Upload usb upgrade package to CPLM used time: {:.2f} S".format(end_time - start_time))

        start_time = time.time()
        upload_body = self.cplm.get_cplm_upload_software_parma(task_id, zip_emmcbin_path, test_type)
        ret2 = self.cplm.upload_software_to_cplm_soft_task_api(upload_body)
        if ret2:
            self._logger.info(f'upload yandex emmcbin package succeed to {task_id}')
        else:
            self._logger.warn(f'upload yandex emmcbin package failure to {task_id}')
        self.cplm.clean_var_www_sw_bin_files()
        end_time = time.time()
        self._logger.info("Upload emmcbin package to CPLM used time: {:.2f} S".format(end_time - start_time))

        #clean
        self.init_reset_env(target_path, source_path, False)


    def download_path(self, target_path, public_key, source_path, offset=0):
        # self._logger.info('getting "{}" at offset {}'.format(source_path, offset))
        current_path = os.path.join(target_path, source_path)
        pathlib.Path(current_path).mkdir(parents=True, exist_ok=True)
        jsn = requests.get(self.API_ENDPOINT.format(public_key, source_path, offset)).json()

        # first try to treat the actual json as a single file description
        if self.try_as_file(jsn, current_path):
            return

        # otherwise treat it as a directory
        try:
            emb = jsn['_embedded']
        except KeyError:
            log.error(pformat(jsn))
            return
        items = emb['items']
        for i in items:
            # each item can be a file...
            if self.try_as_file(i, current_path):
                continue
            # ... or a directory
            else:
                subdir_path = os.path.join(source_path, i['name'])
                self.download_path(target_path, public_key, subdir_path)

        # check if current directory has more items
        last = offset + emb['limit']
        if last < emb['total']:
            self.download_path(target_path, public_key, source_path, last)

    def is_nextclould_link(self, url):
        prefix_nextcloud_link = "https://next.nklhk.com/"
        if prefix_nextcloud_link in url:
            return True
        else:
            return False

    def get_nextcloud_zip_link(self, url):
        if self.is_nextcloud:
            requests.packages.urllib3.disable_warnings()
            response = requests.get(url, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')
            download_url = soup.find('input', {'name': 'downloadURL'})['value']
            return download_url
        else:
            return url

    def is_yandex_newlink(self, url):
        prefix_oldlink = "https://disk.yandex.ru/d"
        prefix_newlink = "https://quasar.s3.yandex.net"
        if (prefix_newlink in url) or (self.is_nextcloud):
            return True
        elif prefix_oldlink in url:
            return False
        else:
            raise RuntimeError("Unknown URL:" + url)


    def download_for_newlink(self, target_path, url):
        temp = target_path.split('/')
        file_save_path = target_path + '/' + temp[-1] + '.zip'
        self._logger.info(f' processing, file save path: ./{file_save_path}')
        self.download_file(file_save_path, url)


    def get_lacal_ip_address(self):
        ip = None
        if not os.getenv('LOCAL_IP'):
            result = os.popen("cat /etc/network/interfaces | grep '^\s*address' | awk -F' ' '{print $2}'")
            ip = result.read().replace("\n","")
        else:
            ip = os.getenv('LOCAL_IP')
        return ip


    def yandex_download_upload(self, task_id, test_type):
        self.newlink = self.is_yandex_newlink(self.url)
        temp = self.url.split('/')

        temp_dir_name = None
        if self.newlink:
            temp_dir_name = temp[-1].strip('.zip')
        else :
            temp_dir_name = temp[-1]

        target_path = self.download_root_dir + temp_dir_name
        source_path = ''


        if self.get_lacal_ip_address() != self.yadiredo_hostname:
            if self.is_nextcloud:
                self.remote_ssh_server(self.original_url, task_id)
            else:
                self.remote_ssh_server(self.url, task_id)
        else:
            self.init_reset_env(target_path, source_path, True)
            if self.newlink:
                start_time = time.time()
                self.download_for_newlink(target_path, self.url)
                end_time = time.time()
                self._logger.info("Download yandex software used time: {:.2f} S".format(end_time - start_time))
            else:
                start_time = time.time()
                self.download_path(target_path, self.url, source_path)
                end_time = time.time()
                self._logger.info("Download yandex software used time: {:.2f} S".format(end_time - start_time))

        if self.is_nextcloud:
            self.unpack_rename_upload_sber_software(target_path, source_path, task_id, test_type)
        else:
            self.unpack_rename_upload_yandex_software(target_path, source_path, task_id, test_type)


    def remote_ssh_server(self, url, task_id):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        username = 'iot_common'
        pkey = paramiko.RSAKey.from_private_key_file(os.environ['HOME'] + '/.ssh/id_rsa')

        self._logger.info(f'*** Connecting... {username}@{self.yadiredo_hostname} ')
        client.connect(hostname=self.yadiredo_hostname, port=self.yadiredo_port, username=username, pkey=pkey)
        channel = client.invoke_shell()
        self._logger.info(f'*** Successfully connected!')

        if task_id != None :
            downlod_cmd = 'pyocs yandex ' + url + ' --task_id=' + task_id +' \t\n'
        else:
            downlod_cmd = 'pyocs yandex ' + url + ' \t\n'

        channel.send(downlod_cmd)
        remote_text = ''

        while True:
            time.sleep(2)
            try:
                recv_content = u(channel.recv(1024))
                print(recv_content)
                remote_text += recv_content
                if (("upload yandex usb" in remote_text) and ("upload yandex emmcbin" in remote_text)):
                    break
            except UnicodeDecodeError:
                pass

        client.close()

if __name__ == '__main__':

    d = Yadiredo('https://disk.yandex.ru/d/on0C6NSWkk5PXg')
    d.yandex_download_upload()