import os
import json
# from git import Git
import subprocess
import requests


class GitUtil(object):
    '''
    依靠执行机器上的ssh公钥key获得git相关权限
    因此不使用usr,pwd字段
    '''

    def __init__(self, token):

        # self._git = Git()
        self._token = token

    def popen_block2(self, cmd):
        # stdin = DEVNUL用于解决win7上句柄无效的问题
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, stdin=subprocess.DEVNULL)
        stdout = p.stdout.read()
        stderr = p.stderr.read()
        p.communicate()
        if p.returncode == 0:
            return {"status": True,
                    "rc": p.returncode,
                    "message": stdout}
        else:
            return {"status": False,
                    "rc": p.returncode,
                    "message": stderr}

    def git_clone_branch(self, repository_url, local_repository_path, branch):
        git_clone_cmd = ['git', 'clone', '-b', branch, repository_url, local_repository_path]
        try:
            # 清空clone本地目录
            # self._os_util.removeDirs(local_repository_path)
            # 使用subprocess.check_all如果clone过程中出错则直接抛错，所以无需读取process内容
            process = subprocess.check_call(git_clone_cmd, shell=True, close_fds=True)
            # process.communicate()
            clone_status = 'SUCCESS'

        except Exception as e:
            clone_status = 'ERROR'
            if e.returncode == 128:
                message = "{0} 或 {1} 不存在".format(repository_url, branch)
            else:
                message = "git clone发生错误，错误码{0}".format(e.returncode)
            return {
                "status": clone_status,
                "content": message
            }
        return {
            'status': clone_status,
            'local_repo_path': local_repository_path
        }

    def git_change_branch(self, local_repository_url, branch):
        git_change_branch_cmd = "git checkout {0}".format(branch)
        os.chdir(local_repository_url)
        result = self.popen_block2(git_change_branch_cmd)
        return result

    def git_diff(self, local_repository_path, COMMIT_ID_1, COMMIT_ID_2):
        '''
        :param local_repository_path: 本地代码仓库路径
        :param COMMIT_ID_1: 前commit
        :param COMMIT_ID_2: 后commit
        :return:"status": "error",
                "message": run_diff_result
        '''

        os.chdir(local_repository_path)
        # 如使用 git diff --stat commitid1~ commitid2 如果commitid1=2，仍会带上本次交付的差异
        # 因此改使用命令git diff --stat commitid1 commitid2
        # 因win7和win10差异, 改增加Popen中的stdin=subprocess.DEVNULL参数
        git_diff_cmd = "git diff --stat {0} {1}".format(COMMIT_ID_1, COMMIT_ID_2)
        p = subprocess.Popen(git_diff_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                             stdin=subprocess.DEVNULL)
        stdout, stderr = p.communicate()
        run_diff_result = stdout.decode('utf-8', 'ignore').strip().splitlines()

        if run_diff_result:
            if not "fatal" in run_diff_result[0]:
                diff_info_list = run_diff_result[-1].split(",")
                file_changed_count = int(diff_info_list[0].partition("file")[0].strip())
                insertion_count = 0
                deletion_count = 0

                for diff_info_item in diff_info_list:
                    if "insertion" in diff_info_item:
                        insertion_count = int(diff_info_item.partition("insertion")[0].strip())

                    if "deletion" in diff_info_item:
                        deletion_count = int(diff_info_item.partition("deletion")[0].strip())

                return {
                    "status": "success",
                    "message": {
                        'total': "{0}".format(insertion_count + deletion_count),
                        'add_count': "{0}".format(insertion_count),
                        'del_count': "{0}".format(deletion_count),
                        'difference_files': "{0}".format(file_changed_count)
                    }
                }

            else:
                return {
                    "status": "error",
                    "message": run_diff_result
                }

        # 无返回说明相同
        else:
            return {
                "status": "success",
                "message":
                    {
                        'total': "{0}".format(0),
                        'add_count': "{0}".format(0),
                        'del_count': "{0}".format(0),
                        'difference_files': "{0}".format(0)
                    }
            }

    def git_get_commit_id(self, local_repository_path):
        """
        本地获取commit id
        """
        git_get_commit_id_cmd = "git rev-parse HEAD"
        os.chdir(local_repository_path)

        result = self.popen_block2(git_get_commit_id_cmd).get("message").decode("utf-8").strip()

        return result

    def git_get_commit_id_byapi(self, repository_path, branch, port="8001"):
        """
        使用api获取commit id
        """
        url = ""
        group = ""
        repo = ""

        # ssh方式，需要转换
        if "git@" in repository_path:
            repo = repository_path.rpartition("/")[2].replace(".git", "")
            group = repository_path.rpartition("/")[0].rpartition(":")[2]
            url = "http://{0}".format(repository_path.split("@")[1].split(":")[0])

        # http形式，以.git从右往左切路径
        elif "http" in repository_path:
            if repository_path.endswith("/"):
                repository_path = repository_path.rpartition("/")[0]
            repo = repository_path.rpartition("/")[2]
            if repo.endswith(".git"):
                repo = repo.replace(".git", "")
            group = repository_path.rpartition("/")[0].rpartition("/")[2]
            # http://196.123.135.6
            url = repository_path.rpartition(":")[0]
            # 8001
            port = repository_path.rpartition(":")[2].partition("/")[0]

        api_url = "{0}:{1}/api/v4/projects/{2}%2F{3}/repository/commits/{4}".format(url, port, group, repo, branch)

        querystring = {"private_token": self._token}

        payload = ""
        headers = {
            'cache-control': "no-cache",
        }

        response = requests.request("GET", api_url, data=payload, headers=headers, params=querystring)
        return (json.loads(response.text).get("id"))

    @staticmethod
    def convert_ssh2http(repository_url, port=8081):
        """
        2020/10/23
        author: zqxu
        convert clone ssh url to http url
        :param repository_url: the url of repository
        :param port: git port
        :return: the http url of git repository
        """
        if not repository_url == "":
            repository_url = repository_url.replace("http://", "git@").replace(":" + str(port) + "/", ":")
            return repository_url
        else:
            return False

    @staticmethod
    def convert_http2ssh(repository_url, port=8081):
        """
        2020/10/23
        author: zqxu
        convert clone http url to ssh url
        :param repository_url:
        :param port: git port
        :return: the ssh url of git repository
        """
        if not repository_url == "":
            repository_url = repository_url.replace("git@", "http://").replace(":", ":" + str(port) + "/")
            return repository_url
        else:
            return False
