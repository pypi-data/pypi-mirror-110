# -- coding:utf8 --

"""
Usage:	docker [OPTIONS] COMMAND

A self-sufficient runtime for containers

Options:
      --config string      Location of client config files (default "/root/.docker")
  -c, --context string     Name of the context to use to connect to the daemon (overrides DOCKER_HOST env var
                           and default context set with "docker context use")
  -D, --debug              Enable debug mode
  -H, --host list          Daemon socket(s) to connect to
  -l, --log-level string   Set the logging level ("debug"|"info"|"warn"|"error"|"fatal") (default "info")
      --tls                Use TLS; implied by --tlsverify
      --tlscacert string   Trust certs signed only by this CA (default "/root/.docker/ca.pem")
      --tlscert string     Path to TLS certificate file (default "/root/.docker/cert.pem")
      --tlskey string      Path to TLS key file (default "/root/.docker/key.pem")
      --tlsverify          Use TLS and verify the remote
  -v, --version            Print version information and quit

Management Commands:
  builder     Manage builds
  config      Manage Docker configs
  container   Manage containers
  context     Manage contexts
  engine      Manage the docker engine
  image       Manage images
  network     Manage networks
  node        Manage Swarm nodes
  plugin      Manage plugins
  secret      Manage Docker secrets
  service     Manage services
  stack       Manage Docker stacks
  swarm       Manage Swarm
  system      Manage Docker
  trust       Manage trust on Docker images
  volume      Manage volumes

Commands:
  attach      Attach local standard input, output, and error streams to a running container
  build       Build an image from a Dockerfile
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes to files or directories on a container's filesystem
  events      Get real time events from the server
  exec        Run a command in a running container
  export      Export a container's filesystem as a tar archive
  history     Show the history of an image
  images      List images
  import      Import the contents from a tarball to create a filesystem image
  info        Display system-wide information
  inspect     Return low-level information on Docker objects
  kill        Kill one or more running containers
  load        Load an image from a tar archive or STDIN
  login       Log in to a Docker registry
  logout      Log out from a Docker registry
  logs        Fetch the logs of a container
  pause       Pause all processes within one or more containers
  port        List port mappings or a specific mapping for the container
  ps          List containers
  pull        Pull an image or a repository from a registry
  push        Push an image or a repository to a registry
  rename      Rename a container
  restart     Restart one or more containers
  rm          Remove one or more containers
  rmi         Remove one or more images
  run         Run a command in a new container
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
  search      Search the Docker Hub for images
  start       Start one or more stopped containers
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
  top         Display the running processes of a container
  unpause     Unpause all processes within one or more containers
  update      Update configuration of one or more containers
  version     Show the Docker version information
  wait        Block until one or more containers stop, then print their exit codes

Run 'docker COMMAND --help' for more information on a command.

docker volume

Usage:	docker volume COMMAND

Manage volumes

Commands:
  create      Create a volume
  inspect     Display detailed information on one or more volumes
  ls          List volumes
  prune       Remove all unused local volumes
  rm          Remove one or more volumes

Run 'docker volume COMMAND --help' for more information on a command.

"""
import argparse
import os,sys

def check_dir():
  dc_file = 'docker-compose.yml'
  if not os.path.exists(dc_file):
    print("执行目录错误：没有在当前目录发现docker-compose.yml！")



def main_cli():
    # 创建解析对象
    parser = argparse.ArgumentParser(
        usage="dc-help COMMAND", description="docker-compose辅助工具,帮助管理镜像、版本文件")
    # 获取第一层子命令操作对象
    sub_parsers = parser.add_subparsers(title="COMMAND",)
    # 创建一个子命令
    p1 = sub_parsers.add_parser("image",
                                usage='dc-help COMMAND image [-h] (--pack | --unpack | --clear | --upgrade)',
                                help="管理docker-compose.yml中的镜像，打包、装载、清理、升级")
    p2 = sub_parsers.add_parser("init-data",
                                usage="dc-help init-data [-h] (--pack | --unpack)",
                                help="init-data的压缩和解压缩")
    p3 = sub_parsers.add_parser("run-data",
                                usage="dc-help run-data [-h] (--pack | --unpack)",
                                help="run-data的压缩和解压缩2", add_help=True)
    # 互斥，且至少需要一个参数
    group = p1.add_mutually_exclusive_group(required=True)
    group.add_argument('--pack', action='store_true', help="对镜像进行自动打包")
    group.add_argument('--unpack', action='store_true', help="对镜像进行自动装载")
    group.add_argument('--clear', action='store_true', help="对镜像文件进行清理")
    group.add_argument('--upgrade', action='store_true',
                       help="对镜像文件进行自动装载，然后升级")

    def foo(args):
        print("args")
        print(args)
    p1.set_defaults(func=foo)  # 将函数foo 与子解析器foo绑定

    group = p2.add_mutually_exclusive_group(required=True)
    group.add_argument('--pack', action='store_true', help="对init-data进行自动打包")
    group.add_argument('--unpack', action='store_true',
                       help="对init-data进行自动解包")

    def foo2(args):
        print("args2")
        print(args)
    p2.set_defaults(func=foo2)  # 将函数foo 与子解析器foo绑定
    # init_data_pack_parser.set_defaults(func=print)
    group = p3.add_mutually_exclusive_group(required=True)
    group.add_argument('--pack', action='store_true', help="对run-data进行自动打包")
    group.add_argument('--unpack', action='store_true', help="对run-data进行自动解包")

    def run_data_unpack():
        print('run_data_unpack')
    p3.set_defaults(func=run_data_unpack)
    # 需要提前定义好目标函数
    # 添加子命令函数
    # def foo(args):
    #     print (args.x * args.y)

    # def bar(args):
    #     print ('((%s))' %args.z)

    # p1.set_defaults(func=print)
    # p2.set_defaults(func=print)

    # parser.parse_args(['--help'])
    # parser.parse_args(['a','--help'])
    check_dir()
    import sys
    args = parser.parse_args(sys.argv[1:])
    # print(args)
    args.func(args)
