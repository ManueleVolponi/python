
import controller
import os

resp = controller.execute()

if resp == '' :
        resp = 'y'
if resp == 'y' :
    cmd = 'sudo systemctl status apache2'
    os.system(cmd)
else:
    print("See you later")




