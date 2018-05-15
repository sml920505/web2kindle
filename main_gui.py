# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Vincent<vincent8280@outlook.com>
#         http://wax8280.github.io
# Created on 2018/1/9 12:24
if __name__ == '__main__':
    try:
        from web2kindle import MAIN_CONFIG
        from web2kindle.webui.webui import app

        print("""                                                                                                         
                      VVV         VVVVVV   VVV          VVV                     VVV    VVV               
                      VVV        VVVVVVVV  VVV          VVV                     VVV    VVV               
                      VVV        VVV  VVVV VVV                                  VVV    VVV               
                      VVV       VVV    VVV VVV                                  VVV    VVV               
                      VVV             VVVV VVV                                  VVV    VVV               
 VVVVVVVVVVV VVVVVVV  VVVVVVVV        VVV  VVV  VVVV    VVV     VVVVVVVV   VVVVVVVV    VVV      VVVVVV   
 VVVVVVVVVV VVVV VVVV VVVV VVVV      VVVV  VVV VVV      VVV     VVVV VVVV VVVV VVVV    VVV     VVV  VVV  
 VVVVVVVVVV VVV   VVV VVVV  VVV      VVV   VVVVVV       VVV     VVV   VVV VVV  VVVV    VVV    VVVV  VVVV 
 VVVVVVVVVV VVVVVVVVV VVV   VVVV    VVV    VVVVVV       VVV     VVV   VVVVVVV   VVV    VVV    VVVVVVVVVV 
  VVVVVVVVV VVV       VVV   VVVV   VVVV    VVVVVVV      VVV     VVV   VVVVVVV   VVV    VVV    VVV        
  VVVVVVVV  VVV       VVV   VVV   VVVV     VVV VVV      VVV     VVV   VVV VVV   VVV    VVV    VVVV       
  VVVVVVVV  VVVV  VVV VVVV  VVV  VVVV      VVV  VVV     VVV     VVV   VVV VVV  VVVV    VVV     VVV  VVVV 
  VVVV VVV   VVVVVVVV VVVVVVVVV  VVVVVVVVV VVV  VVVV    VVV     VVV   VVV VVVVVVVVV    VVV     VVVVVVVV  
   VVV VVV    VVVVV   VVVVVVV    VVVVVVVVV VVV   VVV    VVV     VVV   VVV   VVVVVVV    VVV       VVVVV   

---------------------------------------------------------------------------------------------------------
Author:wax8280
Email:wax8280@163.com
Github:github.com/wax8280/web2kindle
Version:1.1.2""")
        app.run(port=MAIN_CONFIG.get('WEBUI_PORT', 1101))
    except:
        import traceback

        traceback.print_exc()
        input("任意键结束...")
