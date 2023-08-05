

def read_images():
  dc_file = 'docker-compose.yml'
  imgs =[]
  with open(dc_file,'rt') as f:
    lines = f.readlines()

  for l in lines:
    l = l.strip()
    if 'image:' in l and l[0] !='#':
        imgs.append(l.split()[1])
  return list(set(i))

def do_image_pack():
  imgs = read_images()
  pack_path = './back/image/'
  #若没有back文件夹，新建
  if not os.path.exists(pack_path):
    run_cmd("mkdir "+pack_path)

  #打包镜像
  # docker save IMAGE > xxx.tar #  或者 docker save -o xxx.tar IMAGE
  # gizp xxx.tar.gz xxx.tar  # 可以压缩为原来为三分之一
  for i in imgs:
    print('打包镜像:'+i)
    result = os.popen("docker inspect -f '{{ .Created }}' "+i)
    res = result.read().strip()
    dt = datetime.datetime.strptime(res[:26],"%Y-%m-%dT%H:%M:%S.%f")
    time = dt.strftime("%Y%m%d%H%M%S")
    if not os.path.exists(pack_path+ i.split("/")[-1]+"_"+time+'.tar.gz'):
      cmd = "docker save "+ i +" > " +pack_path+ i.split("/")[-1]+"_"+time+'.tar'
      run_cmd(cmd)
      cmd = "gzip "+ pack_path +i.split("/")[-1]+"_"+time+'.tar'
      run_cmd(cmd)
    else:
      print(i.split("/")[-1]+"_"+time+'.tar 已存在!')


def do_image_unpack():
  pass

def do_image_clear():
  pass

def do_image_upgrade():
  pass