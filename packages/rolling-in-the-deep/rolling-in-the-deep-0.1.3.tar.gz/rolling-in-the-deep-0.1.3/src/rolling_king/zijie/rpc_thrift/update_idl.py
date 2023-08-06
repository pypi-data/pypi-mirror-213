"""下载idl

使用手册：https://bytedance.feishu.cn/docs/doccnSuhygJAzwis5ryxOWUt0le
非中idl文件归档在group idl和cpputil/service_rpc_idl这两处
每个库的工程结构是不一样的：
    group idl下归档的idl以group idl的父目录作为构建根目录，引用范围涉及group idl下的所有库
    service_rpc_idl内的idl以service_rpc_idl库作为构建根目录，一般采用相对当前idl路径引用的方式引用其他idl文件，引用文件都在service_rpc_idl库下
"""
import os
import re
import logging
import subprocess

from copy import deepcopy

logger = logging.getLogger(__name__)


class UpdateIdl(object):

    def update_idl(self, idl_file_remote, idl_path_local, branch, repo, token):
        need_update = os.getenv('NEED_UPDATE_IDL') != '0' and True or False
        if not need_update:
            idl_local = self.simplifyPath(idl_path_local + str.split(repo, ".")[0] + "/" + idl_file_remote)
            return idl_local
        idl_path = os.path.split(idl_file_remote)[0]
        idl_sub_path = idl_path_local + str.split(repo, ".")[0] + "/" + idl_path
        logger.debug("idl_sub_path: %s", idl_sub_path)
        if not os.path.exists(idl_sub_path):
            os.makedirs(idl_sub_path)
        idl_local = self.simplifyPath(idl_path_local + str.split(repo, ".")[0] + "/" + idl_file_remote)
        logger.debug("idl_local: %s", idl_local)
        idl_file_remote = self.simplifyPath(idl_file_remote)
        logger.debug("idl_file_remote: %s", idl_file_remote)
        self.idl_update_os(token, repo, branch, idl_file_remote, idl_local)
        with open(idl_local, 'r') as idl_file_local:
            for line in idl_file_local:
                find_include = re.search("^include *", line)
                if find_include:
                    if (len(str.split(line, '"'))) > 1:
                        next_idl_name = str.split(line, '"')[1]
                        if (next_idl_name.startswith(".") == False) & ("/" in next_idl_name):
                            repo, next_idl_file = self.idl_file_in_other_repo(next_idl_name)
                        else:
                            next_idl_file = idl_path + '/' + next_idl_name
                        self.update_idl(next_idl_file.lstrip('/'), idl_path_local, branch, repo, token)
        logger.debug("idl_file_local=%s", idl_file_local.name)
        return idl_file_local.name

    def idl_file_in_other_repo(self, idl):
        repo_out = str.split(idl, '/', 2)[0] + '/' + str.split(idl, '/', 2)[1]
        idl_new = str.split(idl, '/', 2)[2]
        return repo_out, idl_new

    def idl_update_os(self, token, repo, branch, idl_file_remote, idl_local):
        logger.debug("repo=%s, branch=%s, idl_file_remote=%s, idl_local=%s", repo, branch, idl_file_remote, idl_local)
        repo_encode = repo.replace('/', '%2F')
        idl_file_remote_encode = idl_file_remote.replace('/', '%2F')
        idl_copy = "curl --request GET --header 'PRIVATE-TOKEN: "+token+"' 'https://code.byted.org/api/v4/projects/" + repo_encode + "/repository/files/" + idl_file_remote_encode + "/raw?ref=" + branch + "' >> " + idl_local
        logger.debug("idl_copy: %s", idl_copy)
        if os.path.exists(idl_local):
            os.remove(idl_local)
        logger.debug("curl results: %s", os.popen(idl_copy).read())

    def simplifyPath(self, path):
        """
        :type path: str
        :rtype: str
        """
        logger.debug("path before simplify: %s", path)
        path.replace('//', '/')
        list = path.split('/')
        res = []
        for i in range(len(list)):
            if list[i] == '..' and len(res) > 0:
                res = res[:-1]
            elif list[i] != '' and list[i] != '.' and list[i] != '..':
                res.append(list[i])
        simplifyPath = '/' + '/'.join(res)
        logger.debug("path after simplify: %s", simplifyPath)
        return simplifyPath


def update(token, idl, branch='master', dst='.'):
    """
    token: self access token, used for gitlab authentication, configured on gitlab
    idl: idl url, e.g. https://code.byted.org/idl/i18n_ad/ad_understanding/ad_understanding.thrift
    branch: git branch
    dst: destination directory of idl downloaded, e.g. ../tmp. directory struct unchanged, e.g. ${dst}/idl/i18n_ad/...
    """
    need_update = os.getenv('NEED_UPDATE_IDL') != '0' and True or False
    if not need_update:
        return True
    tmp = re.search(r'\w+\.\w+\.\w+/(?P<repo>\w+/\w+)/(blob/master/|blob/{}/|)(?P<idl>.+\.thrift)'.format(branch), idl)
    if tmp is None:
        logger.error('{} is not valid'.format(idl))
        return False
    repo = tmp.group('repo')
    idl = tmp.group('idl')
    repo_type = get_repo_type(repo)
    if repo_type == 'service_rpc_idl':
        include_paths = ['cpputil/service_rpc_idl']
    elif repo_type == 'idl/':
        include_paths = ['']
    else:
        include_paths = [repo]
    updated_files = set()
    return download_idls(repo, idl, token, dst, branch, include_paths, updated_files)


