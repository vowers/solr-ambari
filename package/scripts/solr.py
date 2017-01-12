import sys, os, pwd, grp, signal, time
import sys
from resource_management import *

class Solr(Script):
    def install(self, env):
        
        #import properties defined in -config.xml file from params class
        import params
        import status_params
        # Install packages listed in metainfo.xml
        #self.install_packages(env)
        Execute('find '+params.service_packagedir+' -iname "*.sh" | xargs chmod +x')	
        try: grp.getgrnam(params.solr_group)
    	except KeyError: Group(group_name=params.solr_group) 
    
    	try: pwd.getpwnam(params.solr_user)
    	except KeyError: User(username=params.solr_user, 
                          gid=params.solr_group, 
                          groups=[params.solr_group], 
                          ignore_failures=True)    

        Directory([params.solr_log_dir, status_params.solr_piddir, params.solr_dir],
              mode=0755,
              cd_access='a',
              owner=params.solr_user,
              group=params.solr_group
            )


        File(params.solr_log,
            mode=0644,
            owner=params.solr_user,
            group=params.solr_group,
            content=''
            )


        Execute('echo Solr dir: ' + params.solr_dir)
        
        #params.solr_downloadlocation

        Execute('cd ' + params.solr_dir + '; wget  -c' + params.solr_downloadlocation +' -O solr.tgz -o '+ params.solr_log, user=params.solr_user)
        Execute('cd ' + params.solr_dir + '; tar -xvf solr.tgz', user=params.solr_user)
        Execute('cd ' + params.solr_dir + '; ln -s solr latest', user=params.solr_user)
        
        
        
        Execute('chown -R '+params.solr_user + ':' + params.solr_group + ' ' + params.solr_dir)            
       
        Execute ('echo "Solr install complete"')
	
    def configure(self, env):
        import params
        env.set_params(params)
        
        #write content in jinja text field to solr.in.sh
        env_content=InlineTemplate(params.solr_env_content)
        File(format("{solr_conf}/solr.in.sh"), content=env_content, owner=params.solr_user)    

        
        xml_content=InlineTemplate(params.solr_xml_content)    
        File(format("{solr_datadir}/solr.xml"), content=xml_content, owner=params.solr_user)    

        log4j_content=InlineTemplate(params.solr_log4j_content)    
        File(format("{solr_log4jdir}/resources/log4j.properties"), content=log4j_content, owner=params.solr_user)    

        zoo_content=InlineTemplate(params.solr_zoo_content)    
        File(format("{solr_datadir}/zoo.cfg"), content=zoo_content, owner=params.solr_user)    


    def start(self, env):

        #import properties defined in -config.xml file from params class
        import params

        #import status properties defined in -env.xml file from status_params class
        import status_params
        self.configure(env)

        #this allows us to access the params.solr_pidfile property as format('{solr_pidfile}')
        env.set_params(params)
            
        Execute('find '+params.service_packagedir+' -iname "*.sh" | xargs chmod +x')

        cmd = params.service_packagedir + '/scripts/start.sh ' + params.solr_dir + ' ' + params.solr_log + ' ' + status_params.solr_pidfile + ' ' + params.solr_bindir
        Execute('echo "Running cmd: ' + cmd + '"')    
        Execute(cmd, user=params.solr_user)

    def stop(self, env):

        import params
     
        #import status properties defined in -env.xml file from status_params class  
        import status_params
        
        #this allows us to access the params.solr_pidfile property as format('{solr_pidfile}')
        env.set_params(params)
        #self.configure(env)

        
        #kill the instances of solr
        Execute (format('SOLR_INCLUDE={solr_conf}/solr.in.sh {solr_bindir}/solr stop -all >> {solr_log}'), user=params.solr_user, ignore_failures=True)  

        #delete the pid file
        Execute (format("rm -f {solr_pidfile} >> {solr_log}"), user=params.solr_user, ignore_failures=True)

    def status(self, env):
        
        #import status properties defined in -env.xml file from status_params class
        import status_params
        env.set_params(status_params)  
        
        #use built-in method to check status using pidfile
        check_process_status(status_params.solr_pidfile)  

if __name__ == "__main__":
    Solr().execute()
