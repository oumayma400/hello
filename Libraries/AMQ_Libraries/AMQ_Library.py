from robot.api import logger
from lxml import etree
import stomp
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Listener(object):
    Messages= [[]]


    def __init__(self):
        self.Messages = []

    def on_error(self, headers, message):
        self.Messages.append('(ERROR) ' + message)

    def on_message(self, headers, message):
        self.Messages.append([message, headers['message-id']])


class AMQ_Library(object):
    """
    Library for SICONIA Test non-regression.

    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'


    def Inject(self,message:str, queue:str, host:str, port:int,user:str,password:str):
        """
        Inject message into ActiveMQ

        *Args:*\n

            | message  | XML message to inject into AMQ  on Queue |
            | queue    | queue name  |
            | host     | ActiveMQ host ( IP Address )  |
            | port     | ActiveMQ Port  |
            | user     | Queue username |
            | password | Queue Password |

        """
        print("le message a aenvoyer vers activemq ")
        print(message.decode('ascii'))
        c = stomp.Connection([(host, port),(host,port)],auto_content_length=False)
        c.connect(user,password, wait=True)
        c.send(queue, message)
        c.disconnect()
        logger.info("XML Injected Successfully !")


    def Consume(self,queue:str,correlationID:str,correlationIDPath:str,timeout:int,host:str, port:int,user:str,password:str):
        print("timeout equal to :", timeout)
        """
        Consume message from ActiveMQ with a specific message ID  before Timeout

        *Args:*\n

            | correlationID  | XML's correlationID ( message ID Used in Request ) to search on Queue  |
            | correlationID  | XML's correlationID ( message ID Used in Request ) to search on Queue  |
            | correlationIDPath | Path to correlationID in the xml response Example : reply/correlationId |
            | timeout  | Max Time to wait for a message on queue |
            | queue    | queue name  |
            | host     | ActiveMQ host ( IP Address )  |
            | port     | ActiveMQ Port  |
            | user     | Queue username |
            | password | Queue Password |

        """

        c = stomp.Connection([(host, port),(host,port)],auto_content_length=False)
        listener = Listener()
        c.set_listener('', listener)
        c.connect(user,password, wait=True)
        c.subscribe(destination='/queue/'+queue, id=912, ack='client-individual')
        # c.subscribe(destination='/queue/'+queue, id=911, ack='auto',headers={'activemq.prefetchSize':10})
        t=0
        replaycode=-1
        while(t<int(timeout)):
            t=t+1
            messageFound=False

            for message in listener.Messages:
                # print("message : ", message)
                root = etree.fromstring(str.encode(message[0]))
                tree = etree.ElementTree(root)
                root= tree.getroot()
                if root.find(correlationIDPath,root.nsmap).text==correlationID:
                    print(message)
                    messageFound=True
                    replaycode= root.find("reply/replyCode",root.nsmap).text
                    print('root[0][3].text' , root[0][3].text)
                    responsetime=root[0][3].text
                    print("message id to ack = ", message[1] )
                    c.ack(message[1], 912)
                    break
            time.sleep(1)
            if messageFound==True:
                break
        c.disconnect()
        if messageFound==True:
            logger.info(message[0])
            return 200,message[0], replaycode,responsetime
        else:
            print(datetime.datetime.now())
            logger.error("Message with correlation ID"+ correlationID +"is not found")
            return 408,"Time Out",replaycode, 'no reception time'
    def inject_with_gui(self,message :str, queue:str, host:str, port:str,user:str,password:str):
        driver = webdriver.Firefox()
        url='http://'+user +':'+password +'@'+str(host)+':'+str(port)+'/admin/send.jsp'
        queue=queue
        driver.get(url)
        dest=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/div[2]/div/div/div/table/tbody/tr/td[1]/div/form/table/tbody/tr[1]/td[2]/input')))
        dest.clear()

        dest.send_keys(queue)
        dest=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/div[2]/div/div/div/table/tbody/tr/td[1]/div/form/table/tbody/tr[11]/td/textarea')))
        dest.clear()
        print('message to send : ', message)
        dest.send_keys(message.decode('ascii'))
        send=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/div[2]/div/div/div/table/tbody/tr/td[1]/div/form/table/tbody/tr[9]/td/input[1]')))
        send.click()
        return 200

    def ConsumeCapabilitiesAll(self,queue:str,meterID:str,timeout:int,host:str,port:int,user:str,password:str) -> str:
        print("start consuming message for device", meterID)

        c = stomp.Connection([(host, port)], heartbeats=(4000, 4000))
        listener = Listener()
        c.set_listener('', listener)

        c.connect(user,password, wait=True)
        c.subscribe(destination='/queue/'+queue, id=912, ack='client-individual')
        i=0


        while(i<int(timeout)):
            i=i+1

            CapaFound=False
            for message in listener.Messages:

                root = etree.fromstring(str.encode(message[0]))
                tree = etree.ElementTree(root)
                root= tree.getroot()
                if (root.find('meter',root.nsmap).text==meterID):
                    print(message)
                    CapaFound=True
                    print("message id to ack = ", message[1] )
                    c.ack(message[1], 912)
                    # break

            time.sleep(1)
            if CapaFound==True:

                print('Capa message is '+message[0])
                break
        c.disconnect()
        if CapaFound==True:
            logger.info(message[0])
            return "200",message[0]
        else:
            logger.error("no capa message for the meter"+meterID+ "was found!!!")
            return "408","Time Out"
    def Clean_Queues(self,queue:str,host:str, port:int,user:str,password:str):

        """
        Consume message from ActiveMQ with a specific message ID  before Timeout

        *Args:*\n

            | correlationID  | XML's correlationID ( message ID Used in Request ) to search on Queue  |
            | correlationID  | XML's correlationID ( message ID Used in Request ) to search on Queue  |
            | correlationIDPath | Path to correlationID in the xml response Example : reply/correlationId |
            | timeout  | Max Time to wait for a message on queue |
            | queue    | queue name  |
            | host     | ActiveMQ host ( IP Address )  |
            | port     | ActiveMQ Port  |
            | user     | Queue username |
            | password | Queue Password |

        """
        try:
            c = stomp.Connection([(host, port)], heartbeats=(4000, 4000))
            listener = Listener()
            c.set_listener('', listener)
            c.connect(user,password, wait=True)
            c.subscribe(destination='/queue/'+queue, id=1, ack='auto')
            return 200
        except Exception as e:
            return 500