def get_repo_type(repo):
    """获取git repo name
    判断待下载idl归档的库，进而决定采用哪种方式下载
    """
    if 'service_rpc_idl' in repo:
        return 'service_rpc_idl'
    elif repo.startswith('idl/'):
        return 'idl/'
    return None


def download_idls(repo, idl, token, dst='.', branch='master', include_paths=[], updated_files=set()):
    """下载当前.thrift文件，及其引用到的其他.thrift文件"""
    # 下载当前idl
    dst_file = os.path.join(dst, repo, idl)
    if dst_file in updated_files:
        return True
    updated_files.add(dst_file)
    content = download_single_idl(token, repo, idl, branch)
    if content is None:
        logger.error('update {}/{} failed'.format(repo, idl))
        return False
    output(content, dst_file)
    logger.debug('update {}/{} success'.format(repo, idl))
    # 获取当前idl引用到的其他idl
    idls_to_update = get_idl_to_update(content)
    # 根据引用方式的不同，采用不同方式递归下载其他引用到的idl
    for next_idl in idls_to_update:
        if re.match(r'[.]{1,2}/.*', next_idl) or re.match(r'\w+\.thrift', next_idl):  # 相对当前文件
            abs_idl = os.path.normpath(os.path.join(repo, os.path.dirname(idl), next_idl))
            tmp = abs_idl.split('/')
            next_repo = '/'.join(tmp[:2])
            next_idl = '/'.join(tmp[2:])
            if not download_idls(next_repo, next_idl, token, dst, branch, include_paths, updated_files):
                return False
        elif re.match(r'[\w]+/.*', next_idl):
            cur_include_paths = deepcopy(include_paths)
            cur_include_paths.append(os.path.join(repo, os.path.dirname(idl)))
            for path in cur_include_paths:
                tmp = os.path.normpath(os.path.join(path, next_idl)).split('/')
                next_repo = '/'.join(tmp[:2])
                next_idl = '/'.join(tmp[2:])
                if download_idls(next_repo, next_idl, token, dst, branch, include_paths, updated_files):
                    break
            else:
                return False
        else:
            return False
    return True


def download_single_idl(token, repo, idl, branch):
    branches = ['master']
    if branch != 'master':
        branches.insert(0, branch)
    for br in branches:
        cmd = ("curl --request GET "
               "--header 'PRIVATE-TOKEN: {token}' "
               "'https://code.byted.org/api/v4/projects/{repo}/repository/files/{idl}/raw?"
               "ref={branch}'").format(
            token=token,
            repo=repo.replace('/', '%2F'),
            idl=idl.replace('/', '%2F'),
            branch=br
        )
        content = shell_command(cmd)
        if content is None or re.search(r'"404.*Not Found"', content):
            logger.warning('download {}/{} on branch {} failed:{}'.format(repo, idl, branch, content))
            continue
        return content
    return None


def shell_command(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True)
    if res.returncode != 0:
        logger.error('"{}" exec failed'.format(cmd))
        logger.error('reason: {}'.format(res.stderr.decode()))
        return None
    return res.stdout.decode()


def get_idl_to_update(content):
    """获取当前文件引用到的.thrift文件"""
    res = []
    for o in re.finditer(r'^\s*include\s+[\'"](?P<file>.*)[\'"]', content, flags=re.MULTILINE):
        path = o.group('file')
        res.append(path)
    return res


def output(content, dst_file):
    # todo: 文件锁
    d = os.path.dirname(dst_file)
    os.makedirs(d, exist_ok=True)
    if os.path.exists(dst_file):
        with open(dst_file) as fd:
            tmp = fd.read()
        if content == tmp:
            return True
        else:
            os.remove(dst_file)
    with open(dst_file, mode='w') as fd:
        fd.write(content)
    return True


def get_psm_idls(idl_remote, git_token):
    """
    使用文档: https://bytedance.feishu.cn/docs/doccnSuhygJAzwis5ryxOWUt0le
    """
    psm_idl = ""
    if idl_remote is not None:
        logger.info(f"psm idl_remote: {idl_remote}")
        logger.info(f"git_token: {git_token}")
        updater = UpdateIdl()
        psm_idl = updater.update_idl(idl_file_remote=idl_remote["idl_file"],
                                     idl_path_local='{}'.format(
                                         # os.path.dirname(os.path.abspath(__file__)) + '/../idls/'),  # 在导入包时该路径则在包中，而不在测试项目中。
                                         get_idl_location()),  # 所以要使用该方法。
                                     branch=idl_remote["branch"],
                                     repo=idl_remote["repo"],
                                     token=git_token)
        logger.info("psm idl path: %s", psm_idl)
    return psm_idl


def get_idl_location():
    curr_sys_path = os.getcwd()
    index_of_com = curr_sys_path.find("com")
    if index_of_com != -1:
        # 下面一行是绝对路径传入获取配置文件的方法。
        return curr_sys_path[0:index_of_com] + "com/zijie/tests/thrift/idls/"
    else:
        return curr_sys_path + "/com/zijie/tests/thrift/idls/"


if __name__ == '__main__':
    logger.debug(update(idl='https://code.byted.org/idl/i18n_ad/style/engine.thrift',
                 branch='master',
                 token='xxx',
                 dst='tmp'))
    logger.debug(update(idl='https://code.byted.org/cpputil/service_rpc_idl/blob/master/ad/lego.thrift',
                 branch='master',
                 token='xxx',
                 dst='tmp'))
    logger.debug(update(idl='https://code.byted.org/cpputil/service_rpc_idl/blob/master/ad/tetris/instant_page_interface_i18n.thrift',
                 branch='master',
                 token='xxx',
                 dst='tmp'))
