# -*- coding:utf-8 -*-
import os
import sys
import requests
import json
from urllib.parse import quote
from urllib.parse import unquote
from artifactory import ArtifactoryPath
from loguru import logger
from artifactory import ArtifactoryProAccessor
import argparse

"""
    Artifactory Lib Util
    Author: ygong
    统一输入为未转码的制品库路径
    @:param user
    用户名
    @:param password
    密码
"""


class ArtifactoryLibUtil(object):
    def __init__(self, user, password):

        self._user = user
        self._password = password

    def artifactory_upload_file(self, local_path, artifactory_path):
        """
        上传本地文件到制品库
        :param local_path: 本地文件路径
        :param artifactory_path: 制品库路径
        :return: 无返回值
        """

        # 本地路径是文件
        # artifactory路径是目录

        if (local_path.endswith("/")):
            logger.error("源路径需为文件")
        elif (not artifactory_path.endswith("/")):
            logger.error("artifactory路径需以/结尾")
            logger.error("源路径需为文件")
        else:
            path = ArtifactoryPath(artifactory_path, auth=(self._user, self._password))
            path.deploy_file(local_path)

    def artifactory_download_file(self, local_path, artifactory_path):
        """
        下载远端文件到本地
        :param local_path: 本地文件路径
        :param artifactory_path: 制品库路径
        :return: 无返回值
        """

        # artifactory路径是文件
        # 本地路径是目录结尾的

        if self.artifactory_path_isdir(artifactory_path):
            logger.error("artifactory路径需为文件")
        else:
            file_name = artifactory_path.rpartition("/")[-1]
            path = ArtifactoryPath(
                artifactory_path, auth=(self._user, self._password)
            )
            local_path = local_path + "/" + file_name
            with path.open() as fd, open(local_path, "wb") as out:
                out.write(fd.read())

    def artifactory_upload_tree(self, local_dir, artifactory_dir):
        """
        上传本地文件夹到远程文件夹
        :param local_dir: 本地文件夹
        :param artifactory_dir: 远端artifactory文件夹
        :return:
        """

        # 两个都是目录
        local_list = os.listdir(local_dir)
        for local in local_list:
            src = local_dir + "/" + local
            self.create_artifactory_dir(artifactory_dir + "/")
            if os.path.isdir(src):
                self.create_artifactory_dir(artifactory_dir + "/" + local + "/")
                self.artifactory_upload_tree(src, artifactory_dir + "/" + local + "/")
            else:
                self.artifactory_upload_file(src, artifactory_dir + "/")

    def artifactory_download_tree(self, local_dir, artifactory_dir):
        """
        下载本地文件夹到远程文件夹
        :param local_dir: 本地文件夹
        :param artifactory_dir: 远端artifactory文件夹
        :return:
        """

        artifactory_list = self.list_artifactory_path(artifactory_dir)
        for path in artifactory_list:
            path = str(path)
            path_name = path.rpartition("/")[-1]
            if self.artifactory_path_isdir(path):
                self.create_local_dir(local_dir + "/" + path_name)
                self.artifactory_download_tree(local_dir + "/" + path_name + "/", path)
            else:
                self.artifactory_download_file(local_dir + "/", path)

    def list_artifactory_path(self, artifactory_path):
        """
        列出artifactory文件路径
        :param artifactory_path: artifactory路径
        :return:
        """
        path_list = []
        path = ArtifactoryPath(artifactory_path, auth=(self._user, self._password))

        for p in path:
            path_list.append(p)
        return path_list

    def artifactory_path_isdir_unquoted(self, unquoted_artifactory_path):
        """
        判断给出的路径是否目录(未转码)
        Args:
            artifactory_path: 制品库路径

        Returns:
            是目录返回True，是文件返回False，其他错误返回"error"
        """
        quoted_path = quote(str(unquoted_artifactory_path), safe="/:")
        path = ArtifactoryPath(quoted_path, auth=(self._user, self._password))
        stat = ArtifactoryPath.stat(path)
        try:
            return stat.is_dir
        except:
            return "error"

    def artifactory_path_isdir(self, artifactory_path):
        """
        判断给出的路径是否目录
        Args:
            artifactory_path: 制品库路径

        Returns:
            是目录返回True，是文件返回False，其他错误返回"error"
        """

        path = ArtifactoryPath(artifactory_path, auth=(self._user, self._password))
        stat = ArtifactoryPath.stat(path)
        try:
            return stat.is_dir
        except:
            return "error"

    """
    展示路径上所有属性
    @:param artifactory_path 制品库路径，如不存在则报错    
    """

    def create_artifactory_dir(self, artifactory_path):
        """
        :param: artifactory_path:artifactory_path: 制品库路径。
        :return: 成功:"success"/失败:"error"
        """
        try:
            path = ArtifactoryPath(
                artifactory_path, auth=(self._user, self._password)
            )
            if not self.artifactory_path_exist(artifactory_path):
                path.mkdir()
            return "success"
        except Exception as e:
            return "error"

    @staticmethod
    def create_local_dir(local_path):
        if not os.path.exists(local_path):
            os.makedirs(local_path)

    def artifactory_search_dir(self, artifactory_path, recursive_flag):
        """
        搜索远端文件夹
        :param artifactory_path: 搜索的远端的路径
        :param recursive_flag: 搜索模式
        :return:
        """
        rst_list = []
        if recursive_flag == "r":

            path_list = self.list_artifactory_path(artifactory_path)
            for path in path_list:
                if self.artifactory_path_isdir_unquoted(str(path)):
                    # 返回nested list
                    # list.append(self.artifactory_search_dir(path, "r"))
                    result = self.artifactory_search_dir(str(path), "r")
                    for r in result:
                        rst_list.append(r)
                    rst_list.append(str(path) + "/")
                else:
                    rst_list.append(str(path))
            return rst_list
        elif recursive_flag == "nr":
            path_list = self.list_artifactory_path(artifactory_path)
            for path in path_list:
                if self.artifactory_path_isdir_unquoted(str(path)):
                    rst_list.append(str(path) + "/")
                else:
                    rst_list.append(str(path))
            return rst_list
        else:
            logger.error("recursive标志错误")
            return "error"

    def quote_path(self, path):
        quoted_path = quote(path, safe="/:")
        return quoted_path

    def artifactory_path_exist_unquoted(self, unquoted_artifactory_path):

        """
                判断给出的路径是否目录(未转码)
                Args:
                    artifactory_path: 制品库路径

                Returns:
                    是目录返回True，是文件返回False，其他错误返回"error"
                """
        quoted_path = quote(str(unquoted_artifactory_path), safe="/:")
        path = ArtifactoryPath(quoted_path, auth=(self._user, self._password))
        if path.exists():
            return True
        else:
            return False

    def artifactory_path_exist(self, artifactory_path):

        """ 判断路径是否存在
        :param artifactory_path: artifactory路径(已转义后)，如果路径尾带"/"，但实际路径为文件，则认为路径不存在。
                                                 如果路径尾不带"/"，则认为可能文件可能目录。
        :return:True/False 存在/不存在
        """
        # path = ArtifactoryPath(artifactory_path, auth=(self._user, self._password))
        # if path.exists():
        #     return True
        # else:
        #     return False

        if artifactory_path.endswith("/"):
            path_type = "dir"
            artifactory_path = artifactory_path.rstrip("/")

        else:
            path_type = "any"

        if "%" not in artifactory_path:
            artifactory_path_encode = quote(artifactory_path, safe="/:")
        else:
            artifactory_path_encode = artifactory_path

        url_list = artifactory_path_encode.partition("/artifactory/")
        url = "{0}{1}api/storage/{2}".format(url_list[0], url_list[1], url_list[2])

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }
        result = requests.get(url, headers=headers, auth=(self._user, self._password))

        if result.status_code == 404:
            # 路径不存在
            return False
        elif result.status_code != 200:
            logger.error("{0}".format(result.text))
            return False
        else:
            dict_str = result.content.decode("utf-8")
            data_dict = json.loads(dict_str)
            query_url = quote(data_dict.get("uri"), safe="/:")

            # 解决路径中有类似!()的未转义符号时的问题
            query_url_unquote = unquote(query_url)
            url_unquote = unquote(url)
            if query_url_unquote == url_unquote:
                if path_type == "dir" and "size" in data_dict.keys():
                    return False
                return True
            else:
                # 解决路径有多余空格时，路径仍存在的问题
                return False

    """
    设置属性
    @:param artifactory_path artifactory_path路径，如不存在则报错
    @:param key 标签的键
    @:param value 标签的值
    """

    def artifactory_set_property(self, artifactory_path, key, value):
        path = ArtifactoryPath(artifactory_path, auth=(self._user, self._password))
        if self.artifactory_path_exist(artifactory_path):
            try:
                properties = path.properties
                properties[key] = value
                path.properties = properties
                return "success"
            except:
                logger.error("set properties failed")
                return "error"
        else:
            logger.error("artifactory path {0} doesn't exist".format(artifactory_path))
            return "error"

    """
    移除属性
    @:param artifactory_path artifactory_path路径，如不存在则报错
    @:param key 要移除的标签键
    """

    def artifactory_remove_property(self, artifactory_path, key):
        path = ArtifactoryPath(artifactory_path, auth=(self._user, self._password))
        if self.artifactory_path_exist(artifactory_path):
            try:
                properties = path.properties
                path.properties = properties
                properties.pop(key)
                return "success"
            except KeyError as e:
                logger.error("no this key")
                return "error"
            except:
                logger.error("remove properties failed")
                return "error"
        else:
            logger.error("no this artifactory path")
            return "error"

    """
    展示路径上所有属性
    @:param artifactory_path 制品库路径，如不存在则报错    
    """

    def artifactory_list_properties(self, artifactory_path):
        path = ArtifactoryPath(artifactory_path, auth=(self._user, self._password))
        if self.artifactory_path_exist(artifactory_path):
            properties_dict = path.properties
            for key in properties_dict:
                properties_dict[key] = properties_dict[key][0]
            return properties_dict
        else:
            logger.error("no this artifactory path")
            return "error"

    """
    移动制品库
    @:param src_path artifactory路径，要移动的源路径，如不存在则报错(未转义前)   
    @:param dst_path artifactory路径，移动的目的路径，如不存在则创建(未转义前)

                     源路径为文件时，如果目的路径以/结尾，判定为目录，以原文件名移动
                     源路径为文件时，如果目的路径不以/结尾，判定为文件，以该文件名重命名移动

                     源路径为目录"A"，目的路径为"B/"(以/结尾)，则最终移动结果为"B/A/"
                     源路径为目录"A"，目的路径为"B"(不以/结尾)，在最终移动结果为"B"（等于重命名目录）

                     ※如果目的路径已存在，则不变更它的创建时间
                     ※目录属性在移动后会被保留

    """

    def artifactory_move(self, src_path, dst_path):
        """
        文件剪切
        :param src_path: 源文件路径
        :param dst_path: 目标文件路径
        :return:
        """
        source = ArtifactoryPath(src_path, auth=(self._user, self._password))
        dest = ArtifactoryPath(dst_path, auth=(self._user, self._password))

        if source.exists():
            # 如果目的路径为目录则创建目录
            if dst_path.endswith("/"):
                if not dest.exists():
                    dest.mkdir()
            # 如果源路径为目录则也创建目的路径目录
            if source.is_dir():
                if not dest.exists():
                    dest.mkdir()

            if self.artifactory_path_isdir_unquoted(src_path):
                if not dst_path.endswith("/"):
                    src_path_list = self.artifactory_search(src_path, "r", "a")
                    for each_path in src_path_list:
                        path_suffix = each_path.rpartition(src_path)[-1]
                        file_src_path = ArtifactoryPath(each_path, auth=(self._user, self._password))
                        if self.artifactory_path_isdir_unquoted(each_path):
                            file_dst_path = ArtifactoryPath(dst_path, auth=(self._user, self._password))
                        else:
                            file_dst_path = ArtifactoryPath(dst_path + "/" + path_suffix,
                                                            auth=(self._user, self._password))
                        file_src_path.move(file_dst_path)
                else:
                    source.move(dest)
                # 如果源路径为空，则最后删除源目录
                if source.exists() and self.artifactory_search(src_path, "r", "a") == []:
                    self.artifactory_remove(src_path)
            else:
                source.move(dest)

            return "success"

        else:
            logger.error("source artifactory path does not exist")
            return "error"

    """
    复制制品库
    @:param src_path artifactory路径，要复制的源路径，如不存在则报错(未转义前)   
    @:param dst_path artifactory路径，复制的目的路径，如不存在则创建(未转义前)

                     源路径为文件时，目的路径如果以/结尾，判定为目录，以原文件名复制
                     源路径为文件时，目的路径如果不以/结尾，判定为文件，以该文件名重命名复制

                     源路径为目录"A"，目的路径为"B/"(以/结尾)，则最终拷贝结果为"B/A/"
                     源路径为目录"A"，目的路径为"B"(不以/结尾)，在最终拷贝结果为"B"（等于重命名目录）

                     ※如果目的路径已存在，则不变更它的创建时间
                     ※目录属性在移动后不会被保留

    """

    def artifactory_copy(self, src_path, dst_path):
        """
            文件粘贴
            :param src_path: 源文件路径
            :param dst_path: 目标文件路径
            :return:
        """
        source = ArtifactoryPath(src_path, auth=(self._user, self._password))
        dest = ArtifactoryPath(dst_path, auth=(self._user, self._password))

        if source.exists():
            # 如果目的路径为目录则创建目录
            if dst_path.endswith("/"):
                if not dest.exists():
                    dest.mkdir()
            # 如果源路径为目录则也创建目的路径目录
            if source.is_dir():
                if not dest.exists():
                    dest.mkdir()
            if self.artifactory_path_isdir_unquoted(src_path):
                if not dst_path.endswith("/"):
                    src_path_list = self.artifactory_search(src_path, "r", "a")
                    for each_path in src_path_list:
                        path_suffix = each_path.rpartition(src_path)[-1]
                        file_src_path = ArtifactoryPath(each_path, auth=(self._user, self._password))

                        if self.artifactory_path_isdir_unquoted(each_path):
                            dict_dst_path = dst_path + "/" + path_suffix
                            if not self.artifactory_path_exist(dict_dst_path):
                                self.create_artifactory_dir(dict_dst_path)
                        else:
                            file_dst_path = ArtifactoryPath(dst_path + "/" + path_suffix,
                                                            auth=(self._user, self._password))
                            file_src_path.copy(file_dst_path)
                else:
                    source.copy(dest)
            else:
                source.copy(dest)
            return "success"
        else:
            logger.error("source artifactory path does not exist")
            return "error"

    def artifactory_search(self, artifactory_path, recursive_flag, only_flag):
        """
        搜索远端文件
        :param artifactory_path: artifactory_path路径，如不存在则报错，如果是文件返回原路径
        :param recursive_flag: 是否递归搜索:r/nr
        :param only_flag: 只输出文件/目录:f/d 其余值则输出所有
        :return:
        """
        try:
            if self.artifactory_path_exist(artifactory_path) == False:
                logger.error("no this artifactory path")
                result = "error"
            else:
                if self.artifactory_path_isdir(artifactory_path):
                    result = self.artifactory_search_dir(artifactory_path, recursive_flag)
                else:
                    result = [artifactory_path]

                # 只输出文件
                if only_flag == "f":
                    temp_list = []
                    for x in result:
                        if not x.endswith("/"):
                            temp_list.append(x)
                    result = temp_list
                # 只输出目录
                elif only_flag == "d":
                    temp_list = []
                    for x in result:
                        if x.endswith("/"):
                            temp_list.append(x)
                    result = temp_list

            return result
        except:
            return "error"

    """
    上传制品
    @:param local_path 源本地文件或路径，如不存在则报错
    @:param artifactory_path artifactory目的路径，如不存在则创建
                             artifactory目的路径如果以"/"结尾，则表示以原文件名传到该路径下
                             artifactory目的路径如果不以"/"结尾，如 
                             "Release/NWF2020/BPC_10.10.10/a" 则文件名为a
                             如果路径下已有文件夹a，则效果同"Release/NWF2020/BPC_10.10.10/a/"

    """

    def artifactory_upload(self, local_path, artifactory_path):
        # 判断本地路径是否存在
        if not os.path.exists(local_path):
            logger.error("not found")
            return "error"
        else:
            try:
                if os.path.isdir(local_path):
                    self.artifactory_upload_tree(local_path, artifactory_path)
                    return "success"
                elif os.path.isfile(local_path):
                    self.create_artifactory_dir(artifactory_path.rpartition("/")[0])
                    self.artifactory_upload_file(local_path, artifactory_path + "/")
                    return "success"
            except Exception as e:
                return "error"

    """
    下载制品
    @:param local_path 本地目的路径，如不存在则创建
    @:param artifactory_path artifactory源路径，如不存在则报错
    """

    def artifactory_download(self, local_path, artifactory_path):
        # 判断远端路径是否存在
        if not self.artifactory_path_exist(artifactory_path):
            logger.error("no this artifactory path")
            return "error"
        else:
            try:
                if self.artifactory_path_isdir(artifactory_path):
                    self.artifactory_download_tree(local_path, artifactory_path)
                    return "success"
                elif self.artifactory_path_isdir(artifactory_path) is False:
                    self.artifactory_download_file(local_path, artifactory_path)
                    return "success"
                else:
                    return "error"
            except:
                return "error"

    """
    删除制品
    @:param artifactory_path 要删除的artifactory路径，如不存在则报错
    """

    def artifactory_remove(self, artifactory_path):
        path = ArtifactoryPath(artifactory_path, auth=(self._user, self._password))
        try:
            if self.artifactory_path_exist(artifactory_path):
                if self.artifactory_path_isdir(artifactory_path):
                    path.rmdir()
                else:
                    path.unlink()
                return "success"
            else:
                logger.error("no this artifactory path")
                return "error"
        except:
            logger.error("remove artifactory path failed")
            return "error"

    """
    使用aql进行查询
    @aql_query 使用aql语法进行查询
    返回查询结果{'results':[...],'range':{...}}
    """

    def artifactory_query(self, artifactory_path, aql_query: dict):
        if not artifactory_path.endswith("/"):
            artifactory_path = artifactory_path + "/"

        url = artifactory_path + "api/search/aql"

        headers = {
            'Content-Type': "text/plain"}

        payload = json.dumps(aql_query)
        payload = "items.find({0})".format(payload)

        result = requests.post(url, data=payload, headers=headers, auth=(self._user, self._password))

        if result.status_code != 200:
            logger.error("{0}".format(str(result.text)))
            return None
        else:
            result_json = json.loads(result.text)
            return result_json

    def artifactory_filepath_md5(self, artifactory_path):
        """
        :param artifactory_path: 未转码前制品库路径
        :return: {文件:md5}
        """
        if not self.artifactory_path_exist_unquoted(artifactory_path):
            logger.error("no this artifactory path")
            return "error"
        else:
            quoted_artifactory_path = self.quote_path(artifactory_path)
            stat = self.artifactory_path_stat(quoted_artifactory_path)
            return {artifactory_path: stat.md5}

    def artifactory_path_md5(self, artifactory_path):
        """
        :param artifactory_path: artifactory路经
        :return:
            artifactory_path为文件时，返回{文件:md5}
            artifactory_path为目录时，返回{文件A:md5,文件B:md5,...}
        """

        file_list = self.artifactory_search(artifactory_path, "r", "f")
        result_dict = {}
        for file in file_list:
            result_dict.update(self.artifactory_filepath_md5(file))
        return result_dict

    def artifactory_path_stat(self, artifactory_path):

        """
        :param artifactory_path制品库路径（需为转义前）
        :return: 类型为ArtifactoryStat的对象
        包含以下属性：
        ctime
        mtime
        created_by
        modified_by
        mime_type
        size
        sha1
        sha256
        md5
        is_dir
        children
        """
        path = ArtifactoryPath(artifactory_path, auth=(self._user, self._password))
        return ArtifactoryPath.stat(path)

    def artifactory_promote_docker(self, src_path, dst_path, copy_flag=True):
        """
        :param src_path: 源docker路径
        :param dst_path: 目的docker路径
        :param copy_flag: 是否拷贝标志,默认True
        :return: success/error
        """
        tag = [x for x in src_path.split("/") if x][-1]
        target_tag = [x for x in dst_path.split("/") if x][-1]

        src_string = src_path.partition("/" + tag)[0].partition("/artifactory/")[-1]
        artifactory_server = src_path.partition("/artifactory/")[0]
        # dst_string = dst_path.partition("/"+target_tag)[0].partition("/artifactory/")[-1]
        dst_repo_tag = dst_path.partition("/artifactory/")[-1]
        dst_string = dst_repo_tag.rpartition("/" + target_tag)[0]

        repo_key = src_string.split("/")[0]
        target_repo_key = dst_string.split("/")[0]

        docker_repo = src_string.partition(repo_key + "/")[-1]
        target_docker_repo = dst_string.partition(target_repo_key + "/")[-1]

        url = "{0}/artifactory/api/docker/{1}/v2/promote".format(artifactory_server, repo_key)
        data_dict = {
            "targetRepo": target_repo_key,
            "dockerRepository": docker_repo,
            "targetDockerRepository": target_docker_repo,
            "tag": tag,
            "targetTag": target_tag,
            "copy": copy_flag
        }
        data = json.dumps(data_dict)

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }
        result = requests.post(url, data=data, headers=headers, auth=(self._user, self._password))

        if result.status_code != 200:
            logger.error("{0}".format(result.content))
            return "error"
        else:
            return "success"

    def artifactory_get_docker_sha256(self, artifactory_path):
        """
        :param artifactory_path: docker路径
        :return: docker的sha256值
        """
        artifactory_path = artifactory_path + "/manifest.json"
        if self.artifactory_path_exist(artifactory_path):
            path = ArtifactoryPath(artifactory_path, auth=(self._user, self._password))
            result = self.sub_get_file_json_sha256(artifactory_path)
            return result
        else:
            return "error"

    def sub_get_file_json_sha256(self, artifactory_path):
        """
        :param artifactory_path: docker路径
        :return: 该docker的sha256值
        """
        local_path = os.getcwd()
        # basename = manifest.json
        basename = artifactory_path.split("/")[-1]
        self.artifactory_download_file(local_path, artifactory_path)
        file_path = local_path + "/{0}".format(basename)
        with open(file_path, "r") as f:
            dict_data = json.load(f)
        os.remove(file_path)
        return dict_data.get("config").get("digest").partition("sha256:")[-1]

    def artifactory_latest_child_path(self, artifactory_path):
        """
        :param artifactory_path: 父路径
        :return: 修改时间最晚的子路径
        """

        path = ArtifactoryPath(artifactory_path, auth=(self._user, self._password))
        child_path_dict = {}
        for p in path:
            a = ArtifactoryPath.stat(p)
            child_path_dict[p] = a.mtime
        latest_key = sorted(child_path_dict)[-1]
        return latest_key


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="artifactory tool")
    # parser.add_argument("-usr", type=str)
    # parser.add_argument("-pwd", type=str)
    # parser.add_argument("-func", type=str)
    # args = parser.parse_args()

    usr = "admin"
    pwd = "Sseadmin123"
    # func = args.func

    artifactory_lib_util = ArtifactoryLibUtil(usr, pwd)
    result = artifactory_lib_util.create_artifactory_dir(
        "http://artifactory.test.com:8081/artifactory/pypi-local/halring"
    )
    pxd = 1

    # print(eval("artifactory_lib_util.{0}".format(func)))
    # python artifactory_lib_util.py -usr aqc001 -pwd l1nx1L1n@n6 -func "artifactory_latest_child_path(path)"
