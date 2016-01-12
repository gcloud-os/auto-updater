


 *  升级包名格式

            typ包类型_cut客户代号_ver包版本_md5校验码.zip

            包类型：    软件包名称
            客户代号：  identifying of updater. 
            包版本:     升级工具取得升级包列表，从这里得到包版本，从而判断是否需要升级;
                        版本格式是年月日，固定8个整数
            md5校验码： 下载完成后基于此校验码进行完整性校验
            package type is zip, you can put anythings you want into package, and do what you
            want with your specific handle script also in package.

            example:
                typPortal_cutTengzheng_ver20151209_md5xxxxxxxxxxxx.zip
                |--------------------------------------------------
                | - > xxxx.rpm    something need to be install.
                | - > any.others  
                | - > xxxx/a.py
                | - > readme.txt  what ever, say something you want.
                | - > install.sh  安装脚本，第一个参数是脚本(安装文件)所在路径，第二个参数是日志文件路径;
                |                 这个脚本一定要存在，
                | - > restart.sh     最后执行的脚本，可以没有这个脚本，取决于升级包的具体要求；比如可以在安装目录
                |                 做一些记号，让服务知道可以重启自己了，因为有些服务是不方便随便重启的，要由
                |                 服务自己来控制；
                |--------------------------------------------------


 * xxx