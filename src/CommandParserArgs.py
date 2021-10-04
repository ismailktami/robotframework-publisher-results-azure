import argparse
def ParseCommandLineParameters():
    global OUTPUTDIR,USERNAME,JOB_URL,JOB_NAME,JOB_ID,JOB_STARTED_TIME,ENVIRONNEMENT
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir", "--output-dir",action="store", dest="outputdir", default='output_dir')
    parser.add_argument("-u", "--username",action="store", dest="username", default='Ismail Ktami')
    parser.add_argument("-i", "--jobid",action="store", dest="jobid", default='XXXYYY')
    parser.add_argument("-t", "--jobstartedtime",action="store", dest="jobstartedtime",default='00/66/44')
    parser.add_argument("-n", "--jobname",action="store", dest="jobname", default='JOB NAME')
    parser.add_argument("-l", "--joburl",action="store", dest="joburl", default='www.job.url.com')
    parser.add_argument("-e", "--env",action="store", dest="environnement", default='release')

    results = parser.parse_args()
    OUTPUTDIR = results.outputdir
    USERNAME = results.username
    JOB_URL = results.joburl
    JOB_NAME = results.jobname
    JOB_ID =results.jobid
    JOB_STARTED_TIME=results.jobstartedtime
    ENVIRONNEMENT=results.environnement