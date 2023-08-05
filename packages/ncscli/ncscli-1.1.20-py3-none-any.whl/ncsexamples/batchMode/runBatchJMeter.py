#!/usr/bin/env python3
import datetime
import logging
import os
import subprocess
import sys

import ncscli.batchRunner as batchRunner


class JMeterFrameProcessor(batchRunner.frameProcessor):
    '''defines details for using JMeter for a simplistic load test'''

    def installerCmd( self ):
        return '/opt/apache-jmeter/bin/jmeter.sh --version'
        # could install an alternative version of jmeter, if the preinstalled version is not wanted
        '''
        jmeterVersion = '5.4.1'  # 5.3 and 5.4.1 have been tested, others may work as well
        cmd = 'curl -s -S -L https://mirrors.sonic.net/apache/jmeter/binaries/apache-jmeter-%s.tgz > apache-jmeter.tgz' % jmeterVersion
        cmd += ' && tar zxf apache-jmeter.tgz'
        return cmd
        # alternatively, could use https://mirror.olnevhost.net/pub/apache/... or https://downloads.apache.org/...
        '''
    JMeterFilePath = 'TestPlan.jmx'
    #JMeterFilePath = 'TestPlan_RampLong.jmx'
    #JMeterFilePath = 'TestPlan_RampLong_MoreSlow.jmx'
    #JMeterFilePath = 'TestPlan_RampLong_LessSlow.jmx'

    def frameOutFileName( self, frameNum ):
        return 'TestPlan_results_%03d.csv' % frameNum

    def frameCmd( self, frameNum ):
        cmd = '/opt/apache-jmeter/bin/jmeter.sh -n -t %s -l TestPlan_results_%03d.csv -D httpclient4.time_to_live=1 -D httpclient.reset_state_on_thread_group_iteration=true' % (
            self.JMeterFilePath, frameNum
        )
        return cmd


# configure logger formatting
#logging.basicConfig()
logger = logging.getLogger(__name__)
logFmt = '%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s'
logDateFmt = '%Y/%m/%d %H:%M:%S'
formatter = logging.Formatter(fmt=logFmt, datefmt=logDateFmt )
logging.basicConfig(format=logFmt, datefmt=logDateFmt)
#batchRunner.logger.setLevel(logging.DEBUG)  # for more verbosity

dateTimeTag = datetime.datetime.now().strftime( '%Y-%m-%d_%H%M%S' )
outDataDir = 'data/jmeter_' + dateTimeTag

try:
    rc = batchRunner.runBatch(
        frameProcessor = JMeterFrameProcessor(),
        commonInFilePath = JMeterFrameProcessor.JMeterFilePath,
        authToken = os.getenv( 'NCS_AUTH_TOKEN' ) or 'YourAuthTokenHere',
        encryptFiles=False,
        timeLimit = 80*60,
        instTimeLimit = 6*60,
        frameTimeLimit = 13*60,
        filter = '{"dpr": ">=48","ram:":">=2800000000","app-version": ">=2.1.11"}',
        outDataDir = outDataDir,
        startFrame = 1,
        endFrame = 6,
        nWorkers = 10,
        limitOneFramePerWorker = True,
        autoscaleMax = 2
    )
    if (rc == 0) and os.path.isfile( outDataDir +'/recruitLaunched.json' ):
        rampStepDuration = 60
        SLODuration = 240
        SLOResponseTimeMax = 1.5

        rc2 = subprocess.call( [sys.executable, 'plotJMeterOutput.py',
            '--dataDirPath', outDataDir,
            '--rampStepDuration', str(rampStepDuration), '--SLODuration', str(SLODuration),
            '--SLOResponseTimeMax', str(SLOResponseTimeMax)
            ],
            stdout=subprocess.DEVNULL )
        if rc2:
            logger.warning( 'plotJMeterOutput exited with returnCode %d', rc2 )
    sys.exit( rc )
except KeyboardInterrupt:
    logger.warning( 'an interuption occurred')
