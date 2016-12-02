from flask import Flask, request, Response, session

class ConsoleFlask(Flask):
    def __init__(self, import_name, static_path=None, static_url_path=None,
                 static_folder='static', template_folder='templates',
                 instance_path=None, instance_relative_config=False,
                 root_path=None):
        Flask.__init__(self, import_name, static_path=static_path,
                 static_url_path=static_url_path, static_folder=static_folder,
                 template_folder=template_folder, instance_path=instance_path,
                 instance_relative_config=instance_relative_config,
                 root_path=root_path)

#    def send_static_file(self, filename):
#        # Get user from session
#        print(session)
#        if user.is_authenticated():
#            return super(SecuredStaticFlask, self).send_static_file(filename)
#        else:
#            return Response(
#           'Could not verify your access level for that URL.\n'
#            'You have to login with proper credentials', 401,
#            {'WWW-Authenticate': 'Basic realm="Login Required"'})
